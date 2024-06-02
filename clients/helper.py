import os
import streamlit as st
from login import getClientEmail

def display_hotel_rooming_list(df):
    rl_hotel = f"<br><p style='color:Red; font-size:20px; margin-bottom:0px; padding:0px;'>Hotel Rooming List<p>"
    st.markdown(rl_hotel, unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

def save_file_to_server(file):
    # Use the current working directory
    upload_folder = 'rl_uploads'
    save_path = os.path.join(os.getcwd(), upload_folder)  
    os.makedirs(save_path, exist_ok=True)  # Ensure the directory exists

    # Add email and timestamp (exclude minutes and seconds later on)
    filestamp = getClientEmail()

     # Get the extension of the file
    _, extension = os.path.splitext(file.name)

    file_path = os.path.join(save_path, filestamp + extension)

    # Ensure the file name is valid and handle common issues
    if '/' in file.name or '\\' in file.name:
        st.error("File name is invalid. Please ensure it does not contain path characters.")
    else:
        try:
            with open(file_path, 'wb') as f:
                f.write(file.getbuffer())
            st.success("File saved successfully.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Function to hide rows in a DataFrame
def hide_rows(df, rows_to_hide):
    """
    This function hides selected rows from a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame from which to hide rows.
    rows_to_hide (list): The list of row indices to hide.

    Returns:
    pd.DataFrame: The DataFrame with the selected rows hidden.
    """
    df_hidden_rows = df.drop(rows_to_hide)
    return df_hidden_rows

def hide_identical_rows(checkbox, in_df_style, same_rows):
    in_df = in_df_style.data
    if checkbox:
            in_df= hide_rows(in_df, same_rows)
            return in_df.style
    else:
        return in_df_style