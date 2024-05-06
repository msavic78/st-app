# data_comparison.py
import streamlit as st

# Find a way to hide/show dataframe rows that are not different by clicking a button
# Add #EEEEEE to every second row in the dataframe

def compare_dataframes(df1, df2):
    if not df1.columns.equals(df2.columns):
        st.error("The files do not have the same format (columns differ).")
        return None, None
    else:
        # Highlight differences
        df1_highlighted = df1.copy().astype(str)
        df2_highlighted = df2.copy().astype(str)

        differences = []
        
        for col in df1.columns:
            mask = df1[col].astype(str) != df2[col].astype(str)
            df1_highlighted.loc[mask, col] = '**' + df1[col].astype(str) + '**'
            df2_highlighted.loc[mask, col] = '**' + df2[col].astype(str) + '**'

            # Capture the actual DataFrame indices where differences occur
            indices = df1.index[mask].tolist()
            differing_values_df1 = df1.loc[mask, col].tolist()
            differing_values_df2 = df2.loc[mask, col].tolist()

            for idx, val1, val2 in zip(indices, differing_values_df1, differing_values_df2):
                differences.append((idx, col, val1, val2))

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
        df1_styled = df1_highlighted.style.applymap(apply_cell_highlight_style).apply(hotelRL_highlighter).apply(apply_row_highlight_style, axis=1)
        df2_styled = df2_highlighted.style.applymap(apply_cell_highlight_style).apply(ABTSRL_highlighter).apply(apply_row_highlight_style, axis=1)
        
        return df1_styled, df2_styled

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
    Formats and displays the differences between dataframes in a Streamlit text element.

    Parameters:
    differences (list of tuples): List containing tuples with (row_idx, col, val1, val2)
                                  where each tuple represents a difference found between two dataframes.
    """
    if differences:  # Check if there are any differences
        differences_str = "<br>".join(f"<span style='color: #BC8313;'><b style='color:red;'>Row {row_idx}</b>, {col}: {val1} vs {val2}</span>" 
                                    for row_idx, col, val1, val2 in differences)
        
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

