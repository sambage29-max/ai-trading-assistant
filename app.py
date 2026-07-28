import streamlit as st
import requests
ACCESS_TOKEN = st.secrets["UPSTOX_ACCESS_TOKEN"]

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

st.set_page_config(
    page_title="AI Trading Assistant",
    page_icon="📈"
)

st.title("📈 AI Trading Assistant")

st.success("Step 1 Successful ✅")

st.write("Token loaded successfully ✅")
st.write(ACCESS_TOKEN[:10] + "...")
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

st.write("Status Code:", response.status_code)

try:
    st.json(response.json())
except Exception:
    st.write(response.text)
