import streamlit as st
import yfinance as yf
import pandas as pd
import ta  # Using ta library instead of pandas-ta or TA-Lib

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

# Calculate Indicators using ta library
btc["SMA_S"] = ta.trend.sma_indicator(btc["Close"], window=sma_short)
btc["SMA_L"] = ta.trend.sma_indicator(btc["Close"], window=sma_long)
btc["RSI"] = ta.momentum.rsi(btc["Close"], window=rsi_period)

# Bollinger Bands
bb = ta.volatility.BollingerBands(btc["Close"], window=bb_period)
btc["Upper_BB"] = bb.bollinger_hband()
btc["Lower_BB"] = bb.bollinger_lband()

# MACD
macd = ta.trend.MACD(btc["Close"], window_slow=macd_slow, window_fast=macd_fast, window_sign=macd_signal)
btc["MACD"] = macd.macd()
btc["MACD_Signal"] = macd.macd_signal()

# Get latest data
latest = btc.iloc[-1]
prev = btc.iloc[-2]

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
