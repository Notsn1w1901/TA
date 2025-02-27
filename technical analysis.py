import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta  # Changed to pandas_ta

# Streamlit UI
st.title("Bitcoin Technical Analysis Signals")
st.sidebar.header("Indicator Settings")

# User inputs (keep same as before)
sma_short = st.sidebar.slider("SMA Short Period", 10, 100, 50)
sma_long = st.sidebar.slider("SMA Long Period", 100, 400, 200)
bb_period = st.sidebar.slider("Bollinger Bands Period", 10, 50, 20)
rsi_period = st.sidebar.slider("RSI Period", 10, 30, 14)
macd_fast = st.sidebar.slider("MACD Fast Period", 5, 20, 12)
macd_slow = st.sidebar.slider("MACD Slow Period", 20, 50, 26)
macd_signal = st.sidebar.slider("MACD Signal Period", 5, 20, 9)

# Fetch Bitcoin data
btc = yf.download("BTC-USD", period="6mo", interval="1d")

# Calculate Indicators using pandas_ta
btc["SMA_S"] = ta.sma(btc["Close"], length=sma_short)
btc["SMA_L"] = ta.sma(btc["Close"], length=sma_long)
btc["RSI"] = ta.rsi(btc["Close"], length=rsi_period)

# Bollinger Bands
bbands = ta.bbands(btc["Close"], length=bb_period)
btc["Upper_BB"] = bbands[f"BBU_{bb_period}_2.0"]
btc["Lower_BB"] = bbands[f"BBL_{bb_period}_2.0"]

# MACD
macd = ta.macd(btc["Close"], fast=macd_fast, slow=macd_slow, signal=macd_signal)
btc["MACD"] = macd[f"MACD_{macd_fast}_{macd_slow}_{macd_signal}"]
btc["MACD_Signal"] = macd[f"MACDs_{macd_fast}_{macd_slow}_{macd_signal}"]

# Rest of the signal logic remains the same
# ... (keep all signal detection code unchanged)

# Display signals
st.subheader("Latest Signals for BTC-USD")
if signals:
    for signal in signals:
        st.write(f"✅ {signal}")
else:
    st.write("🔍 No significant signals detected.")
