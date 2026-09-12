import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.set_page_config(page_title="AI Trading Assistant", layout="wide")
st.title("🤖 AI Delivery & Intraday Signal Screener")
st.write("Standard Parameters par profitable setups filter karein")

# Nifty Tickers List (Examples)
WATCHLIST = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "TATAMOTORS.NS", "SBIN.NS", "BHARTIARTL.NS"]

def get_signals(ticker):
    try:
        # Fetching historical daily data
        data = yf.download(ticker, period="1y", interval="1d", progress=False)
        if data.empty or len(data) < 50:
            return None
        
        # Standard Technical Indicators
        data['RSI'] = ta.rsi(data['Close'], length=14)
        data['SMA_50'] = ta.sma(data['Close'], length=50)
        data['SMA_200'] = ta.sma(data['Close'], length=200)
        data['Avg_Volume'] = data['Volume'].rolling(window=20).mean()
        
        # Latest values
        last_row = data.iloc[-1]
        prev_row = data.iloc[-2]
        price = round(float(last_row['Close']), 2)
        rsi = round(float(last_row['RSI']), 2)
        volume = float(last_row['Volume'])
        avg_vol = float(last_row['Avg_Volume'])
        
        # Strategy Logic Setup
        signal = "HOLD / NEUTRAL"
        reason = "No strong pattern found"
        target = 0.0
        stop_loss = 0.0
        
        # Bullish Breakout Condition (Profitable Setup Rule)
        if rsi > 40 and rsi < 65 and price > float(last_row['SMA_50']) and volume > (avg_vol * 1.5):
            signal = "🚀 BUY (Delivery / Breakout)"
            reason = "Volume breakout with price staying above 50 SMA. RSI displays strong momentum."
            target = round(price * 1.05, 2)  # 5% Target
            stop_loss = round(price * 0.96, 2)  # 4% Stop-loss
            
        elif rsi > 70:
            signal = "⚠️ OVERBOUGHT (Caution)"
            reason = "RSI is in highly overbought territory. Potential reversal zone."
            
        return {
            "Ticker": ticker, "Price": price, "RSI": rsi, 
            "Signal": signal, "Reason": reason, "Target": target, "Stop Loss": stop_loss
        }
    except Exception as e:
        return None

# Trigger Scanner in App
if st.button("Start AI Market Scan"):
    results = []
    with st.spinner("Analyzing standard parameters..."):
        for stock in WATCHLIST:
            res = get_signals(stock)
            if res:
                results.append(res)
                
    if results:
        df = pd.DataFrame(results)
        st.dataframe(df.style.highlight_max(axis=0, subset=['Signal']))
    else:
        st.error("Data fetch error or market closed sync issue.")
