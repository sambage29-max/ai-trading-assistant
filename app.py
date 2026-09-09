import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np

# Page configuration
st.set_page_config(page_title="AI Multi-Asset Signal Generator", layout="wide")
st.title("📈 AI Trading Signal Engine (Intraday, Options & MCX)")
st.caption("Live mathematical signals with entry, exit, target, and stop-loss rules.")

# Technical Indicator Calculations
def calculate_indicators(df):
    # 1. RSI Calculation
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / (loss + 1e-10)
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # 2. Moving Averages for Trend Filtering
    df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
    
    # 3. Mathematical Stop-Loss & Target Anchors (ATR proxy via rolling volatility)
    df['Volatility'] = df['Close'].rolling(window=14).std()
    return df

# Machine Learning Rule Engine for Maximum Success Probability
def generate_ai_signals(df):
    df = calculate_indicators(df)
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]
    
    close = last_row['Close']
    rsi = last_row['RSI']
    vol = last_row['Volatility'] if last_row['Volatility'] > 0 else (close * 0.005)
    
    # Mathematical anchors for risk management
    stop_loss_buy = round(close - (1.5 * vol), 2)
    target_buy = round(close + (2.5 * vol), 2)
    
    stop_loss_sell = round(close + (1.5 * vol), 2)
    target_sell = round(close - (2.5 * vol), 2)
    
    # High-probability Logic: Trend Aligning + Momentum Confirmation
    if (last_row['EMA_20'] > last_row['EMA_50']) and (rsi > 50 and prev_row['RSI'] <= 50):
        return "⚡ STRONG BUY SIGNAL", close, target_buy, stop_loss_buy, rsi
    elif (last_row['EMA_20'] < last_row['EMA_50']) and (rsi < 50 and prev_row['RSI'] >= 50):
        return "⚠️ STRONG SELL SIGNAL", close, target_sell, stop_loss_sell, rsi
    else:
        return "⏳ NO CLEAR SIGNAL (🔴 HOLD)", close, "N/A", "N/A", rsi

# Sidebar Inputs for Asset Classes
st.sidebar.header("🕹️ Select Asset Universe")
asset_type = st.sidebar.selectbox("Market Segment", ["Intraday Equity", "MCX Commodities", "Option Chains Indices"])

ticker_dict = {
    "Intraday Equity": {"RELIANCE": "RELIANCE.NS", "TATA MOTORS": "TATAMOTORS.NS", "SBI": "SBIN.NS"},
    "MCX Commodities": {"CRUDE OIL": "CL=F", "GOLD": "GC=F", "SILVER": "SI=F"},
    "Option Chains Indices": {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK"}
}

selected_asset = st.sidebar.selectbox("Select Script", list(ticker_dict[asset_type].keys()))
ticker_symbol = ticker_dict[asset_type][selected_asset]

timeframe = st.sidebar.selectbox("Intraday Interval", ["5m", "15m", "60m"])

# Data Fetching & Execution
if st.sidebar.button("⚡ Generate Live AI Signals"):
    with st.spinner(f"Fetching real-time mathematical feeds for {selected_asset}..."):
        try:
            # Fetching fresh data using yfinance without API constraints
            data = yf.download(tickers=ticker_symbol, period="5d", interval=timeframe)
            
            if not data.empty:
                # Standardizing multi-index columns if any
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.droplevel(1)
                
                signal, entry, target, sl, current_rsi = generate_ai_signals(data)
                
                # Visual Dashboard Display
                st.subheader(f"📊 Live Signal Dashboard: {selected_asset} ({timeframe} View)")
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("CURRENT PRICE (ENTRY)", f"₹{entry:.2f}")
                col2.metric("AI SIGNAL STATUS", signal)
                col3.metric("MATHEMATICAL TARGET", f"₹{target}" if target != "N/A" else "N/A")
                col4.metric("STRICT STOP LOSS", f"₹{sl}" if sl != "N/A" else "N/A")
                
                st.info(f"💡 **Success Probability Anchor:** Current RSI Momentum sits at **{current_rsi:.2f}**. Rules enforce entries only when short-term momentum aligns with structural moving average crossovers.")
                
                # Show Raw Market State Data
                with st.expander("👀 View Back-end Live Feed (Last 5 Candlesticks)"):
                    st.dataframe(data.tail(5))
            else:
                st.error("Market data feeds are currently empty. Please verify the asset class interval.")
        except Exception as e:
            st.error(f"Failed to compile structural mathematical model matrix. Error: {str(e)}")
else:
    st.warning("👈 Please click the 'Generate Live AI Signals' button in the sidebar to start calculations.")
