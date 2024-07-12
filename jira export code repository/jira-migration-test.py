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

# Function to update issue links for all relevant columns
def update_links(row, key_map):
    inward_columns = [col for col in row.index if 'Inward issue link (Blocks)' in col]
    outward_columns = [col for col in row.index if 'Outward issue link (Blocks)' in col]
    
    for col in inward_columns:
        if pd.notnull(row[col]):
            row[col] = key_map.get(row[col], row[col])
    
    for col in outward_columns:
        if pd.notnull(row[col]):
            row[col] = key_map.get(row[col], row[col])
    
    return row

# Update links in file1 based on key_map
file1 = file1.apply(update_links, key_map=key_map, axis=1)

# Identify all possible inward and outward columns
all_inward_columns = [col for col in combined.columns if 'Inward issue link (Blocks)' in col]
all_outward_columns = [col for col in combined.columns if 'Outward issue link (Blocks)' in col]

# Ensure all inward and outward columns are present in the final file1 dataframe
for col in all_inward_columns:
    if col not in file1.columns:
        file1[col] = None

for col in all_outward_columns:
    if col not in file1.columns:
        file1[col] = None

# Check for unchanged values
unchanged_inward = file1[file1.filter(regex='Inward issue link \(Blocks\)').apply(lambda x: x.str.contains('AHA', na=False)).any(axis=1)]
unchanged_outward = file1[file1.filter(regex='Outward issue link \(Blocks\)').apply(lambda x: x.str.contains('AHA', na=False)).any(axis=1)]

# Log unchanged values
logging.info("Rows with unchanged Inward issue link (Blocks):")
logging.info(unchanged_inward[['Summary'] + list(unchanged_inward.filter(regex='Inward issue link \(Blocks\)').columns)].to_string(index=False))
logging.info("Rows with unchanged Outward issue link (Blocks):")
logging.info(unchanged_outward[['Summary'] + list(unchanged_outward.filter(regex='Outward issue link \(Blocks\)').columns)].to_string(index=False))

# After updating the inward/outward links, update the Issue Key column
file1['Issue key'] = file1['Issue key'].map(key_map)

# Remove suffixes from column names
file1.columns = [col.split('_')[0] for col in file1.columns]

# Save the updated file
output_file = 'Updated-Blocked.xlsx'
file1.to_excel(output_file, index=False)

logging.info(f"Updated file saved as {output_file}")
