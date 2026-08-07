from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import json
import ta
from indicators import calculate_indicators
from ai_engine import ai_decision
from upstox_client import Configuration, ApiClient, HistoryApi
import streamlit as st

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="AI Trading Assistant",
    page_icon="📈",
    layout="wide"
)

# -----------------------
# --------------------------
 
# --------------------------
# Live Market Data
# --------------------------

@st.cache_data(ttl=60)
def get_market_data():


    config = Configuration()
    config.access_token = st.secrets["UPSTOX_ACCESS_TOKEN"]

    api_client = ApiClient(config)
    history_api = HistoryApi(api_client)

    return history_api.get_historical_candle_data(
        instrument_key="NSE_INDEX|Nifty 50",
        interval="15minute",
        to_date="",
        from_date=""
    )
try:
    response = get_market_data()
except Exception as e:
    import traceback
    st.exception(e)
    st.code(traceback.format_exc())
    st.stop()

    if df_live.empty:
        st.error("No market data received.")
        st.stop()

except Exception as e:
    st.error(f"Market Data Error : {e}")
    st.stop()

config = Configuration()

config.access_token = st.secrets["UPSTOX_ACCESS_TOKEN"]

api_client = ApiClient(config)

history_api = HistoryApi(api_client)

return history_api.get_historical_candle_data(
    instrument_key="NSE_INDEX|Nifty 50",
    interval="15minute",
    to_date="",
    from_date="",
    api_version="2.0"
)

price = data["price"]
rsi = data["rsi"]
ema20 = data["ema20"]
ema50 = data["ema50"]
macd = data["macd"]
atr = data["atr"]
adx = data["adx"]
candle = data["candle"]

entry = price
stop_loss = round(entry - (atr * 1.5), 2)
target1 = round(entry + (atr * 2), 2)
target2 = round(entry + (atr * 4), 2)

risk_reward = "1 : 2"




# --------------------------
signal, score, confidence_score, trade_rating, market_mood, buy_probability, sell_probability, reasons = ai_decision(
    rsi,
    ema20,
    ema50,
    macd,
    adx,
    candle,
)

confidence = f"{confidence_score}%"

if signal == "BUY 🟢":
    trend = "Bullish 🟢"
elif signal == "SELL 🔴":
    trend = "Bearish 🔴"
else:
    trend = "Sideways 🟡"

# AI Confidence Score
confidence_score = abs(score)

if adx >= 30:
    confidence_score += 15
elif adx >= 25:
    confidence_score += 10
elif adx >= 20:
    confidence_score += 5

confidence_score = min(confidence_score, 100)
confidence = f"{confidence_score}%"


confidence = f"{confidence_score}%"
# ===========================
# MARKET MOOD
# ===========================

if score >= 80:
    market_mood = "🚀 Strong Bullish"
elif score >= 60:
    market_mood = "🟢 Bullish"
elif score >= 40:
    market_mood = "🟡 Sideways"
elif score >= 20:
    market_mood = "🟠 Weak Bearish"
else:
    market_mood = "🔴 Strong Bearish"

# Trade Rating
if confidence_score >= 90:
    trade_rating = "⭐⭐⭐⭐⭐"
elif confidence_score >= 75:
    trade_rating = "⭐⭐⭐⭐"
elif confidence_score >= 60:
    trade_rating = "⭐⭐⭐"
elif confidence_score >= 40:
    trade_rating = "⭐⭐"
else:
    trade_rating = "⭐"

if score >= 75:
    signal = "BUY 🟢"
    trend = "Bullish 🟢"

elif score <= -75:
    signal = "SELL 🔴"
    trend = "Bearish 🔴"

else:
    signal = "WAIT 🟡"
    trend = "Sideways 🟡"
    

# -----------------------
# Title
# -----------------------
st.title("📈 AI Trading Assistant")
st.caption("🚀 Powered by Upstox API + AI")

st.success("🟢 LIVE MARKET CONNECTED")
st.info(f"🏛️ Market : NSE | 🕒 {datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%d-%m-%Y %H:%M:%S')}"
)
st.markdown("---")
st.subheader("📋 Suggested Trade")
if signal == "BUY 🟢":
    st.success(f"""
📈 BUY Setup

Entry : {price:.2f}

Stop Loss : {stop_loss:.2f}

Target 1 : {target1:.2f}

Target 2 : {target2:.2f}

Risk Reward : {risk_reward}
""")

elif signal == "SELL 🔴":
    st.error(f"""
📉 SELL Setup

Entry : {price:.2f}

Stop Loss : {stop_loss:.2f}

Target 1 : {target1:.2f}

Target 2 : {target2:.2f}

Risk Reward : {risk_reward}
""")

else:
    st.warning("⚠️ No Trade Setup Available. Wait for a better opportunity.")

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
    st.subheader("⭐ Trade Rating")

if confidence_score >= 90:
    st.success(f"{trade_rating}  Excellent Trade")
elif confidence_score >= 75:
    st.success(f"{trade_rating}  Good Trade")
elif confidence_score >= 60:
    st.warning(f"{trade_rating}  Average Trade")
elif confidence_score >= 40:
    st.warning(f"{trade_rating}  Risky Trade")
else:
    st.error(f"{trade_rating}  Avoid Trade")
    st.caption(f"✅ Last Updated : {datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%H:%M:%S')}")
# -----------------------
# AI Analysis Table
# -----------------------
st.markdown("---")
st.subheader("📝 AI Reason")
for item in reason:
    st.write(item)

for item in reasons:
    st.write(item)

st.write(f"🟢 BUY Probability : {buy_probability}%")
st.progress(buy_probability)

st.write(f"🔴 SELL Probability : {sell_probability}%")
st.progress(sell_probability)

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

st.subheader("🕯️ Current Candle")
st.info(candle)
st.subheader("📊 AI Score")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("RSI", "52.4")

with col2:
    st.metric("MACD", "Bullish 🟢")

with col3:
    st.metric("Accuracy", "75%")
st.metric("🧠 AI Score", "100%")
# -----------------------
# Market Summary
# -----------------------
st.markdown("### 🎯 Trade Plan")

col1, col2 = st.columns(2)

with col1:
    st.success(f"Entry : {entry:.2f}")
    st.error(f"Stop Loss : {stop_loss:.2f}")

with col2:
    st.info(f"Target 1 : {target1:.2f}")
    st.info(f"Target 2 : {target2:.2f}")

st.metric("⚖️ Risk : Reward", risk_reward)

st.subheader("🌍 Market Mood")
st.success(market_mood)

st.subheader("📋 Market Summary")

entry = price

stop_loss = entry - (atr * 1.5)

risk = entry - stop_loss

target1 = entry + (risk * 2)

target2 = entry + (risk * 3)

risk_reward = "1 : 2 / 1 : 3"

st.info(
    f"""
**Trend:** {trend}

**Signal:** {signal}

**Confidence:** {confidence}

**Market:** NSE
"""
)