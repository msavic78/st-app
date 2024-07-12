import logging
import pandas as pd
import sys
import os
from datetime import datetime

# Function to replace all instances of a string in a DataFrame
def replace_string_in_df(df, old_string, new_string):
    return df.replace(old_string, new_string, regex=True)

# Setup logging
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_filename = f'log_{timestamp}.txt'

logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(message)s')

# Ensure correct number of arguments
if len(sys.argv) != 5:
    print("Usage: python script_name.py <file_path> <output_path> <old_conference_name> <new_conference_name>")
    sys.exit(1)

# Get file names and conference names from command line arguments
file_path = sys.argv[1].strip()
output_path = sys.argv[2].strip()
old_conference_name = sys.argv[3].strip()
new_conference_name = sys.argv[4].strip()

# Check if file exists
if not os.path.isfile(file_path):
    print(f"File not found: {file_path}")
    sys.exit(1)

# Load the file
df = pd.read_excel(file_path)

# Replace old conference name with new conference name
df = replace_string_in_df(df, old_conference_name, new_conference_name)

# Save the updated file
df.to_excel(output_path, index=False)

print(f"Updated file saved as {output_path}")

# Logging the operation
with open(log_filename, 'w') as log_file:
    log_file.write(f"Replaced '{old_conference_name}' with '{new_conference_name}' in file {file_path}\n")
    log_file.write(f"Updated file saved as {output_path}\n")

print(f"Log file created: {log_filename}")
