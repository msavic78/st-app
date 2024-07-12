import pandas as pd
import streamlit as st
from datetime import datetime

# Function to replace all instances of a string in a DataFrame
def replace_string_in_df(df, old_string, new_string):
    return df.replace(old_string, new_string, regex=True)

# Streamlit app
st.title("Jira Conference Name Replacement")

# File upload
uploaded_file = st.file_uploader("Upload an Excel file", type="xlsx")

# Input fields for old and new conference names
old_conference_name = st.text_input("Enter the existing conference name (e.g., AHA24)")
new_conference_name = st.text_input("Enter the new conference name (e.g., AAOS25)")

# Input field for the full new conference name
new_full_conference_name = st.text_input("Enter the full new conference name (e.g., AAOS 2025)")

# Button to perform the replacement
if st.button("Replace and Download"):
    if uploaded_file is not None and old_conference_name and new_conference_name and new_full_conference_name:
        # Load the uploaded file
        df = pd.read_excel(uploaded_file)

        # Replace old conference name with new conference name
        df = replace_string_in_df(df, old_conference_name, new_conference_name)

        # Replace the values in the 'Project Name' column with the new full conference name
        if 'Project Name' in df.columns:
            df['Project Name'] = new_full_conference_name

        # Generate a timestamped filename for the output
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f'Updated_File_{timestamp}.xlsx'

        # Save the updated DataFrame to a file
        df.to_excel(output_filename, index=False)

        # Provide a link to download the updated file
        with open(output_filename, 'rb') as f:
            st.download_button(
                label="Download Updated File",
                data=f,
                file_name=output_filename,
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        
        # Logging the operation
        log_filename = f'log_{timestamp}.txt'
        with open(log_filename, 'w') as log_file:
            log_file.write(f"Replaced '{old_conference_name}' with '{new_conference_name}' in the uploaded file\n")
            log_file.write(f"Set 'Project Name' column to '{new_full_conference_name}'\n")
            log_file.write(f"Updated file saved as {output_filename}\n")

        st.success("Replacement completed and log file created.")
    else:
        st.error("Please upload a file and enter all required conference names.")
