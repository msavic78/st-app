# data_editing.py

import base64
import os
import streamlit as st
import pandas as pd

# Function to display a DataFrame and allow cell editing
def display_and_edit_dataframe(df, df_key, file_path):
    if 'df_changes' not in st.session_state:
        st.session_state.df_changes = pd.DataFrame()

    # Use st.columns to place inputs on the same row
    col1, col2, col3 = st.columns(3)  # Create three columns
    with col1:
        row_to_edit = st.number_input("Enter the row index to edit:", min_value=0, max_value=len(df)-1, key=f"row_{df_key}")
    with col2:
        column_to_edit = st.selectbox("Select the column to edit:", df.columns, key=f"col_{df_key}")
    with col3:
        new_value = st.text_input("Enter the new value:", key=f"new_{df_key}")

    if st.button("Apply Changes", key=f"apply_{df_key}"):
        try:
            current_value = df.at[row_to_edit, column_to_edit]
            new_value_converted = type(current_value)(new_value)
            df.at[row_to_edit, column_to_edit] = new_value_converted
            st.session_state.df_changes = df  # Update the session state with the new df
            st.success(f"Value updated successfully: {new_value_converted}")

            # Generate download link after successful save
            filename = os.path.basename(file_path)  # Extract filename from path
            download_link_html = download_link(st.session_state.df_changes.copy(), filename)
            st.markdown(download_link_html, unsafe_allow_html=True)  # Allow HTML for download link

        except Exception as e:
            st.error(f"Failed to update the value. Error: {e}")

# Download for edited file
def download_link(df, filename):
    """Generates a downloadable link for the DataFrame."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode('utf-8')).decode()  # Base64 encode for download
    href = f"<a href='data:application/octet-stream;base64,{b64}' download='{filename}'>Download {filename}</a>"
    return href



