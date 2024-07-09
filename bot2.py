from botbuilder.core import TurnContext, ActivityHandler
from botbuilder.core.integration import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity, ActivityTypes
import requests
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

class Bot2(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        # Receive the complaint from Bot1
        complaint = turn_context.activity.text
        await turn_context.send_activity(f"Support Team received your complaint: {complaint}")

        # Categorize the complaint
        category = self.categorize_complaint(complaint)
        await turn_context.send_activity(f"The complaint is categorized as: {category}")

        # Respond to the complaint
        response_message = "Thank you for your feedback. Our team is working on improving the mobile banking application. We apologize for the inconvenience."
        await turn_context.send_activity(response_message)

    def categorize_complaint(self, complaint):
        # Use Azure Text Analytics API to extract key phrases
        endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
        key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
        
        url = f"{endpoint}/text/analytics/v3.1/keyPhrases"
        headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
        documents = {"documents": [{"id": "1", "language": "en", "text": complaint}]}
        
        response = requests.post(url, headers=headers, json=documents)
        key_phrases = response.json().get("documents", [])[0].get("keyPhrases", [])
        
        if not key_phrases:
            return "Uncategorized"
        
        # Simple categorization based on key phrases
        # TODO: define more categories and improve the categorization logic
        if any(phrase in ["crashes", "crash", "unstable"] for phrase in key_phrases):
            return "Stability Issues"
        elif any(phrase in ["UI", "user interface", "user experience", "UX"] for phrase in key_phrases):
            return "User Interface Issues"
        else:
            return "General Issues"

# Bot setup
# TODO: replace YOUR_APP_ID and YOUR_APP_PASSWORD with your bot's app ID and password
app_id = "YOUR_APP_ID"
app_password = "YOUR_APP_PASSWORD"
settings = BotFrameworkAdapterSettings(app_id, app_password)
adapter = BotFrameworkAdapter(settings)

bot = Bot2()

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
    app.run(port=3979)
