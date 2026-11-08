import streamlit as st
import yfinance as yf
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Stock Explorer",
    page_icon="📈",
    layout="wide"
)

st.title("📈Stock Explorer")
st.write("Explore real stock market data without needing to memorize ticker symbols!")

# --- POPULAR STOCKS DICTIONARY ---
POPULAR_STOCKS = {
    "🔥 Big Tech & AI": {
        "Apple (AAPL)": "AAPL",
        "Microsoft (MSFT)": "MSFT",
        "Google / Alphabet (GOOGL)": "GOOGL",
        "Amazon (AMZN)": "AMZN",
        "NVIDIA (NVDA)": "NVDA",
        "Tesla (TSLA)": "TSLA",
        "Meta / Facebook (META)": "META"
    },
    "🏛️ Market Indexes & ETFs": {
        "S&P 500 Index ETF (SPY)": "SPY",
        "Nasdaq 100 ETF (QQQ)": "QQQ",
        "Dow Jones Industrial ETF (DIA)": "DIA",
        "Total Stock Market ETF (VTI)": "VTI"
    },
    "🍔 Famous Brands & Retail": {
        "Coca-Cola (KO)": "KO",
        "McDonald's (MCD)": "MCD",
        "Nike (NKE)": "NKE",
        "Disney (DIS)": "DIS",
        "Walmart (WMT)": "WMT",
        "Netflix (NFLX)": "NFLX"
    },
    "🪙 Crypto & Assets": {
        "Bitcoin USD (BTC-USD)": "BTC-USD",
        "Ethereum USD (ETH-USD)": "ETH-USD",
        "Gold Trust (GLD)": "GLD"
    }
}

# --- SIDEBAR CONTROLS ---
st.sidebar.header("1. Choose a Stock")

# Selection Mode
selection_mode = st.sidebar.radio(
    "How would you like to pick a stock?",
    ["Select from Popular Stocks", "Type Custom Ticker Symbol"]
)

selected_ticker = "AAPL"

if selection_mode == "Select from Popular Stocks":
    category = st.sidebar.selectbox("Choose Category", list(POPULAR_STOCKS.keys()))
    stock_label = st.sidebar.selectbox("Choose Stock", list(POPULAR_STOCKS[category].keys()))
    selected_ticker = POPULAR_STOCKS[category][stock_label]
else:
    selected_ticker = st.sidebar.text_input(
        "Enter Symbol (e.g., AMD, INTC, PYPL)", 
        value="AAPL"
    ).upper().strip()

st.sidebar.header("2. Customize View")

time_period = st.sidebar.selectbox(
    "Select Time Horizon",
    options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
    index=3
)

data_column = st.sidebar.selectbox(
    "Select Metric",
    options=["Close", "Open", "High", "Low", "Volume"],
    index=0
)

chart_type = st.sidebar.selectbox(
    "Select Chart Type",
    options=["Line Chart", "Area Chart", "Bar Chart"]
)

# --- REAL DATA FETCHING ---
@st.cache_data(ttl=3600)
def load_stock_data(ticker, period):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    return df, stock.info

try:
    with st.spinner(f"Loading data for **{selected_ticker}**..."):
        df, info = load_stock_data(selected_ticker, time_period)

    if df.empty:
        st.error(f"No data found for symbol '{selected_ticker}'. Please check your input.")
    else:
        # Get readable names and info safely
        company_name = info.get("shortName", selected_ticker)
        sector = info.get("sector", "N/A")
        summary = info.get("longBusinessSummary", "")

        st.subheader(f"{company_name} ({selected_ticker})")
        if sector != "N/A":
            st.caption(f"**Sector:** {sector}")

        # Metrics display
        latest_price = df["Close"].iloc[-1]
        previous_price = df["Close"].iloc[-2] if len(df) > 1 else latest_price
        price_change = latest_price - previous_price
        pct_change = (price_change / previous_price) * 100

        c1, c2, c3 = st.columns(3)
        c1.metric("Latest Price", f"${latest_price:,.2f}", f"{price_change:+.2f} ({pct_change:+.2f}%)")
        c2.metric("High (Period)", f"${df['High'].max():,.2f}")
        c3.metric("Low (Period)", f"${df['Low'].min():,.2f}")

        # Render Chart
        st.write(f"### {data_column} Price Chart ({time_period})")
        chart_df = df[[data_column]]

        if chart_type == "Line Chart":
            st.line_chart(chart_df)
        elif chart_type == "Area Chart":
            st.area_chart(chart_df)
        elif chart_type == "Bar Chart":
            st.bar_chart(chart_df)

        # Expandable Company Info
        if summary:
            with st.expander("ℹ️ About this company"):
                st.write(summary)

        # Raw data option
        if st.checkbox("Show Raw Data Table"):
            st.dataframe(df)

except Exception as e:
    st.error(f"Error retrieving stock data: {e}")
