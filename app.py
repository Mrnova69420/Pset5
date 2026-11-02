import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Interactive Visualization App",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dynamic Data Explorer")
st.write("Customize the visualization using the controls in the sidebar!")

# --- SIDEBAR CONTROLS (USER INPUTS) ---
st.sidebar.header("User Inputs")

# 1. Text Input
custom_title = st.sidebar.text_input(
    label="Custom Chart Title", 
    value="Monthly Metrics Dashboard"
)

# 2. Dropdown / Selectbox
chart_type = st.sidebar.selectbox(
    label="Select Chart Type",
    options=["Bar Chart", "Line Chart", "Area Chart"]
)

# 3. Slider Input
num_months = st.sidebar.slider(
    label="Select Range (Months)",
    min_value=3,
    max_value=12,
    value=6
)

# --- DATA GENERATION ---
np.random.seed(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][:num_months]
revenue = np.random.randint(200, 600, size=num_months)
expenses = revenue * np.random.uniform(0.4, 0.7, size=num_months)

df = pd.DataFrame({
    "Month": months,
    "Revenue ($)": revenue,
    "Expenses ($)": np.round(expenses, 2)
}).set_index("Month")

# --- MAIN DISPLAY & VISUALIZATION ---
st.subheader(custom_title)

# Display Key Metrics
col1, col2 = st.columns(2)
col1.metric("Total Revenue", f"${df['Revenue ($)'].sum():,}")
col2.metric("Total Expenses", f"${df['Expenses ($)'].sum():,.2f}")

# Render Selected Chart
if chart_type == "Bar Chart":
    st.bar_chart(df)
elif chart_type == "Line Chart":
    st.line_chart(df)
elif chart_type == "Area Chart":
    st.area_chart(df)

# Toggle to display raw data
if st.checkbox("Show Raw Data Table"):
    st.dataframe(df)