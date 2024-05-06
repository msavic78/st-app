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
    file_path = os.path.join(save_path, filestamp + file.name)

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