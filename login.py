import streamlit as st

# Function to check if the login credentials are correct
def check_login(username, password):
    # Define the correct credentials
    correct_username = "abts"
    correct_password = "abts"
    
    # Check if the entered credentials match the correct ones
    return username == correct_username and password == correct_password

# Check session state for login status (avoid Login button double click to submit)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Function to create and manage the login form
def show_login_form():
    with st.form(key='login_form'):
        
        # Adjusted Main App to conditionally display tables
        title=f"<h3 style='color:#3C8595;'>ABTS <span style='color:#333333;'>RoomSync</span></h3>"
        st.markdown(title, unsafe_allow_html=True)
        
        rlv = f"<p style='font-size:20px; margin-top:-20px; margin-bottom:-10px; padding:0px;'>Rooming List Validation</p><hr>"
        st.markdown(rlv, unsafe_allow_html=True)

        # Input elements
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        user_type = st.selectbox("User Type", ["Select", "Admin", "Viewer"], index=0)
        login_button = st.form_submit_button(label="Login")

        # 
        form_submitted = login_button
        if 'form_submitted' not in st.session_state:
             st.session_state["form_submitted"] = False
        if form_submitted:
             st.session_state["form_submitted"] = True
        
        if st.session_state["form_submitted"]:
            if user_type == "Select":
                 st.error("Please select a user type.")
            elif user_type != "Select" and check_login(username, password):
                st.session_state['logged_in'] = True  # Set a session state variable to indicate successful login
                st.session_state['user_type'] = user_type # Store user type in session state
                st.experimental_rerun()  # This forces the script to rerun, immediately reflecting the login state
            else:
                st.error("Login Failed. Please check your credentials.")
                return False



"""
DATABASE LOGIN (PENDING ABTSolute connection)

import streamlit as st
import pyodbc

# Function to create a database connection
def create_db_connection():
    # Replace these with your actual database connection details
    server = 'your_server'
    database = 'your_database'
    username = 'your_username'
    password = 'your_password'
    driver= '{ODBC Driver 17 for SQL Server}'  # Adjust driver version as needed
    cnxn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    return cnxn

# Function to check if the login credentials are correct
def check_login(username, password):
    cnxn = create_db_connection()
    cursor = cnxn.cursor()
    query = "SELECT COUNT(1) FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    return result[0] == 1

# Function to create and manage the login form
def show_login_form():
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        user_type = st.selectbox("User Type", ["Select", "Admin", "Viewer"], index=0)
        login_button = st.form_submit_button(label="Login")
        
        if login_button and user_type != "Select":
            if check_login(username, password):
                st.session_state['logged_in'] = True  # Set a session state variable to indicate successful login
                return True
            else:
                st.error("Login Failed. Please check your credentials.")
                return False
        elif login_button:
            st.error("Please select a user type.")

"""