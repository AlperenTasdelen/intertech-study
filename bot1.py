from botbuilder.core import TurnContext, ActivityHandler
from botbuilder.core.integration import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity, ActivityTypes
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

class Bot1(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        # Simulate a customer complaint
        customer_complaint = "I am facing issues with the mobile banking application. It crashes frequently and the UI is not user-friendly."
        await turn_context.send_activity(f"Customer: {customer_complaint}")

        # Forward the complaint to Bot2
        response = requests.post('https://bot2-endpoint/api/messages', json={"text": customer_complaint})
        if response.status_code == 200:
            await turn_context.send_activity("Your complaint has been forwarded to the support team.")
        else:
            await turn_context.send_activity("Failed to forward the complaint. Please try again later.")

# Bot setup
app_id = "YOUR_APP_ID"
app_password = "YOUR_APP_PASSWORD"
settings = BotFrameworkAdapterSettings(app_id, app_password)
adapter = BotFrameworkAdapter(settings)

bot = Bot1()

@app.route("/api/messages", methods=["POST"])
async def messages():
    body = await request.json()
    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")

    response = await adapter.process_activity(activity, auth_header, bot.on_turn)
    if response:
        return jsonify(response.body), response.status
    return "", 200

if __name__ == "__main__":
    app.run(port=3978)
