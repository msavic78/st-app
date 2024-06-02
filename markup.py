# markup.py

import streamlit as st

# Check which pages actually use this (i.e. login and main.py do not use this)
def init_markup():
    header = st.container()
    title=f"<h3 style='color:#3C8595;'>ABTS <span style='color:#333333;'>RoomSynce</span></h3>"
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

