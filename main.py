import pandas as pd
import streamlit as st
import os
from io import BytesIO

st.set_page_config(page_title='🚀 ConvertEase', layout="centered")

st.sidebar.title("🔄 ConvertEase")
uploaded_files = st.sidebar.file_uploader('Upload CSV or Excel files', type=['csv', 'xlsx'], accept_multiple_files=True)

st.title('🔄 ConvertEase: Seamless CSV & Excel Conversion with Smart Insights! 📊')

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"Error reading file {file.name}: {e}")
            continue

        st.subheader(f"📂 File: {file.name}")
        st.write(f"📏 Size: {file.size / 1024:.2f} KB")

        st.subheader("📊 Data Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Show Data Summary for {file.name}"):
            st.write(df.describe())
            st.write("Missing Values per Column:")
            st.write(df.isnull().sum())

        st.subheader("🛠️ Data Cleaning Options")
    if st.checkbox(f"🧹 Clean data for {file.name}"):
        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"🗑️ Remove Duplicates from {file.name}"):
                df.drop_duplicates(inplace=True)
                st.success("✅ Duplicates Removed!")

        with col2:
            if st.button(f"📊 Fill Missing Values for {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("✅ Missing Values have been Filled!")

        selected_columns = st.multiselect(f"Select columns for {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        
        st.subheader("📈 Data Visualization")
        chart_type = st.selectbox("Choose a chart type", ["Bar Chart", "Line Chart", "Histogram"], key=file.name)
        num_cols = df.select_dtypes(include='number').columns
        if not num_cols.empty:
            selected_col = st.selectbox("Select a numeric column", num_cols, key=file.name + "_chart")
            if chart_type == "Bar Chart":
                st.bar_chart(df[selected_col])
            elif chart_type == "Line Chart":
                st.line_chart(df[selected_col])
            elif chart_type == "Histogram":
                st.write(df[selected_col].hist(bins=20))
        else:
            st.warning("No numeric columns available for visualization.")

        st.subheader("🔄 File Conversion")
        conversion_type = st.radio(f"Convert {file.name} to:", ['CSV', 'Excel', 'JSON'], key=f"{file.name}_conversion")
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            elif conversion_type == "JSON":
                df.to_json(buffer, orient='records', lines=True)
                file_name = file.name.replace(file_ext, ".json")
                mime_type = "application/json"
            buffer.seek(0)
            st.download_button(
                label=f"Download {file_name}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
            st.success(f"🚀 {file_name} is ready!")
