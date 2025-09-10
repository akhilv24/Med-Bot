import streamlit as st
import pdfplumber
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def extract_health_data_from_pdf(pdf_text):
    # Dummy regex-based extraction (customize this to your report format)
    data = {"Age": int(re.search(r"Age[:\s]+(\d+)", pdf_text).group(1)) if re.search(r"Age[:\s]+(\d+)", pdf_text) else None,"BMI": float(re.search(r"BMI[:\s]+([\d.]+)", pdf_text).group(1)) if re.search(r"BMI[:\s]+([\d.]+)", pdf_text) else None,"Blood Pressure": int(re.search(r"Blood Pressure[:\s]+(\d+)", pdf_text).group(1)) if re.search(r"Blood Pressure[:\s]+(\d+)", pdf_text) else None,"Cholesterol": int(re.search(r"Cholesterol[:\s]+(\d+)", pdf_text).group(1)) if re.search(r"Cholesterol[:\s]+(\d+)", pdf_text) else None,}
    return data

def show_health_dashboard():
    st.title("Health Report Stats Dashboard")

    uploaded_pdf = st.file_uploader("📄 Upload your medical report (PDF)", type="pdf")

    if uploaded_pdf:
        with pdfplumber.open(uploaded_pdf) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"

        st.text_area(" Extracted Text from Report", value=text, height=200)

        data_dict = extract_health_data_from_pdf(text)

        if all(value is not None for value in data_dict.values()):
            df = pd.DataFrame([data_dict])
            st.success("Report extracted successfully!")

            st.write("### 📋 Extracted Health Data")
            st.dataframe(df)

            # Plotting
            # Plotting
            st.write("### 📈 BMI Distribution")
            fig1, ax1 = plt.subplots()
            sns.histplot(df["BMI"], bins=10, stat="count", kde=False, ax=ax1)
            ax1.set_xlabel("BMI")
            ax1.set_ylabel("Count")
            st.pyplot(fig1)

            st.write("### 📈 Blood Pressure vs Age")
            fig2, ax2 = plt.subplots()
            sns.scatterplot(x=df["Age"], y=df["Blood Pressure"], size=df["Cholesterol"], legend=False, ax=ax2)
            st.pyplot(fig2)

            st.write("### Correlation Heatmap")
            fig3, ax3 = plt.subplots()
            sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax3)
            st.pyplot(fig3)
        else:
            st.warning("⚠️ Could not extract all required metrics. Please ensure your report contains Age, BMI, Blood Pressure, and Cholesterol in readable text.")
