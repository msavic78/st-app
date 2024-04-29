# data_comparison.py
import streamlit as st

def compare_dataframes(df1, df2):
    if not df1.columns.equals(df2.columns):
        st.error("The files do not have the same format (columns differ).")
        return None, None
    else:
        # Highlight differences
        df1_highlighted = df1.copy().astype(str)
        df2_highlighted = df2.copy().astype(str)
        
        for col in df1.columns:
            mask = df1[col].astype(str) != df2[col].astype(str)
            df1_highlighted.loc[mask, col] = '**' + df1[col].astype(str) + '**'
            df2_highlighted.loc[mask, col] = '**' + df2[col].astype(str) + '**'
        
        # Function to apply cell-specific styling
        def apply_cell_highlight_style(cell_value):
            if '**' in cell_value:
                return 'background-color: yellow'
            return ''

        # Function to apply row-specific styling based on cell condition
        def apply_row_highlight_style(row):
            # Check if any cell in the row has '**'
            if any('**' in str(cell) for cell in row):
                return ['background-color: #fffbb8' if '**' not in cell else 'background-color: yellow' for cell in row]
            else:
                return ['' for _ in row]

        # Applying styling
        df1_styled = df1_highlighted.style.applymap(apply_cell_highlight_style).apply(hotelRL_highlighter).apply(apply_row_highlight_style, axis=1)
        df2_styled = df2_highlighted.style.applymap(apply_cell_highlight_style).apply(ABTSRL_highlighter).apply(apply_row_highlight_style, axis=1)
        
        return df1_styled, df2_styled


def normalize_column(df, column_name):

    # Set column type to string and, 
    df[column_name] = df[column_name].astype(str)
    df[column_name] = df[column_name].astype(str)
    
    # Remove trailing dots
    df[column_name] = df[column_name].apply(lambda x: x.split('.')[0])
    return df

def hotelRL_highlighter(row):
    style_lt = "background-color: #ffffff; color: #8a0700;"
    return [style_lt for _ in row]

def ABTSRL_highlighter(row):
    style_lt = "background-color: #ffffff; color: #00008a;"
    return [style_lt for _ in row]


def FinalRL_highlighter(row):
    style_lt = "background-color: #ffffff; color: #710087;"
    return [style_lt for _ in row]
    
    


#def color_negative_red(val):
#    color = 'red' if val < 0 else 'black'
#    return 'color: %s' % color

