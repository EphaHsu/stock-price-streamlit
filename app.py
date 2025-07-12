import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📈 Stock Price Viewer")

# Upload CSV
uploaded_file = st.file_uploader("Upload stock price CSV file", type=["csv"])

if uploaded_file:
    # Load data
    df = pd.read_csv(uploaded_file, parse_dates=["Date"])
    df.set_index("Date", inplace=True)
    df.sort_index(inplace=True)

    # Frequency options
    freq_map = {
        "Daily": "D",
        "Weekly": "W",
        "Monthly": "M",
        "Yearly": "Y"
    }

    freq_choice = st.selectbox("Select frequency", list(freq_map.keys()), index=0)

    # Resample
    freq = freq_map[freq_choice]
    df_resampled = df["Close"].resample(freq).last()

    # Plot
    fig, ax = plt.subplots()
    df_resampled.plot(ax=ax, label="Close Price")
    ax.set_title(f"Stock Price ({freq_choice})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.grid(True)
    st.pyplot(fig)
else:
    st.info("👆 Upload a CSV file with 'Date' and 'Close' columns to get started.")