# data_loading.py
import pandas as pd
import io
import streamlit as st

def load_csv(file_uploader, side):
    """Load data from a CSV or Excel file.

    Args:
        file_uploader (UploadedFile): The uploaded file object from Streamlit.

    Returns:
        pd.DataFrame: The loaded data as a DataFrame, or None if loading fails.
    """
    if file_uploader is not None:
        file_name = file_uploader.name
        bytes_data = file_uploader.read()  # Read file contents
        try:
            if file_name.endswith('.csv'):
                return pd.read_csv(io.BytesIO(bytes_data), encoding='ISO-8859-1', on_bad_lines='skip')
            elif file_name.endswith('.xlsx'):
                return pd.read_excel(io.BytesIO(bytes_data))
            else: # Handling unsupported file types
                st.error("File type not supported. Please upload a CSV or Excel file.")
                return None
        except Exception as e:
            st.error(f"Error processing the file: {e}")
    return None
