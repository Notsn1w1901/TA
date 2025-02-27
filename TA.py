import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib

# Fetch Bitcoin historical data
btc = yf.download("BTC-USD", period="6mo", interval="1d")

# Calculate Technical Indicators
btc["SMA_50"] = talib.SMA(btc["Close"], timeperiod=50)
btc["SMA_200"] = talib.SMA(btc["Close"], timeperiod=200)
btc["Upper_BB"], btc["Middle_BB"], btc["Lower_BB"] = talib.BBANDS(btc["Close"], timeperiod=20)
btc["RSI"] = talib.RSI(btc["Close"], timeperiod=14)
macd, macd_signal, _ = talib.MACD(btc["Close"], fastperiod=12, slowperiod=26, signalperiod=9)

# Plot Bitcoin Price & Indicators
fig, axs = plt.subplots(3, figsize=(12, 8), sharex=True)

# Price Chart with SMA & Bollinger Bands
axs[0].plot(btc.index, btc["Close"], label="BTC Price", color="black")
axs[0].plot(btc.index, btc["SMA_50"], label="50-day SMA", color="blue", linestyle="dashed")
axs[0].plot(btc.index, btc["SMA_200"], label="200-day SMA", color="red", linestyle="dashed")
axs[0].fill_between(btc.index, btc["Upper_BB"], btc["Lower_BB"], color="gray", alpha=0.3)
axs[0].legend()
axs[0].set_title("Bitcoin Price with SMA & Bollinger Bands")

# MACD Chart
axs[1].plot(btc.index, macd, label="MACD", color="blue")
axs[1].plot(btc.index, macd_signal, label="Signal Line", color="red", linestyle="dashed")
axs[1].axhline(0, color="black", linewidth=0.7, linestyle="dotted")
axs[1].legend()
axs[1].set_title("MACD Indicator")

# RSI Chart
axs[2].plot(btc.index, btc["RSI"], label="RSI", color="purple")
axs[2].axhline(70, color="red", linestyle="dotted", label="Overbought (70)")
axs[2].axhline(30, color="green", linestyle="dotted", label="Oversold (30)")
axs[2].legend()
axs[2].set_title("RSI Indicator")

plt.tight_layout()
plt.show()
