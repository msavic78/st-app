import streamlit as st

# Function to display a DataFrame and allow cell editing
def update_df_in_session_only(df, df_key, file_path):
    if 'df_changes' not in st.session_state:
        st.session_state.df_changes = df

    rl_final = f"<p style='color:Green; font-size:20px; margin-bottom:0px; padding:0px;'>Final Rooming List<p><span style='color:#999999;'>Use this Table to Edit & Update Values. Once done, donwload as CSV (hover over the right table corner for more details)</span>"
    st.markdown(rl_final, unsafe_allow_html=True)
    st.dataframe(st.session_state.df_changes, use_container_width=True, height=200)

    # Use st.columns to place inputs on the same row
    col1, col2, col3 = st.columns(3)  # Create three columns
    with col1:
        row_to_edit = st.number_input("Enter the row index to edit:", min_value=0, max_value=len(df)-1, key=f"row_{df_key}")
    with col2:
        column_to_edit = st.selectbox("Select the column to edit:", df.columns, key=f"col_{df_key}")
    with col3:
        new_value = st.text_input("Enter the new value:", key=f"new_{df_key}")

    if st.button("Apply Changes", key=f"apply_{df_key}"):
        try:
            current_value = st.session_state.df_changes.at[row_to_edit, column_to_edit]
            new_value_converted = type(current_value)(new_value)
            st.session_state.df_changes.at[row_to_edit, column_to_edit] = new_value_converted
            st.success(f"Value updated successfully: {new_value_converted}")
            st.experimental_rerun()

        except Exception as e:
            st.error(f"Failed to update the value. Error: {e}")

