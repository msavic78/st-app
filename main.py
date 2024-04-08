import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

from login import show_login_form

# Compare Dataframes (data_comparison.py)
from data_comparison import compare_dataframes

# Update Table Values Bar
from data_editing import update_df_in_session_only


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
                rl_hotel = f"<hr><p style='color:Red; font-size:20px; margin-bottom:0px; padding:0px;'>Hotel Rooming List<p><span style='color:#999999;'>Differences Highlighted in yellow</span>"
                st.markdown(rl_hotel, unsafe_allow_html=True)
                st.dataframe(left_df_styled, use_container_width=True)
                # Insert the editing functionality here for the left table
                #update_df_in_session_only(left_df, "left", left_file_path)
                
                
            if right_df_styled is not None:
                rl_ABTS = f"<p style='color:Blue; font-size:20px; margin-bottom:0px; padding:0px;'>ABTSolute Rooming List<p><span style='color:#999999;'>Differences Highlighted in yellow</span>"
                st.markdown(rl_ABTS, unsafe_allow_html=True)
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



