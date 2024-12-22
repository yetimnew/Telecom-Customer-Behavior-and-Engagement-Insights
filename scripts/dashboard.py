import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Dynamically add the scripts folder to the Python path
project_path = r"D:\10x\Projects\Telecom-Customer-Behavior-and-Engagement-Insights"
if project_path not in sys.path:
    sys.path.append(project_path)


from scripts import TelecomAnalysis

# Titlecd
st.title("TellCo User Analysis Dashboard")

# Sidebar
st.sidebar.header("Dashboard Options")
selected_option = st.sidebar.selectbox(
    "Select a view:",
    ["Overview", "Handset Analysis", "Application Engagement"]
)

# Initialize and Load Data
database = "telecom"
password = "password"
table_name = "xdr_data"

try:
    # Use TelecomAnalysis class for data handling
    analysis = TelecomAnalysis(database=database, password=password, table_name=table_name)
    raw_data = analysis.load_data()

    # Clean the data using data_cleaning module
    data = clean_data(raw_data)  # Adjust as per your actual cleaning function
except Exception as e:
    st.error(f"Error loading or cleaning data: {e}")
    st.stop()

# Display Based on Selection
if selected_option == "Overview":
    st.header("Overview")
    st.write("Welcome to the TellCo User Analysis Dashboard!")
    st.write("Explore user behavior, device preferences, and engagement metrics.")

elif selected_option == "Handset Analysis":
    st.header("Top 10 Handsets")
    
    try:
        # Fetch Top 10 Handsets
        top_handsets = analysis.find_top_handsets(n=10)  # Ensure this method exists in TelecomAnalysis
        
        if top_handsets is not None:
            st.write("Bar chart of the most popular handsets among TellCo customers:")
            fig, ax = plt.subplots(figsize=(12, 6))
            top_handsets.plot(kind='bar', color='skyblue', ax=ax)
            ax.set_title('Top 10 Handsets Used by Customers', fontsize=16)
            ax.set_xlabel('Handset Type', fontsize=14)
            ax.set_ylabel('Number of Users', fontsize=14)
            ax.tick_params(axis='x', rotation=45, labelsize=12)
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            st.pyplot(fig)
        else:
            st.warning("No data available for Top 10 Handsets.")
    except Exception as e:
        st.error(f"Error plotting Top 10 Handsets: {e}")

elif selected_option == "Application Engagement":
    st.header("Application Engagement")
    st.write("Coming soon!")

# Footer
st.write("Dashboard created with Streamlit.")
