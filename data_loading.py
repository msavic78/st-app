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


def filter_columns(df):

     # Count columns containing "Name" (case-insensitive)
    name_column_count = sum(col.lower().find("name") != -1 for col in df.columns)

    if name_column_count == 1:
        df_normalized = split_name_column(df)

    # Columns to keep based on your criteria
    keep_columns = [col for col in df.columns if 
                    "Name" in col or 
                    "Arr" in col or 
                    "Dep" in col or
                    "Conf" in col]


    # Ensure string type in the new columns
    df['First Name'] = df['First Name'].astype(str)
    df['Last Name'] = df['Last Name'].astype(str)

    # Filter and return the modified DataFrame
    return df[keep_columns]

import pandas as pd

def split_name_column(df, column_name="Name"):
    """Detects a single 'Name' column, splits it into 'First Name' and 'Last Name', and updates the DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        column_name (str, optional): The name of the column containing combined names. Defaults to "Name".

    Returns:
        pandas.DataFrame: The modified DataFrame with split name columns.
    """

    if column_name in df.columns:
        df.insert(0, 'Last Name', df[column_name].str.split(',', n=1, expand=True)[0])
        df.insert(1, 'First Name', df[column_name].str.split(',', n=1, expand=True)[1])
        df.drop(column_name, axis=1, inplace=True)

        # Renaming logic
        # st.cache_data.clear()  # Clear the cache
        df_cleared = df.rename(columns={"Arr.": "Arrival", "Dep.": "Departure"}, inplace=True)

    return df_cleared

