# data_comparison.py
import streamlit as st



# Function to compare two DataFrames and highlight differences
# It returns two styled DataFrames with differences highlighted
# The way it works is by aligning the DataFrames by index and then comparing the values
# The index alignment ensures that the comparison is row-wise
# Index alignment is done using the 'align' method with 'outer' join
# The 'fill_value' parameter is used to fill missing values with a placeholder
# The placeholder is used to highlight differences in the final styled DataFrames
# The function also captures the actual DataFrame indices where differences occur

def compare_dataframes(df1, df2):
    # Ensure 'same_rows' is initialized in the session state
    if 'same_rows' not in st.session_state:
        st.session_state['same_rows'] = []

    try:
        if not df1.columns.equals(df2.columns):
            st.error("The files do not have the same format (columns differ).")
            return None, None
        else:

            # CORRECTLY ALIGN DATAFRAMES BY INDEX, FILLING MISSING VALUES WITH A PLACEHOLDER
            df1_aligned, df2_aligned = df1.align(df2, join='outer', axis=0, fill_value='Not in other df')

            # Convert DataFrames to strings to highlight differences and 
            # keep the original DataFrames (df1_aligned) for display
            df1_highlighted = df1_aligned.astype(str).copy()
            df2_highlighted = df2_aligned.astype(str).copy()

            differences = []

            for col in df1_aligned.columns:
                mask = df1_aligned[col].astype(str) != df2_aligned[col].astype(str)
                df1_highlighted.loc[mask, col] = '**' + df1_aligned[col].astype(str) + '**'
                df2_highlighted.loc[mask, col] = '**' + df2_aligned[col].astype(str) + '**'

                # Capture the actual DataFrame indices where differences occur
                indices = df1_aligned.index[mask].tolist()
                differing_values_df1 = df1_aligned.loc[mask, col].tolist()
                differing_values_df2 = df2_aligned.loc[mask, col].tolist()

                for idx, val1, val2 in zip(indices, differing_values_df1, differing_values_df2):
                    differences.append((idx, col, val1, val2))

            # Update the logic for detecting same rows to work with aligned DataFrames
            mask_same = (df1_aligned == df2_aligned).all(axis=1)
            same_indices = df1_aligned.index[mask_same].tolist()
            st.session_state['same_rows'] = same_indices

            display_differences(differences)
            
            # Function to apply cell-specific styling
            def apply_cell_highlight_style(cell_value):
                if '**' in cell_value:
                    return 'background-color: red; color:#333333 !important;'
                return ''

            # Function to apply row-specific styling based on cell condition
            def apply_row_highlight_style(row):
                # Check if any cell in the row has '**'
                if any('**' in str(cell) for cell in row):
                    return ['background-color: #fffbb8;color:#333333;' if '**' not in cell else 'background-color: yellow; color:#000000;' for cell in row]
                else:
                    return ['' for _ in row]

            # Applying styling
            df1_styled = df1_highlighted.style.applymap(apply_cell_highlight_style).apply(apply_row_highlight_style, axis=1)
            df2_styled = df2_highlighted.style.applymap(apply_cell_highlight_style).apply(apply_row_highlight_style, axis=1)
            
            return df1_styled, df2_styled

    except Exception as e:
         # Log the exception if needed
        st.error(f"An error occurred during comparison: {e}. Please check the data formats and try again.")
        st.stop()  # Stop execution here
        return None, None

# Booking Number Column Normalization
def normalize_column(df, column_name):

    # Set column type to string and, 
    df[column_name] = df[column_name].astype(str)
    df[column_name] = df[column_name].astype(str)
    
    # Remove trailing dots
    df[column_name] = df[column_name].apply(lambda x: x.split('.')[0])
    return df


def display_differences(differences):
    """
    Formats and displays the differences between dataframes in a Streamlit text element, aggregating all column discrepancies per row.

    Parameters:
    differences (list of tuples): List containing tuples with (row_idx, col, val1, val2)
                                  where each tuple represents a difference found between two dataframes.
    """
    if differences:  # Check if there are any differences
        # Aggregate differences by row
        row_diffs = {}
        for row_idx, col, val1, val2 in differences:
            if row_idx not in row_diffs:
                row_diffs[row_idx] = []
            row_diffs[row_idx].append(f"{col}: {val1} <b style='color:#333333;'>vs.</b> {val2}")

        # Format each row's differences
        differences_str = "<br>".join(
            f"<span style='color: #BC8313;'><b style='color:red;'>Row {row_idx}</b>: " +
            " <b style='color:#000000;'>|</b> ".join(diffs) + "</span>" for row_idx, diffs in row_diffs.items()
        )
        
        with st.expander("Show/Hide rooming list discrepancies"):
            st.warning('Discrepancies Found', icon="⚠️")
            st.markdown(f"<p style='zborder:1px solid #eeeeee; border-radius:10px; padding:10px;background-color:#FFFCE7'>{differences_str}</p>", unsafe_allow_html=True)
    else:
        st.success('No Discrepancies Found', icon="✅")

def hotelRL_highlighter(row):
    style_lt = "background-color: #ffffff; color: #fcc0c0;"
    return [style_lt for _ in row]

def ABTSRL_highlighter(row):
    style_lt = "background-color: #ffffff; color: #c0c6fc;"
    return [style_lt for _ in row]


def FinalRL_highlighter(row):
    style_lt = "background-color: #ffffff; color: #710087;"
    return [style_lt for _ in row]
    
    


#def color_negative_red(val):
#    color = 'red' if val < 0 else 'black'
#    return 'color: %s' % color

