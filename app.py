import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="AI Trading Assistant",
    page_icon="📈",
    layout="centered"
)

st.title("📈 AI Trading Assistant")
st.caption("Upstox • Signal Dashboard V1")

st.warning("⚠️ Paper Trading Mode — No real orders are placed.")

market = st.selectbox(
    "Select Market",
    ["NIFTY 50", "BANK NIFTY", "MCX CRUDE OIL"]
)

st.divider()

st.subheader(market)

col1, col2 = st.columns(2)

with col1:
    st.metric("Market Price", "Waiting...")
    st.metric("Trend", "Waiting...")

with col2:
    st.metric("Signal", "⚪ WAIT")
    st.metric("Confidence", "0%")

st.divider()

st.subheader("🎯 Trade Setup")

st.write("**Entry:** Waiting for signal")
st.write("**Stop Loss:** —")
st.write("**Target 1:** —")
st.write("**Target 2:** —")

st.divider()

st.subheader("🧠 Signal Engine")

st.write("EMA Trend: ⏳")
st.write("RSI Momentum: ⏳")
st.write("VWAP Confirmation: ⏳")
st.write("Price Action: ⏳")

st.divider()

st.caption(
    "Last updated: "
    + datetime.now().strftime("%d-%m-%Y %H:%M:%S")
)

st.info(
    "V1 is for testing and paper trading. "
    "Live Upstox market data will be connected next."
)
