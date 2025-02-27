import streamlit as st
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas_ta as ta  # Using pandas-ta instead of TA-Lib

# Streamlit UI
st.title("Bitcoin Technical Analysis Dashboard")
st.sidebar.header("Indicator Settings")

# User inputs
sma_short = st.sidebar.slider("SMA Short Period (e.g. 50)", min_value=10, max_value=100, value=50)
sma_long = st.sidebar.slider("SMA Long Period (e.g. 200)", min_value=100, max_value=400, value=200)
bb_period = st.sidebar.slider("Bollinger Bands Period", min_value=10, max_value=50, value=20)
rsi_period = st.sidebar.slider("RSI Period", min_value=10, max_value=30, value=14)
macd_fast = st.sidebar.slider("MACD Fast Period", min_value=5, max_value=20, value=12)
macd_slow = st.sidebar.slider("MACD Slow Period", min_value=20, max_value=50, value=26)
macd_signal = st.sidebar.slider("MACD Signal Period", min_value=5, max_value=20, value=9)

# Fetch Bitcoin data
btc = yf.download("BTC-USD", period="6mo", interval="1d")

# Calculate Indicators using pandas-ta
btc["SMA_S"] = btc["Close"].ta.sma(length=sma_short)
btc["SMA_L"] = btc["Close"].ta.sma(length=sma_long)
btc["RSI"] = btc["Close"].ta.rsi(length=rsi_period)

# Bollinger Bands
bbands = btc["Close"].ta.bbands(length=bb_period)
btc["Upper_BB"] = bbands[f"BBU_{bb_period}_2.0"]
btc["Middle_BB"] = bbands[f"BBM_{bb_period}_2.0"]
btc["Lower_BB"] = bbands[f"BBL_{bb_period}_2.0"]

# MACD
macd_df = btc["Close"].ta.macd(fast=macd_fast, slow=macd_slow, signal=macd_signal)
btc["MACD"] = macd_df[f"MACD_{macd_fast}_{macd_slow}_{macd_signal}"]
btc["MACD_Signal"] = macd_df[f"MACDs_{macd_fast}_{macd_slow}_{macd_signal}"]

# Plot indicators
fig, axs = plt.subplots(3, figsize=(12, 8), sharex=True)

# Price & SMA
axs[0].plot(btc.index, btc["Close"], label="BTC Price", color="black")
axs[0].plot(btc.index, btc["SMA_S"], label=f"SMA {sma_short}", color="blue", linestyle="dashed")
axs[0].plot(btc.index, btc["SMA_L"], label=f"SMA {sma_long}", color="red", linestyle="dashed")
axs[0].fill_between(btc.index, btc["Upper_BB"], btc["Lower_BB"], color="gray", alpha=0.3)
axs[0].legend()
axs[0].set_title("Bitcoin Price with SMA & Bollinger Bands")

# MACD
axs[1].plot(btc.index, btc["MACD"], label="MACD", color="blue")
axs[1].plot(btc.index, btc["MACD_Signal"], label="Signal Line", color="red", linestyle="dashed")
axs[1].axhline(0, color="black", linewidth=0.7, linestyle="dotted")
axs[1].legend()
axs[1].set_title("MACD Indicator")

# RSI
axs[2].plot(btc.index, btc["RSI"], label="RSI", color="purple")
axs[2].axhline(70, color="red", linestyle="dotted", label="Overbought (70)")
axs[2].axhline(30, color="green", linestyle="dotted", label="Oversold (30)")
axs[2].legend()
axs[2].set_title("RSI Indicator")

plt.tight_layout()
st.pyplot(fig)
