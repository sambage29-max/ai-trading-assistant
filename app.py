from datetime import datetime
import streamlit as st
import pandas as pd
import ta

# Technical indicators backup function
def calculate_indicators(df):
    df["RSI"] = ta.momentum.rsi(close=df["Close"], window=14)
    df["EMA20"] = ta.trend.ema_indicator(close=df["Close"], window=20)
    df["EMA50"] = ta.trend.ema_indicator(close=df["Close"], window=50)
    return df

st.set_page_config(page_title="AI Trading Assistant", layout="wide")

def get_market_data():
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
    columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    df_live = pd.DataFrame(dummy_data, columns=columns)
    df_live["Date"] = pd.to_datetime(df_live["Date"])
    df_live = calculate_indicators(df_live)
    return df_live

data = get_market_data()

st.title("📊 AI Trading Assistant")

if data is not None and not data.empty:
    price = float(data["Close"].iloc[-1])
    rsi = float(data["RSI"].iloc[-1]) if "RSI" in data.columns else 0.0
    ema20 = float(data["EMA20"].iloc[-1]) if "EMA20" in data.columns else 0.0

    col1, col2, col3 = st.columns(3)
    col1.metric("Latest Price", f"₹{price:.2f}")
    col2.metric("RSI (14)", f"{rsi:.2f}")
    col3.metric("EMA 20", f"₹{ema20:.2f}")

    st.subheader("💡 Signal")
    if rsi < 40:
        st.success("🟢 BUY SIGNAL | SL: 2% below Entry")
    elif rsi > 70:
        st.error("🔴 EXIT / SELL SIGNAL")
    else:
        st.warning("⚪ HOLD | Market is neutral")
        
    st.subheader("📋 Data Table")
    st.dataframe(data.tail(5))
