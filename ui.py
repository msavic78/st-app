import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def display_title():
    title=f"<h3 style='color:#3C8595;'>ABTS <span style='color:#333333;'>RoomSync</span></h3>"
    st.markdown(title, unsafe_allow_html=True)

def display_rooming_list_validation():
    rlv = f"<p style='font-size:20px; margin-top:-20px; margin-bottom:-10px; padding:0px;'>Rooming List Validation</p><hr>"
    st.markdown(rlv, unsafe_allow_html=True)

def display_hotel_rooming_list():
    rl_hotel = f"<br><p style='color:Red; font-size:20px; margin-bottom:0px; padding:0px;'>Hotel Rooming List<p>"
    st.markdown(rl_hotel, unsafe_allow_html=True)

def display_header():

    header = st.container()
    title=f"<h3 style='color:#3C8595;'>ABTS <span style='color:#333333;'>RoomSync</span></h3>"
    header.write(title, unsafe_allow_html=True)
    rlv = f"<p style='font-size:20px; margin-top:-20px; margin-bottom:-10px; padding:0px;'>Rooming List Validation</p>"
    header.write(rlv, unsafe_allow_html=True)
    header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

    # Create two columns
    col1, col2 = st.columns([11,1])

    # Log out button
    logout_clicked = col2.button("Log out", key="logout_button")

    # If the hidden Streamlit button was clicked, clear the session state and rerun the app
    if logout_clicked:
        st.session_state.clear()
        st.experimental_rerun()
        

def change_label_style(label, font_size, font_color):
    html = f"""
    <script>
        var elems = window.parent.document.querySelectorAll('p');
        var elem = Array.from(elems).find(x => x.innerText == '{label}');
        elem.style.fontSize = '{font_size}';
        elem.style.color = '{font_color}';
        elem.style.fontWeight = 'bold';
        
    </script>
    """
    st.components.v1.html(html)



 # Uses streamlit-extras to style the log out button
 # Should remain comme nted out until the issue with button 
 # not applying when button is nested in column 
 # (col2.button vs. st.button) is resolved
    
    with stylable_container(
        "green",
        css_styles="""
        button {
            background-color: #3C8595;
            color: white;
            border-color: white;
        }""",
    ):
        logout_clicked = st.button("Log out", key="logout_button")