import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("TellCo User Analysis Dashboard")

# Sidebar
st.sidebar.header("Dashboard Options")
selected_option = st.sidebar.selectbox(
    "Select a view:",
    ["Overview", "Handset Analysis", "Manufacturer Analysis"]
)

# Load Real Data
from scripts import TelecomAnalysis
database = "telecom"
password = "password"
table_name = "xdr_data"

analysis = TelecomAnalysis(database=database, password=password, table_name=table_name)

# Step 1: Load the data
data = analysis.load_data()

# Extract Real Data
top_handsets = analysis.find_top_handsets(n=10)
top_manufacturers = analysis.find_top_manufacturers(n=3)

# Display based on selection
if selected_option == "Overview":
    st.header("Overview")
    st.write("This dashboard provides insights into TellCo user behavior, handset usage, and manufacturer trends.")

elif selected_option == "Handset Analysis":
    st.header("Top 10 Handsets")
    if top_handsets is not None:
        st.write("Bar chart of the most popular handsets among TellCo customers.")
        fig, ax = plt.subplots(figsize=(18, 6))
        top_handsets.plot(kind='bar', color='skyblue', ax=ax)
        ax.set_title('Top 10 Handsets Used by Customers', fontsize=16)
        ax.set_xlabel('Handset Type', fontsize=14)
        ax.set_ylabel('Number of Users', fontsize=14)
        ax.set_xticklabels(top_handsets.index, rotation=45, ha='right', fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
    else:
        st.warning("No data available for Top 10 Handsets.")

elif selected_option == "Manufacturer Analysis":
    st.header("Top 3 Handset Manufacturers")
    if top_manufacturers is not None:
        st.write("Bar chart showing the top 3 handset manufacturers.")
        fig, ax = plt.subplots(figsize=(8, 5))
        top_manufacturers.plot(kind='bar', color='orange', ax=ax)
        ax.set_title('Top 3 Handset Manufacturers', fontsize=16)
        ax.set_xlabel('Manufacturer', fontsize=14)
        ax.set_ylabel('Number of Users', fontsize=14)
        ax.set_xticklabels(top_manufacturers.index, rotation=45, ha='right', fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
    else:
        st.warning("No data available for Top 3 Handset Manufacturers.")

# Footer
st.write("Dashboard created with Streamlit.")