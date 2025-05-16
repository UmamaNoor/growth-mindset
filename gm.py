
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# ---- PAGE CONFIGURATION ----
st.set_page_config(page_title="Data Sweeper Pro", layout="wide")



# ---- HEADER ----
st.markdown("""
    <div class="header-container">
        <h1>🌐 Data Sweeper Pro</h1>
        <p>Advanced Data Cleaning, Transformation & Visualization Tool</p>
        <small>Crafted with ❤️ by Umama Noor</small>
    </div>
""", unsafe_allow_html=True)

# ---- FILE UPLOAD SECTION ----
st.markdown("## 📂 Upload Your Files")
uploaded_files = st.file_uploader(
    "Choose CSV, Excel, or ODS files", type=["csv", "xlsx", "ods"], accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file, engine="openpyxl")
            elif file_ext == ".ods":
                df = pd.read_excel(file, engine="odf")
            else:
                st.error(f"Unsupported file type: {file_ext}")
                continue

            st.markdown(f"### 📄 {file.name}")
            st.write(f"**File Size:** {file.size / 1024:.2f} KB")
            st.write("#### 🔍 Data Preview")
            st.dataframe(df.head())

            # Data Cleaning Options
            st.write("### 🧹 Data Cleaning Options")
            if st.checkbox(f"Enable Cleaning for `{file.name}`"):
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates Removed!")

                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing Values Filled!")

                if st.button(f"Drop Rows with Missing Values from {file.name}"):
                    df.dropna(inplace=True)
                    st.success("Rows with Missing Values Dropped!")

                if st.button(f"Convert Column Names to Lowercase for {file.name}"):
                    df.columns = df.columns.str.lower()
                    st.success("Column Names Converted to Lowercase!")

            # Column Selection
            st.write("### 🎯 Choose Columns to Keep")
            selected_columns = st.multiselect(f"Select Columns for `{file.name}`", df.columns, default=list(df.columns))
            df = df[selected_columns]

            # Visualization
            st.write("### 📊 Data Visualization")
            if st.checkbox(f"Show Visualization for `{file.name}`"):
                numeric_columns = df.select_dtypes(include="number").columns.tolist()

                if len(numeric_columns) >= 2:
                    selected_chart_columns = st.multiselect(f"Select Columns for Chart - `{file.name}`", numeric_columns, default=numeric_columns[:2])
                    st.bar_chart(df[selected_chart_columns])
                else:
                    st.warning("Not enough numeric columns for visualization")

            # File Conversion
            st.write("### 🔄 Convert & Download File")
            conversion_type = st.radio(f"Convert `{file.name}` to:", ["CSV", "Excel"], key=file.name)

            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_extension = "csv"
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False, engine="xlsxwriter")
                file_extension = "xlsx"
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"Download {file.name.split('.')[0]}_cleaned.{file_extension}",
                data=buffer,
                file_name=f"{file.name.split('.')[0]}_cleaned.{file_extension}",
                mime=mime_type
            )

        except Exception as e:
            st.error(f"Error processing {file.name}: {e}")
