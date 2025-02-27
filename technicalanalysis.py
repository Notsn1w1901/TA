import streamlit as st
import yfinance as yf
import pandas as pd
import ta

# Streamlit UI
st.title("Cryptocurrency Technical Analysis Signals")
st.sidebar.header("Settings")

# Ticker input
ticker = st.sidebar.text_input("Enter Ticker (e.g., BTC-USD)", "BTC-USD").upper()

# Indicator settings
sma_short = st.sidebar.slider("SMA Short Period", 10, 100, 50)
sma_long = st.sidebar.slider("SMA Long Period", 100, 400, 200)
bb_period = st.sidebar.slider("Bollinger Bands Period", 10, 50, 20)
rsi_period = st.sidebar.slider("RSI Period", 10, 30, 14)
macd_fast = st.sidebar.slider("MACD Fast Period", 5, 20, 12)
macd_slow = st.sidebar.slider("MACD Slow Period", 20, 50, 26)
macd_signal = st.sidebar.slider("MACD Signal Period", 5, 20, 9)

# Fetch data
btc = yf.download(ticker, period="1y", interval="1d")

# Check if data is available
if btc.empty or "Close" not in btc.columns or btc["Close"].dropna().empty:
    st.error(f"Failed to load {ticker} data. Try another ticker.")
    st.stop()

# Fill missing values
btc["Close"].fillna(method="ffill", inplace=True)

# Convert 'Close' to a Pandas Series
close_series = btc["Close"].astype(float)

# Calculate technical indicators
try:
    btc["SMA_S"] = ta.trend.SMAIndicator(close_series, window=sma_short).sma_indicator()
    btc["SMA_L"] = ta.trend.SMAIndicator(close_series, window=sma_long).sma_indicator()
    btc["RSI"] = ta.momentum.RSIIndicator(close_series, window=rsi_period).rsi()
    
    bbands = ta.volatility.BollingerBands(close_series, window=bb_period)
    btc["Upper_BB"] = bbands.bollinger_hband()
    btc["Lower_BB"] = bbands.bollinger_lband()

    macd = ta.trend.MACD(close_series, window_slow=macd_slow, window_fast=macd_fast, window_sign=macd_signal)
    btc["MACD"] = macd.macd()
    btc["MACD_Signal"] = macd.macd_signal()
except Exception as e:
    st.error(f"Error calculating indicators: {e}")
    st.write("BTC data preview:")
    st.write(btc.head())  # Debugging output
    st.stop()

# Drop NaN values
btc.dropna(inplace=True)

# Ensure enough data exists
if len(btc) < 2:
    st.error("Not enough historical data to generate signals.")
    st.write("Data preview:")
    st.write(btc.head())  # Debugging
    st.stop()

# Get latest and previous data
latest = btc.iloc[-1]
prev = btc.iloc[-2]

# Signal detection
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

# Display signals in the main dashboard
st.subheader(f"Latest Signals for {ticker}")
if signals:
    for signal in signals:
        st.write(f"✅ {signal}")
else:
    st.write("🔍 No significant signals detected.")
