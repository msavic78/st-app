import os
import pandas as pd
import streamlit as st
import re

from data_loading import filter_columns
from login import getClientEmail
from data_comparison import normalize_column

# Regex pattern for validating an email
EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

# Function to get a list of files in a directory
def get_files(directory):
    
    # Returns a list of filenames found in the directory.
    files = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

# Function to display the files in a directory
def show_files(location, action):
    
    # Check if the action is "Delete"
    # If so, get the current user's email
    actionIsDelete = action == "Delete"

    if actionIsDelete:
        
        # Get the current user's email
        client_email = getClientEmail()

        # Extract the email address from the client_email
        curr_usr_email = re.findall(EMAIL_REGEX, client_email)
        
        # Check if the email address was found
        if curr_usr_email:
            curr_usr_email = curr_usr_email[0]  # Extract the first (and presumably only) email address
        else:
            curr_usr_email = ""
    
    # Check if the location exists and is a directory
    if os.path.exists(location) and os.path.isdir(location):
        
        # Get the list of directories
        dir_list = next(os.walk(location))[1]

        # Display the result in Streamlit
        with st.expander(f"{action} Hotel Rooming List", expanded=False):

            # Initialize the selected file
            selected_file = None

            # Display the list of directories
            selected_dir = st.selectbox("Select a directory:", dir_list)

             # Get the list of files in the selected directory
            file_list = get_files(os.path.join(location, selected_dir))

            # Filter the file list based on the current user's email
            # This is to ensure that a user can only delete their own files
            # This is not necessary for the "Load" action
            user_files = [file for file in file_list] if not actionIsDelete else [file for file in file_list if curr_usr_email in file]
            
            # Display the result in Streamlit
            if file_list:
                st.markdown(f"<span style='color:#3C8595;font-weight:bold; border-bottom: 1px olsid #CCCCCC;'>Rooming lists you have uploaded so far:</span>", unsafe_allow_html=True)

                # Display the list of files
                selected_file = st.selectbox("Select a file:", user_files)

                # Add a button for deleting the selected file
                if st.button(f'{action} Hotel rooming list'):
                    try:
                        file_path = os.path.join(location, selected_dir, selected_file)
                        if action == "Delete":
                            os.remove(file_path)
                            st.success(f'Successfully deleted {selected_file}!')
                            st.rerun()
                        elif action == "Load":
                            #df = pd.read_excel(file_path) # Load the file
                            #df = normalize_column(df.copy(), "Conf. #") # Normalize the column names
                            #df_filtered = filter_columns(df) # Filter the columns
                            #return df_filtered # Display the dataframe
                            return file_path

                    except Exception as e:
                        st.error(f'Error when trying to {action.lower()} file: {e}')

            else:
                st.write("No files found in the directory.")
    else:
        st.error("The provided path does not exist or is not a directory.")
