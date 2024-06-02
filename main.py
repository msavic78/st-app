# Standard library imports
import time
import os

# Related third party imports
import pandas as pd
import streamlit as st

# Local application/library specific imports
from clients.form import show_files
from clients.helper import hide_identical_rows, hide_rows
from data_comparison import compare_dataframes, normalize_column
from data_editing import addAvatarColumn, update_df_in_session_only
from data_loading import filter_columns, load_and_process_data
from login import getClientEmail, show_login_form
from ui import change_label_style, display_header, display_title, display_rooming_list_validation, display_hotel_rooming_list
from styles import get_css

st.set_page_config(layout="wide")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_type'] = None  # Initialize user type in session state

st.session_state['hotel_rooming_list'] = None

# Show login form if not logged in, otherwise show the main application
if not st.session_state['logged_in']: # correct syntax for NOT
    show_login_form()
else:

    # DONE (form.py): Move the code for the whole upload section to a separate file!
    # DODAJ ISTU SEKCIJU I ZA ADMINA GDE MOZE DA POKUPI FILE DIREKTNO UMESTO DA POVUCE SA DISKA 
    # -> (form.py): Move the code for the whole upload section to a separate file!
    # Add check for xls files and csv files - if none of the two -> Discard
    # Make sure the IP address is saved to a log along with the exact filename (TBU for filtering)
    # DONE: Make sure they cannot log in files if the username filed is not an email format
    # DONE: Add and check if the email is a real email address -> reject if invalid
    # IN PROGRESS: Move all CSS to an external file
    # Change log file once a month -> logs should be saved in CSV format
    # DONE: Show the client based on their email a list of formerly uploaded files
    # Provide a status to know whether they have been updated or not
    # Allow the user to download updated file from the list
    # DONE: Prevent an upload of the two files with the same name
    # DONE: Timestamp should be automatically appended but with the seconds and minutes discarded
    # Clients should be able to look no more than a month into the past uploads
    # Add text to page which explain the user what they need to do.
    # TAKODJE - KAD GOD SE UNESE IZMENA ZA FILE, ROOMING LIST DISCREPANCIES TREBA DA SE UPADETUJE KAKO NI POKAZAO DA JE IZMENA NAPRAVLJENA
    # Dodaj poruku za uspesan upload za klijente 
    # i nakon toga skloni poruku za uspesan upload i skloni polja za ime konferencije i hotela
    
    # CLIENT ROOMSYNC
    if st.session_state['user_type'] == "client":

        # Header & Custom CSS to make it sticky
        display_header()
        st.markdown(get_css(), unsafe_allow_html=True)

        with st.expander("Upload Rooming List", expanded=True):

            left_file = st.file_uploader("Upload Client Rooming List", key="left")
            left_df = load_and_process_data(left_file, "viaUploader")

        # Using Hotel column-filtered Rooming List
        show_files('rl_uploads', 'Delete')
        
        # Create placeholders for the original dataframes
        if left_df is not None:

            # CHECK OUT THE HELPER FUNCTION IN THE FORM.PY and see if it can be used here

            # Create placeholders for the original dataframes
                        
            # Remove trailing dots from the Booking Number
            left_df = normalize_column(left_df.copy(), "Conf. #")
            left_df_filtered = filter_columns(left_df)
            
            # Set upload section to be closed by default
            # st.session_state.expander_open = False  
           
            rl_hotel = f"<br><p style='color:Red; font-size:20px; margin-bottom:0px; padding:0px;'>Hotel Rooming List<p>"
            st.markdown(rl_hotel, unsafe_allow_html=True)
            st.dataframe(left_df_filtered, use_container_width=True)


            # Submit button to save the file
            if st.button('Save to Server'):

                # Use session state to store whether the button has been clicked
                st.session_state.save_clicked = True

            # Show the hotel name input only if the "Save to Server" button has been clicked
            if st.session_state.get('save_clicked', False):

               # Create two columns
                col1, col2 = st.columns(2)

                # Prompt the user for the conference and hotel names
                conference_name = col1.selectbox('Select a conference', ['AAD', 'AAN', 'AAOS', 'ADA', 'ASBMR'])
                hotel_name = col2.text_input("Enter the hotel name:")

                 # Add a confirm button
                if st.button('Confirm'):

                    # Only proceed with the upload if the hotel name is not empty
                    if conference_name and hotel_name:

                        # Use the current working directory
                        upload_folder = 'rl_uploads'
                        save_path = os.path.join(os.getcwd(), upload_folder, conference_name)  
                        os.makedirs(save_path, exist_ok=True)  # Ensure the directory exists

                        # Add email and timestamp (exclude minutes and seconds later on)
                        filestamp = getClientEmail()

                        # Get the extension of the file
                        _, extension = os.path.splitext(left_file.name)

                        file_path = os.path.join(save_path, filestamp + hotel_name + extension)

                        # Create a placeholder for the success message
                        success_message = st.empty()

                        # Ensure the file name is valid and handle common issues
                        if '/' in left_file.name or '\\' in left_file.name:
                            st.error("File name is invalid. Please ensure it does not contain path characters.")
                        else:
                            try:
                                with open(file_path, 'wb') as f:
                                    f.write(left_file.getvalue())
                                #st.success(f'File saved successfully at ' + file_path + '!')
                                success_message.success(f'{hotel_name} - Rooming List saved successfully')
                                time.sleep(5)
                                success_message.empty()
                                # st.rerun()
                            except Exception as e:
                                st.error(f"Failed to save file: {e}")

                    else:
                        msg = st.success('Rooming list loaded successfully.')
            

    # ADMIN ROOMSYNC
    elif st.session_state['user_type'] == "admin":

         # Load Data (data_loading.py)
        from data_loading import load_csv

        display_header()

        ### Custom CSS for the sticky header
        st.markdown(get_css(), unsafe_allow_html=True)
        
         # Initialize session state(s) if necessary
        if "expander_open" not in st.session_state:
            st.session_state.expander_open = True  # Initial state as open
        
        # wrap in container
        file_upload_expander = st.expander("Load ABTSolute Rooming List", expanded=st.session_state.expander_open)
        
        #change_label_style("Load ABTSolute Rooming List",'18px', 'blue')

        # Using Hotel column-filtered Rooming List
        # The idea is to use the uploaded rooming lists instead of selecting the one from the hard drive
        # As users will be able to upload the files, the files will be stored in the session state
        # and the session state will be used to display the files in the expander
        # The files will be stored in the session state as dataframes
        # The dataframes will be used to compare the data
        # basically substituting the file selection with the file upload
        
        path = show_files('rl_uploads', 'Load')
        
        # If there is a path, store it in the session state
        if path is not None:
            if 'file_path' not in st.session_state:
                st.session_state.file_path = path

        with file_upload_expander:
            
            # Load dataframes without displaying them immediately
            #left_file = st.file_uploader("Upload Hotel Rooming List", key="left")
            right_file = st.file_uploader("Upload Client Rooming List", key="right")

            # If the state change were set to occur on the second file upload, 
            # the state would indeed update. However, the code would continue to line 142, 
            # effectively using the previous session state to determine the expander's behavior. 
            # This is because the code execution would not return to re-render 
            # the expander with the updated state.
            
            # If the left file is uploaded, close the expander
            # if left_file is not None:
            if right_file is not None:
                st.session_state.expander_open = False

        # Load the dataframes
        
        # On reload path info is lost and the load_csv function is called by passing the session state path
        # This is done to ensure that the file is loaded when the page is reloaded
        if 'file_path' not in st.session_state:
            left_df = load_csv(path, "viaPath")
        else:
            left_df = load_csv(st.session_state.file_path, "viaPath") 
        
        #left_df = load_csv(left_file, "viaUploader") 
        right_df = load_csv(right_file, "viaUploader")


        # Create placeholders for the original dataframes
        placeholder_left = st.empty()
        placeholder_right = st.empty()

        # Compare and display differences if both dataframes exist and have the same format
        if left_df is not None and right_df is not None:

            # Set Booking Number to String Type
            #left_df['Conf. #'] = left_df['Conf. #'].astype(str)
            #right_df['Conf. #'] = right_df['Conf. #'].astype(str)

            # Remove trailing dots from the Booking Number
            left_df = normalize_column(left_df.copy(), "Conf. #")
            right_df = normalize_column(right_df.copy(), "Conf. #")
            
            left_df_filtered = filter_columns(left_df)
            right_df_filtered = filter_columns(right_df)
            
            # Add Avatar column
            # left_df_filtered = addAvatarColumn(left_df_filtered)
            # right_df_filtered = addAvatarColumn(right_df_filtered)


            # Clear the placeholders to hide/minimize the original tables
            placeholder_left.empty()
            placeholder_right.empty()
            
            left_df_styled, right_df_styled = compare_dataframes(left_df_filtered, right_df_filtered)
            
            left_file_path = "RL_hotel.csv"  # Define the file path for the left DataFrame
            right_file_path = "RL_abtsolute.csv"  # Define the file path for the right DataFrame
            
            if right_df_styled is not None:
                rl_ABTS = f"<p style='color:Blue; font-size:20px; margin-bottom:0px; padding:0px;'>ABTSolute Rooming List<p><span style='color:#999999;'>Differences Highlighted in yellow</span>"
                st.markdown(rl_ABTS, unsafe_allow_html=True)

                # Hide identical rows
                hide_ABTSolute_rows_checkbox = st.checkbox("Hide identical rows", key="hide_ABTSolute_rows")
                right_df_styled = hide_identical_rows(hide_ABTSolute_rows_checkbox, right_df_styled, st.session_state['same_rows'])

                # load DF into streamlit container
                ABTSolute_df_height = min(len(right_df_styled.data) * 44, 300)
                st.dataframe(right_df_styled, use_container_width=True,  height=ABTSolute_df_height) # set dataframe attributes (height, width, etc.)

                # Render Avatar Column
                
                # st.data_editor(
                #    right_df_styled,
                #    column_config={
                #        "Avatar": st.column_config.ImageColumn("Image"),
                #        "Last Name" : "Last Name",
                #        "First Name" : "First Name",
                #        "Arrival" : "Arrival",
                #        "Departure" : "Departure",
                #        "Conf. #" : st.column_config.NumberColumn("Conf. #", format="%d") 
                #    },
                #    use_container_width=True
                # )

            if left_df_styled is not None:
                rl_hotel = f"<br><p style='color:Red; font-size:20px; margin-bottom:0px; padding:0px;'>Hotel Rooming List<p><span style='color:#999999;'>Differences Highlighted in yellow</span>"
                st.markdown(rl_hotel, unsafe_allow_html=True)
                
                # Hide identical rows
                hide_hotel_rows_checkbox = st.checkbox("Hide identical rows", key="hide_hotel_rows")
                left_df_styled = hide_identical_rows(hide_hotel_rows_checkbox, left_df_styled, st.session_state['same_rows'])
                
                # load DF into streamlit container
                rl_hotel_df_height = min(len(left_df_styled.data) * 44, 300)  # calculate the height based on the number of rows
                st.dataframe(left_df_styled, use_container_width=True, height=rl_hotel_df_height) # set dataframe attributes (height, width, etc.)

           

                # Render Avatar Column
                
                # st.data_editor(
                #    left_df_styled,
                #    column_config={
                #        "Avatar": st.column_config.ImageColumn("Image"),
                #        "Last Name" : "Last Name",
                #        "First Name" : "First Name",
                #        "Arrival" : "Arrival",
                #        "Departure" : "Departure",
                #        "Conf. #" : st.column_config.NumberColumn("Conf. #", format="%d") 
                #    },
                #    use_container_width=True
                # )
                
                
                
    
            # Using Hotel column-filtered Rooming List 
            update_df_in_session_only(left_df_filtered, "right", right_file_path)

        # Commented out as there is currently no need to render tables prior to comparison
        # that is prior to selecting a second table for comparison
        # I myself like to use triple-quotes to comment out blocks of code while I’m iterating on my app, so I typically do this:
        # Assigning it to a variable means that it won’t magically be printed
        # Assigning it to _ (a standard throw-away variable) means that my auto-linters won’t complain about a variable that I’m not using
        
    _="""
    else:
        # Only show expanders (with the option to load and display the DFs) if no differences are displayed
        with placeholder_left.container():
            if left_df is not None:
                st.markdown("**Hotel Rooming List Original Table**")
                st.dataframe(left_df, use_container_width=True)
        
        with placeholder_right.container():
            if right_df is not None:
                st.markdown("**ABTSolute Rooming List Original Table**")
                st.dataframe(right_df, use_container_width=True)
    """



