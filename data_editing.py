# data_editing.py
import streamlit as st

# Function to display a DataFrame and allow cell editing
def display_and_edit_dataframe(df, df_key, file_path):
    
    # Use st.columns to place inputs on the same row
    col1, col2, col3 = st.columns(3)  # Create three columns
    with col1:
        row_to_edit = st.number_input("Enter the row index to edit:", min_value=0, max_value=len(df)-1, key=f"row_{df_key}")
    with col2:
        column_to_edit = st.selectbox("Select the column to edit:", df.columns, key=f"col_{df_key}")
    with col3:
        new_value = st.text_input("Enter the new value:", key=f"new_{df_key}")
    
    # Save Changes button in a new row below
    if st.button("Save Changes", key=f"save_{df_key}"):
        try:
            current_value = df.at[row_to_edit, column_to_edit]
            new_value_converted = type(current_value)(new_value)
            df.at[row_to_edit, column_to_edit] = new_value_converted
            st.success(f"Value updated successfully: {new_value_converted}")
            
            # Save the modified DataFrame to a file
            df.to_csv(file_path, index=False)
            st.success(f"Changes saved to file: {file_path}")
        except Exception as e:
            st.error(f"Failed to update the value or save the file. Error: {e}")


