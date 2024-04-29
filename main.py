import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

from login import show_login_form

# Compare Dataframes (data_comparison.py)
from data_comparison import compare_dataframes
from data_comparison import normalize_column

# Update Table Values Bar
from data_editing import update_df_in_session_only

# Import filter function for df column cleanup
from data_loading import filter_columns

# Import Avatar column
from data_editing import addAvatarColumn

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_type'] = None  # Initialize user type in session state

# Show login form if not logged in, otherwise show the main application
if not st.session_state['logged_in']: # correct syntax for NOT
    show_login_form()
else:

    if st.session_state['user_type'] == "Viewer":

        # Load Data (data_loading.py)
        from data_loading import load_csv

        # Adjusted Main App to conditionally display tables
        title=f"<h3 style='color:#3C8595;'>ABTS <span style='color:#333333;'>RoomSync</span></h3>"
        st.markdown(title, unsafe_allow_html=True)
        
        rlv = f"<p style='font-size:20px; margin-top:-20px; margin-bottom:-10px; padding:0px;'>Rooming List Validation</p><hr>"
        st.markdown(rlv, unsafe_allow_html=True)

        # Create placeholders for the original dataframes
        placeholder_left = st.empty()

        # Load dataframes without displaying them immediately
        left_file = st.file_uploader("Upload Hotel Rooming List", key="left")

        left_df = load_csv(left_file, "Left")

    
    elif st.session_state['user_type'] == "Admin":

         # Load Data (data_loading.py)
        from data_loading import load_csv

        header = st.container()
        title=f"<h3 style='color:#3C8595;'>ABTS <span style='color:#333333;'>RoomSync</span></h3>"
        header.write(title, unsafe_allow_html=True)
        rlv = f"<p style='font-size:20px; margin-top:-20px; margin-bottom:-10px; padding:0px;'>Rooming List Validation</p>"
        header.write(rlv, unsafe_allow_html=True)
        header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

        ### Custom CSS for the sticky header
        st.markdown(
            """
        <style>
            div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
                position: sticky;
                top: 2.875rem;
                background-color: white;
                z-index: 999;
            }
            .fixed-header {
                border-bottom: 1px solid #cccccc;
            }
        </style>
            """,
            unsafe_allow_html=True
        )
        
         # Initialize session state if necessary
        if "expander_open" not in st.session_state:
            st.session_state.expander_open = True  # Initial state as open

        file_upload_expander = st.expander("Click to view/hide upload options", expanded=st.session_state.expander_open)

        with file_upload_expander:
            # Load dataframes without displaying them immediately
            left_file = st.file_uploader("Upload Hotel Rooming List", key="left")
            right_file = st.file_uploader("Upload ABTSolute Rooming List", key="right")
        
        left_df = load_csv(left_file, "Left")
        right_df = load_csv(right_file, "Right")


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

            st.session_state.expander_open = False  # Update state to closed

            # Clear the placeholders to hide/minimize the original tables
            placeholder_left.empty()
            placeholder_right.empty()
            
            left_df_styled, right_df_styled = compare_dataframes(left_df_filtered, right_df_filtered)
            
            left_file_path = "RL_hotel.csv"  # Define the file path for the left DataFrame
            right_file_path = "RL_abtsolute.csv"  # Define the file path for the right DataFrame

            if left_df_styled is not None:
                rl_hotel = f"<br><p style='color:Red; font-size:20px; margin-bottom:0px; padding:0px;'>Hotel Rooming List<p><span style='color:#999999;'>Differences Highlighted in yellow</span>"
                st.markdown(rl_hotel, unsafe_allow_html=True)
                st.dataframe(left_df_styled, use_container_width=True)

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
                
                
            if right_df_styled is not None:
                rl_ABTS = f"<p style='color:Blue; font-size:20px; margin-bottom:0px; padding:0px;'>ABTSolute Rooming List<p><span style='color:#999999;'>Differences Highlighted in yellow</span>"
                st.markdown(rl_ABTS, unsafe_allow_html=True)
                st.dataframe(right_df_styled, use_container_width=True)

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


