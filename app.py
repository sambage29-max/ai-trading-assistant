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
rsi = 52.4
macd = "Bullish"
ema20 = 24320
ema50 = 24180

if rsi > 60 and macd == "Bullish":
    signal = "BUY 🟢"
    confidence = "90%"
elif rsi < 40 and macd == "Bearish":
    signal = "SELL 🔴"
    confidence = "90%"
else:
    signal = "WAIT 🟡"
    confidence = "75%"

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
st.subheader("📈 NIFTY Trend Chart")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        y=chart_data,
        mode="lines+markers",
        name="NIFTY"
    )
)

fig.update_layout(
    height=350,
    xaxis_title="Time",
    yaxis_title="Price"
)

st.plotly_chart(fig, use_container_width=True) 
st.markdown("---")

st.subheader("📊 AI Score")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("RSI", "52.4")

with col2:
    st.metric("MACD", "Bullish 🟢")

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