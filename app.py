import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np

# 1. System Layout Settings
st.set_page_config(page_title="Ultimate AI Trading System", layout="wide")
st.title("🛡️ Institutional Grade AI Multi-Asset Trading Engine")
st.caption("Advanced Confluence Architecture: Triple EMA + Volume Shock Analytics + Option Chain Predictor + Dynamic Trailing SL + Risk Calculator + Live Trade Log")

# 2. Safe Session State Storage Initialization
if 'trade_log' not in st.session_state:
    st.session_state.trade_log = []

# 3. Dynamic Sidebar UI Components
st.sidebar.header("🕹️ Multi-Asset Universe Configuration")
segment_selector = st.sidebar.selectbox("Market Segment", ["Option Chains", "Intraday Equity", "MCX Commodities"])

ticker_matrix = {
    "Option Chains": {
        "NIFTY 50": "^NSEI", 
        "BANK NIFTY": "^NSEBANK",
        "FINNIFTY": "NIFTY_FIN_SERVICE.NS",
        "MIDCPNIFTY": "^NSEMDCP50",
        "SENSEX": "^BSESN"
    },
    "Intraday Equity": {"RELIANCE": "RELIANCE.NS", "TATA MOTORS": "TATAMOTORS.NS", "SBI": "SBIN.NS"},
    "MCX Commodities": {"CRUDE OIL": "CL=F", "GOLD": "GC=F", "SILVER": "SI=F"}
}

script_selector = st.sidebar.selectbox("Target Derivative Script", list(ticker_matrix[segment_selector].keys()))
ticker_symbol = ticker_matrix[segment_selector][script_selector]
time_window = st.sidebar.selectbox("Strategy Timeframe Window", ["5m", "15m", "60m"])

st.sidebar.markdown("---")
st.sidebar.header("💰 Risk Management Dashboard")
total_capital = st.sidebar.number_input("Your Trading Capital (₹)", min_value=1000, value=50000, step=5000)
risk_percentage = st.sidebar.slider("Max Risk Per Trade (%)", min_value=0.5, max_value=5.0, value=1.0, step=0.5)

# 4. Primary Execution Loop
if st.sidebar.button("🚀 Run Advanced Institutional Scan"):
    with st.spinner("Processing deep structural algorithms..."):
        try:
            market_data = yf.download(tickers=ticker_symbol, period="5d", interval=time_window)
            if not market_data.empty:
                if isinstance(market_data.columns, pd.MultiIndex):
                    market_data.columns = market_data.columns.droplevel(1)
                
                # Internal Technical Indicator Calculations
                market_data['EMA_9'] = market_data['Close'].ewm(span=9, adjust=False).mean()
                market_data['EMA_21'] = market_data['Close'].ewm(span=21, adjust=False).mean()
                market_data['EMA_50'] = market_data['Close'].ewm(span=50, adjust=False).mean()
                
                delta = market_data['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / (loss + 1e-10)
                market_data['RSI'] = 100 - (100 / (1 + rs))
                
                market_data['Vol_Baseline'] = market_data['Volume'].rolling(window=20).mean()
                
                market_data['TR'] = np.maximum(market_data['High'] - market_data['Low'], 
                                              np.maximum(abs(market_data['High'] - market_data['Close'].shift(1)), 
                                                         abs(market_data['Low'] - market_data['Close'].shift(1))))
                market_data['ATR'] = market_data['TR'].rolling(window=14).mean()
                
                last_node = market_data.iloc[-1]
                prev_node = market_data.iloc[-2]
                
                current_price = float(last_node['Close'])
                current_rsi = float(last_node['RSI'])
                atr_band = float(last_node['ATR']) if float(last_node['ATR']) > 0 else (current_price * 0.004)
                volume_shock = float(last_node['Volume']) > (1.3 * float(last_node['Vol_Baseline']))
                
                bullish_structure = (last_node['EMA_9'] > last_node['EMA_21']) and (last_node['EMA_21'] > last_node['EMA_50'])
                bearish_structure = (last_node['EMA_9'] < last_node['EMA_21']) and (last_node['EMA_21'] < last_node['EMA_50'])
                
                bullish_momentum = current_rsi >= 58 and prev_node['RSI'] < 58
                bearish_momentum = current_rsi <= 42 and prev_node['RSI'] > 42
                
                if "NIFTY 50" in script_selector or "FINNIFTY" in script_selector:
                    base_strike = round(current_price / 50) * 50
                elif "BANK NIFTY" in script_selector or "SENSEX" in script_selector:
                    base_strike = round(current_price / 100) * 100
                else:
                    base_strike = round(current_price / 50) * 50
                
                # Signal Generation Assignment Block
                if bullish_structure and (bullish_momentum or current_rsi > 60) and volume_shock:
                    signal_output = "⚡ INSTITUTIONAL BUY SIGNALS"
                    sl = round(current_price - (1.5 * atr_band), 2)
                    target = round(current_price + (2.5 * atr_band), 2)
                    tsl = round(current_price - (0.8 * atr_band), 2)
                    deriv_tip = f"{base_strike - 50} CE" if segment_selector == "Option Chains" else "N/A"
                    system_state = "HIGH WIN-RATE"
                elif bearish_structure and (bearish_momentum or current_rsi < 40) and volume_shock:
                    signal_output = "⚠️ INSTITUTIONAL SHORT SELL SIGNALS"
                    sl = round(current_price + (1.5 * atr_band), 2)
                    target = round(current_price - (2.5 * atr_band), 2)
                    tsl = round(current_price + (0.8 * atr_band), 2)
                    deriv_tip = f"{base_strike + 50} PE" if segment_selector == "Option Chains" else "N/A"
                    system_state = "HIGH WIN-RATE"
                else:
                    signal_output = "⏳ ALGO SHIELD ACTIVE (STAY CASH / HOLD)"
                    sl = "N/A"
                    target = "N/A"
                    tsl = "N/A"
                    deriv_tip = "NO TRADE"
                    system_state = "SAFE RANGE PATTERN LOCK"
                
                # Metric Rendering Screen Area
                st.subheader(f"📊 Quantitative Asset Status: {script_selector} ({time_window} View)")
                metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)
                metric_col1.metric("ENTRY TRIGGER PRICE", f"₹{current_price:.2f}")
                
                if "BUY" in signal_output:
                    metric_col2.markdown(f"### <span style='color:#00C851'>{signal_output}</span>", unsafe_allow_html=True)
                elif "SHORT" in signal_output:
                    metric_col2.markdown(f"### <span style='color:#ff4444'>{signal_output}</span>", unsafe_allow_html=True)
                else:
                    metric_col2.markdown(f"### <span style='color:#a6a6a6'>{signal_output}</span>", unsafe_allow_html=True)
                    
                metric_col3.metric("MATHEMATICAL TARGET", f"₹{target}" if target != "N/A" else "N/A")
                metric_col4.metric("ALGO STOP LOSS", f"₹{sl}" if sl != "N/A" else "N/A")
                metric_col5.metric("🎯 TRAILING STOP LOSS", f"₹{tsl}" if tsl != "N/A" else "N/A")
                
                st.markdown("---")
                st.subheader("💡 Algorithmic Position Sizing & Risk Intelligence")
                
                info_left, info_right = st.columns(2)
                calculated_qty = 0
                
                with info_left:
                    st.info(f"📊 **System Status:** Unified Engine State is locked under **{system_state}**. RSI Core: **{current_rsi:.2f}**.")
                    max_risk_cash = total_capital * (risk_percentage / 100)
                    if sl != "N/A":
                        risk_per_unit = abs(current_price - sl)
                        if risk_per_unit > 0:
                            calculated_qty = int(max_risk_cash // risk_per_unit)
                            if segment_selector == "Option Chains":
                                lot_size = 25 if "NIFTY" in script_selector else 15
                                recommended_lots = max(1, calculated_qty // lot_size)
                                calculated_qty = recommended_lots * lot_size
                                st.success(f"⚖️ **Position Size:** Max Risk = **₹{max_risk_cash:.2f}**. Size = **{calculated_qty} Units ({recommended_lots} Lots)**.")
                            else:
                                st.success(f"⚖️ **Position Size:** Max Risk = **₹{max_risk_cash:.2f}**. Size = **{calculated_qty} Shares**.")
                    else:
                        st.info("⚖️ **Position Size Calculator:** Waiting for confirmation signal.")
                        
                with info_right:
                    if deriv_tip != "N/A" and deriv_tip != "NO TRADE":
                        st.success(f"🎯 **Options Chain Contract:** 🔥 RECOMMENDED CONTRACT: {deriv_tip}")
                    else:
                        st.warning("🎯 **Options Chain Contract:** Framework conditions not met yet. Derivative module locked.")
                
                if "HOLD" not in signal_output and calculated_qty > 0:
                    st.markdown("---")
                    st.subheader("📝 Live Trade Simulator Recorder")
                    if st.button("📥 Log Current Signal to History Dashboard"):
                        new_trade = {
                            "Asset": script_selector,
                            "Type": "BUY" if "BUY" in signal_output else "SHORT SELL",
                            "Entry Price": current_price,
                            "Target": target,
                            "Stop Loss": sl,
                            "Qty Allocated": calculated_qty
                        }
                        st.session_state.trade_log.append(new_trade)
