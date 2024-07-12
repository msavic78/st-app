import pandas as pd
import re
import logging
from datetime import datetime
import sys
import os

# Setup logging
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_filename = f'log_{timestamp}.txt'

logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(message)s')

# Ensure correct number of arguments
if len(sys.argv) != 3:
    print("Usage: python script_name.py <file1_path> <file2_path>")
    sys.exit(1)

# Get file names from command line arguments
file1_path = sys.argv[1].strip()
file2_path = sys.argv[2].strip()

# Check if files exist
if not os.path.isfile(file1_path):
    print(f"File not found: {file1_path}")
    sys.exit(1)
if not os.path.isfile(file2_path):
    print(f"File not found: {file2_path}")
    sys.exit(1)

# Load the files
file1 = pd.read_excel(file1_path)
file2 = pd.read_excel(file2_path)

# Combine data on the Summary column without changing its case
combined = pd.merge(file1, file2, on='Summary', suffixes=('_file1', '_file2'), how='left')

# Identify missing keys
missing_keys = combined[combined['Issue key_file2'].isnull()]

# Log missing keys
logging.info("Rows with missing issue keys in the second file:")
logging.info(missing_keys[['Summary', 'Issue key_file1']].to_string(index=False))

# Additional analysis on missing keys
logging.info("\nMissing keys detailed analysis:")
for index, row in missing_keys.iterrows():
    logging.info(f"Summary: {row['Summary']}, Issue Key: {row['Issue key_file1']}")

# Create a map of old to new issue keys
key_map = dict(zip(combined['Issue key_file1'].dropna(), combined['Issue key_file2'].dropna()))

# Ensure the Sprint column exists in the target file
if 'Sprint' not in file2.columns:
    file2['Sprint'] = None

# Update Sprint column based on the source file and project name from the target file
for index, row in file2.iterrows():
    summary = row['Summary']
    if summary in file1['Summary'].values:
        source_sprint = file1.loc[file1['Summary'] == summary, 'Sprint'].values[0]
        issue_key = row['Issue key']
        project_name = issue_key.split('-')[0]  # Extract project name from Issue key
        if pd.notnull(source_sprint) and pd.notnull(project_name):
            new_sprint = re.sub(r'^[A-Z]+[0-9]+', project_name, source_sprint)
            file2.at[index, 'Sprint'] = new_sprint

# Save the updated file
output_file = 'Updated-Sprints.xlsx'
file2.to_excel(output_file, index=False)

logging.info(f"Updated file saved as {output_file}")
