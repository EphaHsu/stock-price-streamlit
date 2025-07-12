import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta

st.set_page_config(page_title="Stock Price Viewer", layout="centered")
st.title("📈 Stock Price Viewer (with yfinance)")

# Input: Ticker symbol
ticker = st.text_input("Enter stock ticker symbol (e.g. AAPL, TSLA)", value="AAPL")

# Input: Time range
date_range_options = {
    "1 Week": 7,
    "1 Month": 30,
    "6 Months": 182,
    "1 Year": 365,
    "10 Years": 365*10
}
time_range_choice = st.selectbox("Select time range", list(date_range_options.keys()), index=4)

# Input: Frequency selector
freq_map = {
    "Daily": "D",
    "Weekly": "W",
    "Monthly": "M",
    "Yearly": "Y"
}
freq_choice = st.selectbox("Select frequency", list(freq_map.keys()), index=0)

# Get data when ticker is entered
if ticker:
    try:
        # Calculate date range
        end_date = datetime.today()
        start_date = end_date - timedelta(days=date_range_options[time_range_choice])

        # Download data
        df = yf.download(ticker, start=start_date, end=end_date)

        if df.empty:
            st.warning("No data found for this ticker.")
        else:
            # Clean up
            df = df[["Close"]]
            df.index = pd.to_datetime(df.index)
            df.sort_index(inplace=True)

            # Resample
            freq = freq_map[freq_choice]
            df_resampled = df["Close"].resample(freq).last()

            # Plot
            fig, ax = plt.subplots()
            df_resampled.plot(ax=ax, label=f"{ticker} Close")
            ax.set_title(f"{ticker} Price - {time_range_choice} ({freq_choice})")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price (USD)")
            ax.grid(True)
            st.pyplot(fig)
    except Exception as e:
        st.error(f"Error fetching data: {e}")