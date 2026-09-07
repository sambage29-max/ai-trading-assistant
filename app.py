from datetime import datetime
import streamlit as st
import pandas as pd
import ta
import requests
from upstox_client import Configuration, ApiClient, HistoryApi

st.set_page_config(page_title="AI Trading System", layout="wide")
st.title("🚀 Personal AI Trading Dashboard")

st.sidebar.header("🔑 Upstox Credentials")
API_KEY = st.sidebar.text_input("Enter API Key:", type="password")
API_SECRET = st.sidebar.text_input("Enter API Secret:", type="password")
REDIRECT_URI = st.sidebar.text_input("Redirect URI:", value="http://localhost:8501")

if "access_token" not in st.session_state:
    st.session_state.access_token = None

if API_KEY and API_SECRET:
    auth_url = f"https://upstox.com{API_KEY}&redirect_uri={REDIRECT_URI}"
    st.sidebar.markdown(f"[🔗 Click here to Login & Authorize]({auth_url})")
    
    auth_code = st.sidebar.text_input("Paste Redirected URL Code (?code=):")
    
    if st.sidebar.button("⚙️ Generate Access Token") and auth_code:
        try:
            url = "https://upstox.com"
            headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
            payload = {
                'code': auth_code,
                'client_id': API_KEY,
                'client_secret': API_SECRET,
                'redirect_uri': REDIRECT_URI,
                'grant_type': 'authorization_code'
            }
            res = requests.post(url, headers=headers, data=payload).json()
            if "access_token" in res:
                st.session_state.access_token = res["access_token"]
                st.sidebar.success("🟢 Token Generated!")
            else:
                st.sidebar.error("Token generate nahi ho paya. Code check karein.")
        except Exception as e:
            st.sidebar.error(f"Error: {str(e)}")

def calculate_indicators(df):
    df["RSI"] = ta.momentum.rsi(close=df["Close"], window=14)
    df["EMA50"] = ta.trend.ema_indicator(close=df["Close"], window=50)
    df["ATR"] = ta.volatility.average_true_range(high=df["High"], low=df["Low"], close=df["Close"], window=14)
    return df

if st.session_state.access_token:
    ins_key = st.selectbox("Select Stock:", ["NSE_EQ|INE062A01020", "NSE_EQ|INE467B01029"])
    try:
        cfg = Configuration()
        cfg.access_token = st.session_state.access_token
        api = HistoryApi(ApiClient(cfg))
        res = api.get_historical_candle_data_v2(instrument_key=ins_key, interval="1minute", to_date="2026-09-08", from_date="2026-09-01")
        if res and res.status == "success":
            df = pd.DataFrame(res.data.candles, columns=["Date", "Open", "High", "Low", "Close", "Volume", "OI"])
            df["Date"] = pd.to_datetime(df["Date"])
            df = calculate_indicators(df.iloc[::-1].reset_index(drop=True))
            
            price = float(df["Close"].iloc[-1])
            rsi = float(df["RSI"].iloc[-1]) if not pd.isna(df["RSI"].iloc[-1]) else 50.0
            ema50 = float(df["EMA50"].iloc[-1]) if not pd.isna(df["EMA50"].iloc[-1]) else price
            atr = float(df["ATR"].iloc[-1]) if not pd.isna(df["ATR"].iloc[-1]) else (price * 0.01)
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Live Price", f"₹{price:.2f}")
            m2.metric("RSI", f"{rsi:.2f}")
            m3.metric("EMA 50", f"₹{ema50:.2f}")
            
            st.subheader("🤖 AI Trading Signal")
            if price > ema50 and rsi < 42:
                st.success(f"🟢 BUY ALERT | Entry: ₹{price:.2f} | SL: ₹{price-(2*atr):.2f} | Target: ₹{price+(4*atr):.2f}")
            elif price < ema50 and rsi > 68:
                st.error(f"🔴 SHORT/EXIT ALERT | Entry: ₹{price:.2f} | SL: ₹{price+(2*atr):.2f} | Target: ₹{price-(4*atr):.2f}")
            else:
                st.warning("⚪ HOLD | Neutral Zone")
            st.dataframe(df.tail(5))
    except Exception as e:
        st.error(f"Data error: {str(e)}")
else:
    st.info("💡 Sidebar me API credentials daal kar login link par click karein.")
