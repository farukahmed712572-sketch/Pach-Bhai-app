import streamlit as st
import pandas as pd

st.set_page_config(page_title="Panch Bhai Electronics", layout="wide")

st.title("📊 Panch Bhai Electronics Inventory App")

# Load Excel file
file_path = "Panch_Bhai_AppSheet.xlsx"

@st.cache_data
def load_excel(path):
    return pd.ExcelFile(path)

xls = load_excel(file_path)

sheet_choice = st.sidebar.radio("Select Language / ভাষা বাছাই করুন", xls.sheet_names)
df = pd.read_excel(file_path, sheet_name=sheet_choice)

st.write("### Inventory Table")
st.dataframe(df, use_container_width=True)

# Add new product
st.write("### ➕ Add New Product")
with st.form("add_product"):
    cols = st.columns(len(df.columns))
    new_data = []
    for i, col in enumerate(df.columns):
        new_data.append(cols[i].text_input(f"{col}"))
    submitted = st.form_submit_button("Add Product")
    if submitted:
        df.loc[len(df)] = new_data
        with pd.ExcelWriter(file_path, mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=sheet_choice, index=False)
        st.success("✅ Product added successfully! Please refresh.")
