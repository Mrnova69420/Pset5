import streamlit as st
import yfinance as yf
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Real-World Stock Data Explorer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Real-World Stock Data Explorer")
st.write("Fetch real financial market data and customize your view using the sidebar controls!")

# --- SIDEBAR CONTROLS (USER INPUTS) ---
st.sidebar.header("User Inputs")

# 1. Text Input for Ticker
ticker_input = st.sidebar.text_input(
    label="Stock Ticker (e.g., AAPL, MSFT, GOOGL, TSLA)",
    value="AAPL"
).upper().strip()

# 2. Selectbox for Time Horizon
time_period = st.sidebar.selectbox(
    label="Select Time Horizon",
    options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
    index=3
)

# 3. Selectbox for Data Column to Plot
data_column = st.sidebar.selectbox(
    label="Select Metric to Visualize",
    options=["Close", "Open", "High", "Low", "Volume"],
    index=0
)

# 4. Selectbox for Chart Type
chart_type = st.sidebar.selectbox(
    label="Select Chart Type",
    options=["Line Chart", "Area Chart", "Bar Chart"]
)

# --- REAL DATA FETCHING ---
@st.cache_data(ttl=3600)  # Cache data for 1 hour to prevent redundant requests
def load_stock_data(ticker, period):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    return df, stock.info

try:
    with st.spinner(f"Fetching real data for **{ticker_input}**..."):
        df, info = load_stock_data(ticker_input, time_period)

    if df.empty:
        st.error(f"No data found for ticker '{ticker_input}'. Please check the symbol and try again.")
    else:
        # Get Company Name safely
        company_name = info.get("shortName", ticker_input)
        st.subheader(f"{company_name} ({ticker_input}) - {data_column} Price")

        # --- KEY METRICS ---
        latest_price = df["Close"].iloc[-1]
        previous_price = df["Close"].iloc[-2] if len(df) > 1 else latest_price
        price_change = latest_price - previous_price
        pct_change = (price_change / previous_price) * 100

        col1, col2, col3 = st.columns(3)
        col1.metric("Latest Closing Price", f"${latest_price:,.2f}", f"{price_change:+.2f} ({pct_change:+.2f}%)")
        col2.metric("Highest Price (Period)", f"${df['High'].max():,.2f}")
        col3.metric("Lowest Price (Period)", f"${df['Low'].min():,.2f}")

        # --- CHARTS ---
        chart_data = df[[data_column]]

        if chart_type == "Line Chart":
            st.line_chart(chart_data)
        elif chart_type == "Area Chart":
            st.area_chart(chart_data)
        elif chart_type == "Bar Chart":
            st.bar_chart(chart_data)

        # --- RAW DATA TOGGLE ---
        if st.checkbox("Show Raw Stock Data Table"):
            st.dataframe(df)

except Exception as e:
    st.error(f"An error occurred while fetching data: {e}")
