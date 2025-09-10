import streamlit as st
import pandas as pd

@st.cache_data
def load_medicine_data():
    return pd.read_csv("medicine_dataset.csv")

def fetch_medicine_info(medicine_df, medicine_name):
    for _, row in medicine_df.iterrows():
        if row["Name"].lower() == medicine_name.lower():
            return f"""
            **Medic-Bot:**

            • **Name**: {row['Name']}  
            • **Category**: {row['Category']}  
            • **Dosage Form**: {row['Dosage Form']}  
            • **Strength**: {row['Strength']}  
            • **Indication**: {row['Indication']}  
            • **Manufacturer**: {row['Manufacturer']}
            """  
    return "**Medic-Bot:** Medicine not found in database."
import base64
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()