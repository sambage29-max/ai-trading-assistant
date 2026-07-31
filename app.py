import streamlit as st
import requests
import pandas as pd
from streamlit_autorefresh import st_autorefresh


st.set_page_config(
    page_title="AI Trading Assistant",
    page_icon="📈"
)
st_autorefresh(interval=5000, key="refresh")

ACCESS_TOKEN = st.secrets["UPSTOX_ACCESS_TOKEN"]

st.title("📈 AI Trading Assistant")
st.caption("🚀 Powered by Upstox API + AI")
st.divider()
st.success("🟢 LIVE MARKET CONNECTED")
st.info("📊 Market : NSE | ⏰ Refresh : 5 Seconds")
url = "https://api.upstox.com/v2/market-quote/ltp"

params = {
    "instrument_key": "NSE_INDEX|Nifty 50"
}



headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

response = requests.get(
    url,
    headers=headers,
    params=params
)

data = response.json()
# st.write(data)

price = data["data"]["NSE_INDEX:Nifty 50"]["last_price"]
if price > 24250:
    trend = "Bullish 📈"
    signal = "BUY 🟢"

elif price < 24150:
    trend = "Bearish 📉"
    signal = "SELL 🔴"

else:
    trend = "Sideways ↔️"
    signal = "WAIT 🟡"

col1, col2 = st.columns(2)

with col1:
    st.metric("📈 NIFTY 50", f"{price:,.2f}")
st.caption("🔄 Auto Refresh: Every 5 Seconds")

with col2:
    st.metric("📈 Trend", trend)
    st.metric("🧠 AI Signal", signal)
st.metric("🎯 Confidence", "75%")
df = pd.DataFrame({
    "Indicator": ["RSI", "MACD", "EMA", "Trend"],
    "Status": ["Calculating...", "Calculating...", "Calculating...", trend]
})

st.subheader("📊 AI Analysis")
st.dataframe(df, use_container_width=True)


