import pandas as pd

# Load CSV file with UTF-8 encoding
csv_file = 'dataset.csv'
data = pd.read_csv(csv_file, encoding='utf-8')

# Convert to JSON
json_data = data.to_json(orient='records', force_ascii=False)

# Save JSON file with UTF-8 encoding
with open('datasetjsonified.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)
