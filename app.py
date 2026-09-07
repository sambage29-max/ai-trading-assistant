 from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import json
import ta

# Agar tumne alag se indicators aur ai_engine files banayi hain toh yeh kaam aayengi
try:
    from indicators import calculate_indicators
except ImportError:
    # Agar calculate_indicators module nahi milta toh yeh backup functions use honge
    def calculate_indicators(df):
        # 14-period RSI compute karne ke liye simple logic
        df["RSI"] = ta.momentum.rsi(close=df["Close"], window=14)
        df["EMA20"] = ta.trend.ema_indicator(close=df["Close"], window=20)
        df["EMA50"] = ta.trend.ema_indicator(close=df["Close"], window=50)
        df["ATR"] = ta.volatility.average_true_range(high=df["High"], low=df["Low"], close=df["Close"], window=14)
        df["ADX"] = ta.trend.adx(high=df["High"], low=df["Low"], close=df["Close"], window=14)
        return df

# --- Page Config ---
st.set_page_config(
    page_title="AI Trading Assistant",
    page_icon="📈",
    layout="wide"
)

# --- Function: Get Market Data ---
def get_market_data():
    # Asli data ko list of lists format me daala
    dummy_data = [
        ["2026-08-07", 25130, 25180, 25110, 25160, 250000],
        ["2026-08-07", 25160, 25200, 25140, 25190, 260000],
        ["2026-08-07", 25190, 25220, 25170, 25200, 270000],
        ["2026-08-07", 25200, 25240, 25180, 25210, 280000],
        ["2026-08-07", 25210, 25250, 25190, 25220, 290000],
        ["2026-08-07", 25220, 25260, 25200, 25240, 300000],
        ["2026-08-07", 25240, 25280, 25220, 25260, 310000],
        ["2026-08-07", 25260, 25300, 25240, 25290, 320000],
        ["2026-08-07", 25290, 25320, 25270, 25310, 330000],
        ["2026-08-07", 25310, 25350, 25290, 25340, 340000],
        ["2026-08-07", 25360, 25400, 25340, 25390, 360000],
        ["2026-08-07", 25390, 25420, 25370, 25400, 370000],
        ["2026-08-07", 25400, 25450, 25380, 25420, 380000],
        ["2026-08-07", 25420, 25480, 25400, 25460, 390000],
        ["2026-08-07", 25460, 25500, 25440, 25480, 400000]
    ]
    
    # Column names setup kiye
    columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    
    # Pandas DataFrame banaya
    df_live = pd.DataFrame(dummy_data, columns=columns)
    
    # Date ko standard format me badla
    df_live["Date"] = pd.to_datetime(df_live["Date"])
    
    # Indicators calculate kiye (df_live ka use karke)
    df_live = calculate_indicators(df_live)
    
    return df_live

# --- Data Execution Logic ---
data = get_market_data()

st.title("📊 AI Trading Assistant Dashboard")

if data is not None and not data.empty:
    # Latest indicators value nikalna (safety check ke sath)
    price = float(data["Close"].iloc[-1])
    rsi = float(data["RSI"].iloc[-1]) if "RSI" in data.columns and not pd.isna(data["RSI"].iloc[-1]) else 0.0
    ema20 = float(data["EMA20"].iloc[-1]) if "EMA20" in data.columns and not pd.isna(data["EMA20"].iloc[-1]) else 0.0
    ema50 = float(data["EMA50"].iloc[-1]) if "EMA50" in data.columns and not pd.isna(data["EMA50"].iloc[-1]) else 0.0
    atr = float(data["ATR"].iloc[-1]) if "ATR" in data.columns and not pd.isna(data["ATR"].iloc[-1]) else 0.0
    adx = float(data["ADX"].iloc[-1]) if "ADX" in data.columns and not pd.isna(data["ADX"].iloc[-1]) else 0.0

    # Dashboard par metrics show karna
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Latest Price", value=f"₹{price:.2f}")
    col2.metric(label="RSI (14)", value=f"{rsi:.2f}")
    col3.metric(label="EMA 20", value=f"₹{ema20:.2f}")
    col4.metric(label="ADX", value=f"{adx:.2f}")

    # Trading Signal Logic
    st.subheader("💡 System Signal")
    if rsi < 30 and price > ema20:
        st.success("🟢 SIGNAL: BUY | Stop-Loss: 2% below Entry | Target: 4% target")
    elif rsi > 70 or price < ema20:
        st.error("🔴 SIGNAL: SELL / EXIT | Stop-Loss hit ya overbought conditions")
    else:
        st.warning("⚪ SIGNAL: HOLD | Market zone clear nahi hai, wait karein.")

    # Data Table View
    st.subheader("📋 Market History & Indicators")
    st.dataframe(data.tail(10))
else:
    st.error("Market data load nahi ho paya. Kripya check karein.")
