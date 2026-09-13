import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from indicators import calculate_advanced_indicators
from ai_engine import generate_trading_signal

st.set_page_config(page_title="AI Trading Intelligence Suite", layout="wide", initial_sidebar_state="expanded")

st.title("🛡️ Institutional AI Trading System")
st.caption("Advanced Real-time Analytics Engine featuring Multi-Indicator Convergence Model")

# Sidebar configurations
st.sidebar.markdown("### 🎛️ Terminal Controls")
ticker = st.sidebar.text_input("Asset Ticker (e.g., RELIANCE.NS, TSLA, BTC-USD):", value="RELIANCE.NS").strip().upper()
interval = st.sidebar.selectbox("Execution Frequency (Interval):", ["1m", "5m", "15m", "1h", "1d"], index=2)
period = st.sidebar.selectbox("Lookback Window (Period):", ["1d", "5d", "1mo", "3mo", "1y"], index=2)

if st.sidebar.button("⚡ Execute Live Analysis", use_container_width=True):
    with st.spinner("Connecting to live exchanges & running AI matrices..."):
        try:
            df = yf.download(tickers=ticker, period=period, interval=interval, progress=False)
            
            if df.empty:
                st.error("❌ Data Engine Error: Invalid symbol or no liquid volume found for selection.")
            else:
                # Engine Pipeling
                df = calculate_advanced_indicators(df)
                trade_setup = generate_trading_signal(df)
                
                latest_row = df.iloc[-1]
                
                # Metric Grid
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Live LTP", f"₹{latest_row['Close']:.2f}")
                
                sig = trade_setup['signal']
                sig_color = "🟢" if "BUY" in sig else "🔴" if "SELL" in sig else "⚪"
                m2.metric("System Verdict", f"{sig_color} {sig}")
                
                m3.metric("🎯 Calculated Target", f"₹{trade_setup['target']:.2f}" if trade_setup['target'] > 0 else "N/A")
                m4.metric("🛑 System Stoploss", f"₹{trade_setup['sl']:.2f}" if trade_setup['sl'] > 0 else "N/A")
                
                # Logic justification box
                st.info(f"**Engine Framework Logs:** {trade_setup['reason']}")
                
                # High-fidelity Interactive Charts
                fig = go.Figure()
                fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Price Action'))
                fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], line=dict(color='rgba(173,216,230,0.5)', width=1), name='BB Upper'))
                fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], line=dict(color='rgba(173,216,230,0.5)', width=1), name='BB Lower'))
                
                fig.update_layout(template="plotly_dark", height=550, xaxis_rangeslider_visible=False, margin=dict(l=20, r=20, t=30, b=20))
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"Critical Runtime Exception: {str(e)}")
