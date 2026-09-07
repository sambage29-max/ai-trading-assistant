from datetime import datetime
import streamlit as st
import pandas as pd
import ta
import requests
from upstox_client import Configuration, ApiClient, HistoryApi

# --- Page Initialization ---
st.set_page_config(page_title="AI Trading System - Upstox V2", layout="wide")
st.title("🚀 Personal AI Trading Dashboard (Upstox Live)")

# --- Sidebar Configuration Panel ---
st.sidebar.header("🔑 Upstox Credentials")
API_KEY = st.sidebar.text_input("Enter API Key:", value="", type="password")
API_SECRET = st.sidebar.text_input("Enter API Secret:", value="", type="password")
REDIRECT_URI = st.sidebar.text_input("Redirect URI:", value="http://localhost:8501")

# State Management for Access Token
if "access_token" not in st.session_state:
    st.session_state.access_token = None

# --- Step 1: Login URL Generator ---
if API_KEY and API_SECRET:
    # Authorization Code generate karne ka standard OAuth URL
    auth_url = f"https://upstox.com{API_KEY}&redirect_uri={REDIRECT_URI}"
    st.sidebar.markdown(f"[🔗 Click here to Login & Authorize]({auth_url})")
    
    # Login karne ke baad URL me mila '?code=XXXX' yahan daalein
    auth_code = st.sidebar.text_input("Paste Redirected URL Code (?code=):")
    
    if st.sidebar.button("⚙️ Generate Access Token") and auth_code:
        try:
            # Token Exchange Payload Architecture
            url = "https://upstox.com"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'code': auth_code,
                'client_id': API_KEY,
                'client_secret': API_SECRET,
                'redirect_uri': REDIRECT_URI,
                'grant_type': 'authorization_code'
            }
            
            response = requests.post(url, headers=headers, data=data)
            res_data = response.json()
            
            if "access_token" in res_data:
                st.session_state.access_token = res_data["access_token"]
                st.sidebar.success("🟢 Active Access Token Retrieved Successfully!")
            else:
                st.sidebar.error(f"Token generation failed: {res_data.get('errors', [{}])[0].get('message', 'Unknown Error')}")
        except Exception as e:
            st.sidebar.error(f"Connection Error: {str(e)}")

# --- Indicator Engine (High Win Probability Math) ---
def calculate_advanced_indicators(df):
    if df.empty:
        return df
    df["RSI"] = ta.momentum.rsi(close=df["Close"], window=14)
    df["EMA20"] = ta.trend.ema_indicator(close=df["Close"], window=20)
    df["EMA50"] = ta.trend.ema_indicator(close=df["Close"], window=50)
    df["ATR"] = ta.volatility.average_true_range(high=df["High"], low=df["Low"], close=df["Close"], window=14)
    return df

# --- Fetch Dynamic Upstox Stream ---
def fetch_live_market_data(token, instrument_key):
    try:
        config = Configuration()
        config.access_token = token
        api_client = ApiClient(config)
        history_api = HistoryApi(api_client)
        
        api_response = history_api.get_historical_candle_data_v2(
            instrument_key=instrument_key,
            interval="1minute",
            to_date="2026-09-08",
            from_date="2026-09-01"
        )
        
        if api_response and api_response.status == "success":
            candles = api_response.data.candles
            columns = ["Date", "Open", "High", "Low", "Close", "Volume", "OI"]
            df = pd.DataFrame(candles, columns=columns)
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.iloc[::-1].reset_index(drop=True)
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Market Stream Error: {str(e)}")
        return pd.DataFrame()

# --- Core Run Execution Block ---
if st.session_state.access_token:
    instrument_symbol = st.selectbox("Select Trade Instrument:", ["NSE_EQ|INE062A01020", "NSE_EQ|INE467B01029"]) # SBIN, TCS
    
    with st.spinner("Streaming Live Data from Upstox Server..."):
        raw_data = fetch_live_market_data(st.session_state.access_token, instrument_symbol)
        
    if not raw_data.empty:
        data = calculate_advanced_indicators(raw_data)
        
        # Latest Matrix Extraction
        price = float(data["Close"].iloc[-1])
        rsi = float(data["RSI"].iloc[-1]) if not pd.isna(data["RSI"].iloc[-1]) else 50.0
        ema50 = float(data["EMA50"].iloc[-1]) if not pd.isna(data["EMA50"].iloc[-1]) else price
        atr = float(data["ATR"].iloc[-1]) if not pd.isna(data["ATR"].iloc[-1]) else (price * 0.01)
        
        # Metrics UI Layout Grid
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Live Market Price", f"₹{price:.2f}")
        m2.metric("RSI (14)", f"{rsi:.2f}")
        m3.metric("Trend Filter (EMA 50)", f"₹{ema50:.2f}")
        m4.metric("Volatility (ATR)", f"₹{atr:.2f}")
        
        # Win-Probability Signal Core
        st.subheader("🤖 AI Algorithmic Signal Execution")
        stop_loss_value = price - (2 * atr)
        target_value = price + (4 * atr)

        if price > ema50 and rsi < 42:
            st.success(f"🟢 HIGH PROBABILITY BUY SIGNAL | Entry: ₹{price:.2f} | Stop-Loss (2*ATR): ₹{stop_loss_value:.2f} | Target (4*ATR): ₹{target_value:.2f}")
        elif price < ema50 and rsi > 68:
            st.error(f"🔴 SHORT/EXIT SIGNAL | Entry: ₹{price:.2f} | Stop-Loss: ₹{price + (2*atr):.2f} | Target: ₹{price - (4*atr):.2f}")
        else:
            st.warning("⚪ HOLD | Trend and Momentum filters are neutral. Waiting for high probability zone.")
            
        st.subheader("📊 Live Technical Matrix")
        st.dataframe(data.tail(10))
else:
    st.info("💡 App ko active karne ke liye sidebar me apni API Key aur Secret daal kar authorization flow complete karein.")
