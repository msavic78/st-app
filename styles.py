# Description: This file contains the CSS styles for the Streamlit app. 
# The styles are defined as functions that return CSS strings. 
# The functions are then imported and used in the main Streamlit app script.

def get_css():
    return """
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
    """