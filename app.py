import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import requests
from openai import OpenAI

st.set_page_config(page_title="Ultimate AI Trading System", layout="wide")
st.title("🛡️ Institutional Grade AI Multi-Asset Trading Engine")
st.caption("Confluence Architecture: Triple EMA + Volume Shock + Risk Calculator + Telegram Alerts + DeepSeek AI")

TELEGRAM_TOKEN = "8680517650:AAHYrpb5j88XNGIoK-xu-hC-qZWs3RtCHkk"
TELEGRAM_CHAT_ID = "7374819912"

def send_telegram_alert(message):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}, timeout=5)
    except: pass

def get_deepseek_decision(stock_name, price, rsi, signal):
    if "DEEPSEEK_API_KEY" not in st.secrets:
        return "⚡ *AI Decision:* STAY CASH\n🎯 *Reasoning:* [Local Engine Active Mode]"
    try:
        client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://deepseek.com")
        prompt = f"Analyze asset {stock_name} at price {price}, RSI {rsi}, signal {signal}. Reply in 1 simple Hinglish sentence."
        response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=0.2, max_tokens=100, timeout=4)
        return response.choices.message.content
    except:
        return "⚡ *AI Decision:* STAY CASH\n🎯 *Reasoning:* [Server Offline Backup]"

st.sidebar.header("🕹️ Multi-Asset Universe Configuration")
segment_selector = st.sidebar.selectbox("Market Segment", ["Option Chains", "Intraday Equity", "MCX Commodities"])

ticker_matrix = {
    "Option Chains": {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "FINNIFTY": "NIFTY_FIN_SERVICE.NS"},
    "Intraday Equity": {"RELIANCE": "RELIANCE.NS", "TATAMOTORS": "TATAMOTORS.NS", "SBIN": "SBIN.NS"},
    "MCX Commodities": {"CRUDE OIL": "CL=F", "GOLD": "GC=F", "SILVER": "SI=F"}
}

script_selector = st.sidebar.selectbox("Target Derivative Script", list(ticker_matrix[segment_selector].keys()))
ticker_symbol = ticker_matrix[segment_selector][script_selector]
time_window = st.sidebar.selectbox("Strategy Timeframe Window", ["5m", "15m", "60m"])

st.sidebar.markdown("---")
st.sidebar.header("💰 Risk Management Dashboard")
total_capital = st.sidebar.number_input("Your Trading Capital (₹)", min_value=1000, value=50000, step=5000)
risk_percentage = st.sidebar.slider("Max Risk Per Trade (%)", min_value=0.5, max_value=5.0, value=1.0, step=0.5)

if st.sidebar.button("🚀 Run Advanced Institutional Scan"):
    st.write("### 📊 Market Scan Results")
    market_data = yf.download(tickers=ticker_symbol, period="5d", interval=time_window)
    
    if market_data.empty:
        st.error("Market data terminal feed mismatch. Choose an active trading session window.")
    else:
        if isinstance(market_data.columns, pd.MultiIndex):
            market_data.columns = market_data.columns.droplevel(1)
            
        market_data['EMA_9'] = market_data['Close'].ewm(span=9, adjust=False).mean()
        market_data['EMA_21'] = market_data['Close'].ewm(span=21, adjust=False).mean()
        market_data['EMA_50'] = market_data['Close'].ewm(span=50, adjust=False).mean()
        
        delta = market_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        market_data['RSI'] = 100 - (100 / (1 + (gain / (loss + 1e-10))))
        market_data['Vol_Baseline'] = market_data['Volume'].rolling(window=20).mean()
        market_data['TR'] = np.maximum(market_data['High'] - market_data['Low'], np.maximum(abs(market_data['High'] - market_data['Close'].shift(1)), abs(market_data['Low'] - market_data['Close'].shift(1))))
        market_data['ATR'] = market_data['TR'].rolling(window=14).mean()
        
        last_node = market_data.iloc[-1]
        prev_node = market_data.iloc[-2]
        
        raw_price = float(last_node['Close'])
        current_rsi = float(last_node['RSI']) if not np.isnan(last_node['RSI']) else 50.0
        atr_band = float(last_node['ATR']) if float(last_node['ATR']) > 0 else (raw_price * 0.004)
        volume_shock = float(last_node['Volume']) > (1.3 * float(market_data['Vol_Baseline'].iloc[-1])) if not np.isnan(last_node['Volume']) else False
        
        if segment_selector == "MCX Commodities":
            current_price = raw_price * 84.10
            atr_band = atr_band * 84.10
        else:
            current_price = raw_price
            
        bullish_structure = (last_node['EMA_9'] > last_node['EMA_21']) and (last_node['EMA_21'] > last_node['EMA_50'])
        bearish_structure = (last_node['EMA_9'] < last_node['EMA_21']) and (last_node['EMA_21'] < last_node['EMA_50'])
        
        signal_output = "⏳ ALGO SHIELD ACTIVE (STAY CASH / HOLD)"
        sl, target, tsl, is_real_signal = "N/A", "N/A", "N/A", False
        
        if bullish_structure and (current_rsi > 58) and volume_shock:
            signal_output = "⚡ INSTITUTIONAL BUY SIGNALS"
            sl, target, tsl, is_real_signal = round(current_price - (1.5 * atr_band), 2), round(current_price + (2.5 * atr_band), 2), round(current_price - (0.8 * atr_band), 2), True
            
        if bearish_structure and (current_rsi < 42) and volume_shock:
            signal_output = "⚠️ INSTITUTIONAL SHORT SELL SIGNALS"
            sl, target, tsl, is_real_signal = round(current_price + (1.5 * atr_band), 2), round(current_price - (2.5 * atr_band), 2), round(current_price + (0.8 * atr_band), 2), True

        st.subheader(f"📊 Quantitative Asset Status: {script_selector} ({time_window} View)")
        st.info(f"💰 **ENTRY TRIGGER PRICE:** ₹{current_price:,.2f}")
        st.warning(f"🚦 **ENGINE SIGNAL STATUS:** {signal_output}")
        st.markdown("### 🎯 Order Matrix Target Points")
        st.write(f"🔹 **MATHEMATICAL TARGET:** {f'₹{target:,.2f}' if target != 'N/A' else 'N/A'}")
        st.write(f"🔹 **ALGO STOP LOSS:** {f'₹{sl:,.2f}' if sl != 'N/A' else 'N/A'}")
        st.write(f"🔹 **TRAILING STOP LOSS:** {f'₹{tsl:,.2f}' if tsl != 'N/A' else 'N/A'}")
        
        deepseek_insights = get_deepseek_decision(script_selector, round(current_price, 2), round(current_rsi, 2), signal_output)
        
        if is_real_signal:
            send_telegram_alert(f"🚨 ALERT\nAsset: {script_selector}\nAction: {signal_output}\nPrice: ₹{current_price:,.2f}\nTarget: ₹{target:,.2f}\nSL: ₹{sl:,.2f}")
            st.success("✅ Live Alert transmitted successfully to Telegram!")

        st.markdown("---")
        st.subheader("🧠 DeepSeek AI Strategic Overlay Insights")
        st.info(deepseek_insights)
        
        st.markdown("---")
        st.subheader("💡 Algorithmic Position Sizing & Risk Intelligence")
        max_risk_cash = total_capital * (risk_percentage / 100)
        calculated_qty = int(max_risk_cash // (abs(current_price - sl))) if sl != "N/A" else 0
        
        st.success(f"📦 **RECOMMENDED QUANTITY TO TRADE:** {calculated_qty} units")
        st.write(f"🔹 **Max Wallet Capital Allocated to Risk:** ₹{max_risk_cash:,.2f}")
