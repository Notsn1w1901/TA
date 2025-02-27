import streamlit as st
import yfinance as yf
import pandas as pd
import ta  # Make sure to use 'ta' and not 'pandas_ta'

# Streamlit UI
st.title("Bitcoin Technical Analysis Signals")
st.sidebar.header("Indicator Settings")

# User inputs
sma_short = st.sidebar.slider("SMA Short Period", 10, 100, 50)
sma_long = st.sidebar.slider("SMA Long Period", 100, 400, 200)
bb_period = st.sidebar.slider("Bollinger Bands Period", 10, 50, 20)
rsi_period = st.sidebar.slider("RSI Period", 10, 30, 14)
macd_fast = st.sidebar.slider("MACD Fast Period", 5, 20, 12)
macd_slow = st.sidebar.slider("MACD Slow Period", 20, 50, 26)
macd_signal = st.sidebar.slider("MACD Signal Period", 5, 20, 9)

# Fetch Bitcoin data
btc = yf.download("BTC-USD", period="6mo", interval="1d")

# Ensure the data is not empty
if btc.empty:
    st.error("Failed to load BTC-USD data. Try again later.")
    st.stop()

# **Handle Missing Data**
btc["Close"] = btc["Close"].fillna(method="ffill")  # Forward fill missing values
btc.dropna(inplace=True)  # Drop remaining NaN values

# Ensure the 'Close' column is a proper Pandas Series
close_series = btc["Close"].astype(float)

# Calculate Indicators using 'ta' library
btc["SMA_S"] = ta.trend.SMAIndicator(close_series, window=sma_short).sma_indicator()
btc["SMA_L"] = ta.trend.SMAIndicator(close_series, window=sma_long).sma_indicator()
btc["RSI"] = ta.momentum.RSIIndicator(close_series, window=rsi_period).rsi()

# Bollinger Bands
bbands = ta.volatility.BollingerBands(close_series, window=bb_period)
btc["Upper_BB"] = bbands.bollinger_hband()
btc["Lower_BB"] = bbands.bollinger_lband()

# MACD
macd = ta.trend.MACD(close_series, window_slow=macd_slow, window_fast=macd_fast, window_sign=macd_signal)
btc["MACD"] = macd.macd()
btc["MACD_Signal"] = macd.macd_signal()

# Get latest data
latest = btc.iloc[-1]
prev = btc.iloc[-2]

# Signal detection logic
signals = []

# SMA Crossovers
if prev["SMA_S"] < prev["SMA_L"] and latest["SMA_S"] > latest["SMA_L"]:
    signals.append("Golden Cross: SMA Short crossed above SMA Long (Bullish)")

if prev["SMA_S"] > prev["SMA_L"] and latest["SMA_S"] < latest["SMA_L"]:
    signals.append("Death Cross: SMA Short crossed below SMA Long (Bearish)")

# RSI Conditions
if latest["RSI"] > 70:
    signals.append("RSI Overbought: Potential price reversal downward")

if latest["RSI"] < 30:
    signals.append("RSI Oversold: Potential price reversal upward")

# Bollinger Bands
if latest["Close"] > latest["Upper_BB"]:
    signals.append("Price Above Upper Bollinger Band: Market may be overbought")

if latest["Close"] < latest["Lower_BB"]:
    signals.append("Price Below Lower Bollinger Band: Market may be oversold")

# MACD Crossovers
if prev["MACD"] < prev["MACD_Signal"] and latest["MACD"] > latest["MACD_Signal"]:
    signals.append("Bullish MACD Crossover: MACD crossed above Signal Line (Buy Signal)")

if prev["MACD"] > prev["MACD_Signal"] and latest["MACD"] < latest["MACD_Signal"]:
    signals.append("Bearish MACD Crossover: MACD crossed below Signal Line (Sell Signal)")

# Display signals
st.subheader("Latest Signals for BTC-USD")
if signals:
    for signal in signals:
        st.write(f"✅ {signal}")
else:
    st.write("🔍 No significant signals detected.")


