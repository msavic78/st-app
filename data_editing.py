import base64
from io import BytesIO
import streamlit as st
from PIL import Image
#from data_comparison import FinalRL_highlighter

# Function to display a DataFrame and allow cell editing
def update_df_in_session_only(df, df_key, file_path):
    
    if 'df_changes' not in st.session_state:
        st.session_state.df_changes = df

    #st.session_state.df_changes = st.session_state.df_changes.style.apply(FinalRL_highlighter)

    rl_final = f"<p style='color:Green; font-size:20px; margin-bottom:0px; padding:0px;'>Final Rooming List: <span style='color:#710087;'><b>Edit Here</b></span><p><span style='color:#999999;'>Use this Table to Edit & Update Values. Once done, donwload as CSV (hover over the right table corner for more details)</span>"
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
            #st.session_state.df_changes = st.session_state.df_changes.style.apply(FinalRL_highlighter)
            st.success(f"Value updated successfully: {new_value_converted}")
            st.experimental_rerun()

        except Exception as e:
            st.error(f"Failed to update the value. Error: {e}")

def addAvatarColumn(df):
    
    new_column_name = 'Avatar'
    num_rows = len(df)
    
    image_path = 'https://picsum.photos/id/338/100/100'
    avatar = [image_path for _ in range(num_rows)]
    df.insert(0, new_column_name, avatar)

    return df
    
    # Desired size of the images
    # desired_width = 20  # Adjust as needed
    # desired_height = 20  # Adjust as needed

    # Load the specific image
    # image_path = r"D:\ProjectBackups\ABTS\Apps\Roomsync\st-app\no_portrait_image.png"
    #original_image = Image.open(image_path)

    # Resize the Image
    #resized_image = resize_image(original_image, desired_width, desired_height)

    ## new_column_data = [image] * num_rows
    # new_column_data = [resized_image for _ in range(num_rows)]

    # html_image = pil_to_html(resized_image)
    # df['Avatar'] = html_image



# Function to resize a single image
def resize_image(image, width, height):
    return image.resize((width, height), Image.Resampling.LANCZOS)

# TO-DO
# @st.cache_data
def pil_to_html(pil_img):
    buffered = BytesIO()
    pil_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f'<img src="data:image/png;base64,{img_str}" />'

def path_to_image_html(path):
    return '<img src="' + path +'" width="60" >'



