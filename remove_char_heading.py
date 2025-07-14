import os
import pandas as pd
import re

# Define the input and output folder paths
input_folder = r"C:\Users\Lenovo\Downloads\set-5\Datasets\INDEX"
output_folder = r"C:\Users\Lenovo\Desktop\MY-Code\stock_project\output_folder"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop through all CSV files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        # Construct the full file path
        input_file = os.path.join(input_folder, filename)
        
        # Load the CSV file
        df = pd.read_csv(input_file)
        
        # Remove the prefixes ('NIFTY50 ', 'NIFTY100 ', 'NIFTY ') from headers and numbers
        df.columns = df.columns.str.replace(r'^(NIFTY50|NIFTY100|NIFTY)\s*\d*\s*', '', regex=True)
        
        # Create a new filename without the prefixes and numbers
        new_filename = re.sub(r'^(NIFTY50|NIFTY100|NIFTY|YR)\s*\d*\s*', '', filename)
        
        # Construct the output file path
        output_file = os.path.join(output_folder, new_filename)
        
        # Save the updated CSV to the output folder
        df.to_csv(output_file, index=False)

print("Files processed and saved successfully!")
