import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="AI Trading Assistant",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI Trading Assistant")
st.caption("Powered by Upstox API")

ACCESS_TOKEN = st.secrets["UPSTOX_ACCESS_TOKEN"]

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

st.sidebar.header("Settings")

market = st.sidebar.selectbox(
    "Market",
    [
        "NIFTY",
        "BANKNIFTY"
    ]
)

refresh = st.sidebar.button("Refresh")

st.subheader("Live Market Dashboard")

price_placeholder = st.empty()
signal_placeholder = st.empty()
status_placeholder = st.empty()

def get_market_quote(instrument_key):

    url = "https://api.upstox.com/v2/market-quote/quotes"

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            params={
                "instrument_key": instrument_key
            },
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

        return {
            "error": response.text
        }

    except Exception as e:

        return {
            "error": str(e)
        }
        def get_instrument_key(market):

    if market == "NIFTY":
        return "NSE_INDEX|Nifty 50"

    if market == "BANKNIFTY":
        return "NSE_INDEX|Nifty Bank"

    return "NSE_INDEX|Nifty 50"


instrument = get_instrument_key(market)

data = get_market_quote(instrument)

ltp = None

if "error" not in data:

    try:

        market_data = data["data"][instrument]

        if "last_price" in market_data:
            ltp = market_data["last_price"]

        elif "ltp" in market_data:
            ltp = market_data["ltp"]

    except Exception as e:

        status_placeholder.error(f"Parsing Error : {e}")

else:

    status_placeholder.error(data["error"])


if ltp is not None:

    price_placeholder.metric(
        label=f"{market} Live Price",
        value=f"{ltp}"
    )

else:

    price_placeholder.warning(
        "Live price not available."
        signal = "WAIT"

if ltp is not None:

    if market == "NIFTY":

        if ltp > 25000:
            signal = "BUY"
        elif ltp < 24800:
            signal = "SELL"
        else:
            signal = "WAIT"

    elif market == "BANKNIFTY":

        if ltp > 57000:
            signal = "BUY"
        elif ltp < 56500:
            signal = "SELL"
        else:
            signal = "WAIT"

if signal == "BUY":
    signal_placeholder.success("🟢 AI Signal : BUY")

elif signal == "SELL":
    signal_placeholder.error("🔴 AI Signal : SELL")

else:
    signal_placeholder.info("🟡 AI Signal : WAIT")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.write("### Current Market")
    st.write(market)

with col2:
    st.write("### Last Updated")
    st.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    )st.divider()

st.subheader("API Status")

if "error" in data:

    st.error("❌ Upstox API Error")

    st.code(data["error"])

else:

    st.success("✅ Connected to Upstox API")


st.divider()

st.subheader("Raw API Response")

with st.expander("Show JSON Response"):

    st.json(data)


st.divider()

st.caption("AI Trading Assistant V2")

st.caption("Developed with Streamlit + Upstox API")

if refresh:
    st.rerun()
