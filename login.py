from datetime import datetime
import re
from flask import request
import os
import streamlit as st


# Regex pattern for validating an email
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def setClientEmail(email):
    st.session_state['client_email'] = email

def getClientEmail():
    current_time = datetime.now().strftime('%Y-%m-%d %H-%M-%S')  # Format datetime as string
    return st.session_state['client_email'] + ' - ' + current_time + ' '

# Function to check if the login credentials are correct
def check_login(username, password):

    # Define admin credentials
    admin_username = "admin@abtscs.com"
    # admin_password = "2000Albatros"
    admin_password = "a"

    # Define client credentials
    # client_password = "RoomSync2024!!"
    client_password = "a"
    
    # If Admin Login
    if username == admin_username and password == admin_password:
        return True, "admin"
 
    # If Client Login
    if password == client_password:
        return True, "client"

    # if no credentials were provided
    return False, None

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
        username = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button(label="Login")

        # What?
        form_submitted = login_button

        if 'form_submitted' not in st.session_state:
             st.session_state["form_submitted"] = False
        if form_submitted:
             st.session_state["form_submitted"] = True
        
        if st.session_state["form_submitted"]:

            # Email validation message
            if is_valid_email(username):

                login_successful, logged_in_as_user_type = check_login(username, password)
                
                if (login_successful):
                    
                    st.session_state['logged_in'] = True  # Set a session state variable to indicate successful login
                    st.session_state['user_type'] = logged_in_as_user_type # Store user type in session state
                    # If login is specifically a client, log the username
                    if logged_in_as_user_type == "client":

                        # Save client email to a session that can be distributed to other classes
                        setClientEmail(username)    

                        # Get the IP address
                        if 'client_ip' not in st.session_state:
                            st.session_state['client_ip'] = get_client_ip() 
                            client_ip = st.session_state['client_ip']

                        log_client_login(username, client_ip) 
                    
                    st.experimental_rerun()  # This forces the script to rerun, immediately reflecting the login state

                else:
                    st.error("Login Failed. Please check your credentials.")
                    return False
            
            # Reject if username is not an email
            else:
                st.error("This is not a valid email. Please enter a valid email address.")


# Function to log client logins
def log_client_login(username, client_ip):
    # Get the script's directory (application root)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the logs directory if it doesn't exist
    logs_dir = os.path.join(current_dir, 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    # Log file path
    log_file_path = os.path.join(logs_dir, 'client_logins.log')

    # Open the file in append mode and write the log entry
    with open(log_file_path, 'a') as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} - Client login: {username} (IP: {client_ip})\n")

def get_client_ip():
    try: 
        # Check for forwarded IP if behind proxy/load balancer
        if 'X-Forwarded-For' in request.headers:
            return request.headers['X-Forwarded-For'].split(',')[0]
        else:
            return request.remote_addr
    except:
        return None
    
def is_valid_email(email):
    #Check if the provided string matches the email regex pattern.
    return re.match(EMAIL_REGEX, email) is not None
    

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