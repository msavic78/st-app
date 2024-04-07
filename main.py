import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

from login import show_login_form

# Compare Dataframes (data_comparison.py)
from data_comparison import compare_dataframes

# Update Table Values Bar
from data_editing import update_df_in_session_only


st.session_state['logged_in'] = True
st.session_state['user_type'] = "Admin"
st.session_state['Edited'] = False

# Initialize session state
if 'logged_in' not in st.session_state:
    # st.session_state['logged_in'] = False
    # st.session_state['user_type'] = None  # Initialize user type in session state

    st.session_state['logged_in'] = True
    st.session_state['user_type'] = "Admin"  # Initialize user type in session state

 


# Show login form if not logged in, otherwise show the main application
if 'logged_in' not in st.session_state: # correct syntax for NOT
    show_login_form()
else:

    if st.session_state['user_type'] == "Viewer":

        # Load Data (data_loading.py)
        from data_loading import load_csv

        # Adjusted Main App to conditionally display tables
        st.title("RoomSync - Rooming List Comparator")

        # Create placeholders for the original dataframes
        placeholder_left = st.empty()

        # Load dataframes without displaying them immediately
        left_file = st.file_uploader("Upload Hotel Rooming List", key="left")

        left_df = load_csv(left_file, "Left")

    
    elif st.session_state['user_type'] == "Admin":

         # Load Data (data_loading.py)
        from data_loading import load_csv

        # Adjusted Main App to conditionally display tables
        st.title("RoomSync - Rooming List Comparator")

        # Create placeholders for the original dataframes
        placeholder_left = st.empty()
        placeholder_right = st.empty()

        # Load dataframes without displaying them immediately
        left_file = st.file_uploader("Upload Hotel Rooming List", key="left")
        right_file = st.file_uploader("Upload ABTSolute Rooming List", key="right")
        
        left_df = load_csv(left_file, "Left")
        right_df = load_csv(right_file, "Right")

        

        # Compare and display differences if both dataframes exist and have the same format
        if left_df is not None and right_df is not None:
            # Clear the placeholders to hide/minimize the original tables
            placeholder_left.empty()
            placeholder_right.empty()
            
            left_df_styled, right_df_styled = compare_dataframes(left_df, right_df)
            
            left_file_path = "C:\Projects\ABTSolute\Guest List Comparison\RL_hotel.csv"  # Define the file path for the left DataFrame
            right_file_path = "C:\Projects\ABTSolute\Guest List Comparison\RL_abtsolute.csv"  # Define the file path for the right DataFrame

            if left_df_styled is not None:
                st.markdown("**Hotel Rooming List Differences Highlighted**")
                st.dataframe(left_df_styled, use_container_width=True)
                # Insert the editing functionality here for the left table
                #update_df_in_session_only(left_df, "left", left_file_path)
                
                
            if right_df_styled is not None:
                st.markdown("**ABTSolute Rooming List Differences Highlighted**")
                st.dataframe(right_df_styled, use_container_width=True)
                # Insert the editing functionality here for the right table
                # update_df_in_session_only(right_df, "right", right_file_path)

            #if 'df_changes' in st.session_state:
                #st.markdown("Updated Table")
                #st.dataframe(st.session_state.df_changes)
                
            update_df_in_session_only(left_df, "right", right_file_path)

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



