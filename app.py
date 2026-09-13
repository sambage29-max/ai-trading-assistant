import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from ta.momentum import RSIIndicator
from ta.trend import MACD

# Page configuration
st.set_page_config(page_title="AI Live Trading Assistant", layout="wide")

st.title("📈 Advanced Live Trading Assistant")
st.write("World-class indicators (RSI & MACD) के आधार पर लाइव सिग्नल्स और टारगेट्स देखें।")

# Sidebar for inputs
st.sidebar.header("📊 Trading Setup")
ticker = st.sidebar.text_input("Stock Ticker Symbol (e.g., RELIANCE.NS, AAPL, BTC-USD):", value="RELIANCE.NS")
interval = st.sidebar.selectbox("Time Interval:", options=["1m", "5m", "15m", "1h", "1d"], index=2)
period = st.sidebar.selectbox("Data Period:", options=["1d", "5d", "1mo", "3mo", "1y"], index=1)

# Fetch Data Button
if st.sidebar.button("Generate Live Targets"):
    with st.spinner("Fetching live market data and calculating targets..."):
        try:
            # 1. Load Data from yfinance
            data = yf.download(tickers=ticker, period=period, interval=interval)
            
            if data.empty:
                st.error("कोई डेटा नहीं मिला। कृपया सही Ticker सिंबल डालें (जैसे NSE के लिए स्टॉक के अंत में .NS लगाएं)।")
            else:
                # Clean columns (handling multi-index if any)
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.droplevel(1)
                
                # 2. Calculate World-Class Indicators
                # RSI Calculation
                rsi_series = RSIIndicator(close=data['Close'], window=14).rsi()
                data['RSI'] = rsi_series
                
                # MACD Calculation
                macd_obj = MACD(close=data['Close'])
                data['MACD'] = macd_obj.macd()
                data['MACD_Signal'] = macd_obj.macd_signal()
                
                # Get the latest row for live signaling
                latest_data = data.iloc[-1]
                current_price = float(latest_data['Close'])
                latest_rsi = float(latest_data['RSI'])
                latest_macd = float(latest_data['MACD'])
                latest_macd_sig = float(latest_data['MACD_Signal'])
                
                # 3. Trading Logic & Signal Generation
                signal = "HOLD"
                target = 0.0
                stop_loss = 0.0
                color = "white"
                
                # Bullish Condition (Buy)
                if latest_rsi < 40 and latest_macd > latest_macd_sig:
                    signal = "BUY"
                    stop_loss = current_price * 0.985  # 1.5% StopLoss
                    target = current_price * 1.03      # 3% Target
                    color = "#2ecc71"
                    
                # Bearish Condition (Sell)
                elif latest_rsi > 60 and latest_macd < latest_macd_sig:
                    signal = "SELL / SHORT"
                    stop_loss = current_price * 1.015  # 1.5% StopLoss
                    target = current_price * 0.97      # 3% Target
                    color = "#e74c3c"
                
                # 4. Display Results Dashboard
                st.subheader(f"🎯 Live Signal for {ticker.upper()}")
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric(label="Current Live Price", value=f"₹{current_price:.2f}")
                
                with col2:
                    st.markdown(f"**Current Signal:** <span style='color:{color}; font-size:20px; font-weight:bold;'>{signal}</span>", unsafe_allow_html=True)
                
                if signal != "HOLD":
                    col3.metric(label="🎯 Predicted Target", value=f"₹{target:.2f}")
                    col4.metric(label="🛑 Strict Stoploss", value=f"₹{stop_loss:.2f}")
                else:
                    col3.write("मार्केट न्यूट्रल है। सही एंट्री का इंतज़ार करें।")
                
                # Indicator Stats Info
                st.info(f"💡 Technical Stats -> RSI: {latest_rsi:.2f} | MACD: {latest_macd:.4f} | MACD Signal: {latest_macd_sig:.4f}")
                
                # 5. Interactive Charting
                st.subheader("📈 Live Technical Chart")
                fig = go.Figure()
                
                # Candlestick chart
                fig.add_trace(go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name='Market Price'
                ))
                
                fig.update_layout(
                    title=f"{ticker} Price Chart with Indicators",
                    yaxis_title="Price",
                    xaxis_title="Time",
                    template="plotly_dark",
                    xaxis_rangeslider_visible=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"App Execution Error: {str(e)}")
            st.warning("कृपया सुनिश्चित करें कि आपका इंटरनेट एक्टिव है और टिकर फॉर्मेट सही है।")
