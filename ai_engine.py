import streamlit as st
import pandas as pd
import numpy as np
import pandas_ta as ta
import requests

# Page configuration
st.set_page_config(page_title="AI Trading Bot", layout="wide")
st.title("📈 AI Trading Dashboard (Upstox Powered)")

# Sidebar for API Configurations
st.sidebar.header("🔑 Authentication")
ACCESS_TOKEN = st.sidebar.text_input("Upstox Access Token", type="password", value="")
SYMBOL = st.sidebar.selectbox("Select Instrument", ["NSE_EQ|INE002A01018", "NSE_EQ|INE481G01011"]) # Reliance, Nifty, etc.
INTERVAL = st.sidebar.selectbox("Timeframe", ["1minute", "5minute", "30minute", "day"])

# 1. Fetch Data Function
def fetch_historical_data(token, instrument_token, interval):
    if not token:
        st.warning("Please enter your Upstox Access Token in the sidebar.")
        return pd.DataFrame()
    
    # Hypothetical layout for Upstox Historical Data V2 API
    url = f"https://upstox.com{instrument_token}/{interval}/2026-09-08/2026-08-01"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_size == 200:
            data = response.json()['data']['candles']
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'oi'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df.iloc[::-1].reset_index(drop=True) # Chronological order
        else:
            st.error(f"API Error: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return pd.DataFrame()

# Execution UI
if ACCESS_TOKEN:
    st.info("Fetching real-time market matrix...")
    df = fetch_historical_data(ACCESS_TOKEN, SYMBOL, INTERVAL)
    
    if not df.empty:
        # 2. Mathematical Indicator Processing (Fixing Data Alignment Errors)
        df['RSI'] = ta.rsi(df['close'], length=14)
        macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
        df = pd.concat([df, macd], axis=1)
        
        # 3. AI Trading Rule Engine
        df['Signal'] = "HOLD"
        # Buy Logic: RSI Oversold (<30) & MACD Line crosses above Signal Line
        df.loc[(df['RSI'] < 30) & (df['MACD_12_26_9'] > df['MACDs_12_26_9']), 'Signal'] = "BUY"
        # Sell Logic: RSI Overbought (>70)
        df.loc[(df['RSI'] > 70), 'Signal'] = "SELL"
        
        # Metric Layout Show
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Latest Close", f"₹{latest['close']}", f"{round(latest['close']-prev['close'], 2)}")
        col2.metric("RSI (14)", f"{round(latest['RSI'], 2)}")
        col3.metric("Current Signal", f"🚨 {latest['Signal']}")
        col4.metric("Data Points Loaded", len(df))
        
        # Display Table
        st.subheader("📊 Recent Market Feed & Generated Signals")
        st.dataframe(df.tail(15)[['timestamp', 'open', 'high', 'low', 'close', 'RSI', 'Signal']])
else:
    st.write("👈 Access Token dalkar connection execute karein.")
