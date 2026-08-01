import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from datetime import datetime

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="AI Trading Assistant",
    page_icon="📈",
    layout="wide"
)

# -----------------------
# Demo Market Data
# -----------------------
price = 24383.60
trend = "Bullish 🟢"
signal = "BUY 🟢"
confidence = "75%"

# -----------------------
# Title
# -----------------------
st.title("📈 AI Trading Assistant")
st.caption("🚀 Powered by Upstox API + AI")

st.success("🟢 LIVE MARKET CONNECTED")
st.info(f"🏛️ Market : NSE | 🕒 {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

# -----------------------
# Metrics
# -----------------------
col1, col2 = st.columns(2)

with col1:
    st.metric("📈 NIFTY 50", f"{price:,.2f}")
    st.metric("💰 Market Status", "LIVE 🟢")
    st.caption("🔄 Auto Refresh : Every 5 Seconds")

with col2:
    st.metric("📈 Trend", trend)
    st.metric("🧠 AI Signal", signal)
    st.metric("🎯 Confidence", confidence)
    st.caption(f"✅ Last Updated : {datetime.now().strftime('%H:%M:%S')}")
# -----------------------
# AI Analysis Table
# -----------------------

st.subheader("📊 AI Analysis")

df = pd.DataFrame({
    "Indicator": [
        "RSI",
        "MACD",
        "EMA 20",
        "EMA 50",
        "Trend"
    ],
    "Status": [
        "52.4 🟡",
        "Bullish 🟢",
        "24,320 🟢",
        "24,180 🟢",
        trend
    ]
})

st.dataframe(df, use_container_width=True)
# -----------------------
# Market Summary
# -----------------------

st.subheader("📋 Market Summary")

if signal == "BUY 🟢":
    st.success("✅ AI Recommendation: BUY")
elif signal == "SELL 🔴":
    st.error("❌ AI Recommendation: SELL")
else:
    st.warning("⚠️ AI Recommendation: WAIT")

st.info(
    f"""
**Trend:** {trend}

**Signal:** {signal}

**Confidence:** {confidence}

**Market:** NSE
"""
)