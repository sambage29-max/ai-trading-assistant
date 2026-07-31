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
st.success("Step 1 Complete ✅")
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
    st.metric("📈 NIFTY 50", price)

with col2:
    st.metric("📈 Trend", trend)
    st.metric("🧠 AI Signal", signal)
df = pd.DataFrame({
    "Indicator": ["RSI", "MACD", "EMA"],
    "Status": ["Neutral", "Bullish", "Bullish"]
})

st.subheader("📊 AI Analysis")
st.dataframe(df, use_container_width=True)


