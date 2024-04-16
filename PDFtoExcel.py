import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from tabula import read_pdf

import os

# Set JAVA_HOME to your JDK installation path
os.environ["JAVA_HOME"] = "C:\\Program Files\\Java\\jdk-22"

# Add the bin directory of the JDK to PATH
os.environ["PATH"] = "C:\\Program Files\\Java\\jdk-22\\bin" + os.pathsep + os.environ["PATH"]


def download_pdf(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError if the response is not 200
        return BytesIO(response.content)
    except requests.HTTPError as e:
        st.error(f"Failed to download file: {e}")
        return None

def pdf_to_dataframe(source, is_url=False):
    try:
        if is_url:
            pdf_file = download_pdf(source)
            if pdf_file is None:  # Early return if the PDF could not be downloaded
                return None
        else:
            pdf_file = source.getvalue()
        
        tables = read_pdf(BytesIO(pdf_file), pages='all', multiple_tables=True, stream=True)
        if not tables:
            st.warning("No tables found in the PDF.")
            return None
        
        df = pd.concat(tables, ignore_index=True)
        return df
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit UI
st.title("PDF to Excel/CSV Converter")

pdf_file = st.file_uploader("Upload your PDF file", type=["pdf"])
pdf_url = st.text_input("...Or enter a PDF URL")

if st.button("Convert PDF"):
    if pdf_file is not None:
        df = pdf_to_dataframe(pdf_file)
    elif pdf_url:
        df = pdf_to_dataframe(pdf_url, is_url=True)
    else:
        st.error("Please upload a file or enter a URL.")

    if df is not None:
        if df is not None:
            st.write(df)
            
            # Convert the DataFrame to Excel and then get the result as bytes for Excel
            output_excel = BytesIO()
            with pd.ExcelWriter(output_excel, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            output_excel.seek(0)

            # Download button for Excel
            st.download_button(label="Download Excel", data=output_excel.read(), file_name="table.xlsx", mime="application/vnd.ms-excel")
            
            # Convert the DataFrame to CSV and get the result as bytes
            output_csv = BytesIO()
            df.to_csv(output_csv, index=False)
            output_csv.seek(0)

            # Download button for CSV
            st.download_button(label="Download CSV", data=output_csv.read(), file_name="table.csv", mime="text/csv")



