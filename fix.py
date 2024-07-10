import pandas as pd
import csv

# Load the original CSV file with quote handling
csv_file = 'dataset.csv'

# Read the CSV file
data = pd.read_csv(csv_file, encoding='utf-8', quotechar='"', skipinitialspace=True)

# Strip leading and trailing spaces from the second and third columns
data.iloc[:, 1] = data.iloc[:, 1].str.strip()
data.iloc[:, 2] = data.iloc[:, 2].str.strip()

# Save the cleaned data to a new CSV file with quotes preserved
cleaned_csv_file = 'cleaned_file.csv'
data.to_csv(cleaned_csv_file, index=False, quoting=csv.QUOTE_MINIMAL, encoding='utf-8')

print(f'Cleaned CSV file saved as {cleaned_csv_file}.')
