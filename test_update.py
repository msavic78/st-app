import streamlit as st
import pandas as pd

# Initial DataFrame setup
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        'column1': [1, 2, 3],
        'column2': ['A', 'B', 'C']
    })

# Display the DataFrame
st.dataframe(st.session_state.df)

# User input to modify DataFrame
col1, col2 = st.columns(2)
with col1:
    new_value1 = st.text_input("Enter new value for column1", key='new_value1')
with col2:
    new_value2 = st.text_input("Enter new value for column2", key='new_value2')

row_to_update = st.number_input("Enter row index to update", min_value=0, max_value=len(st.session_state.df)-1, key='row_index')

# Update button
if st.button("Update DataFrame"):
    if new_value1:
        st.session_state.df.loc[row_to_update, 'column1'] = new_value1
    if new_value2:
        st.session_state.df.loc[row_to_update, 'column2'] = new_value2

    # Streamlit automatically re-renders components after session state changes
