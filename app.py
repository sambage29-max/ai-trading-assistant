import streamlit as st
import pandas as pd
import numpy as np

# Mobile responsive wide layout configuration
st.set_page_config(page_title="Pro AI Signal Generator", layout="centered")

st.title("🎯 Pro AI Signal Generator")
st.caption("Intraday | Options Chain | MCX Commodities")
st.divider()

# --- SEGMENT SELECTOR TABS ---
tab1, tab2, tab3 = st.tabs(["⚡ Intraday", "📊 Options Chain", "🔥 MCX Commodities"])

# =========================================================================
# 1. INTRADAY EQUITY SEGMENT
# =========================================================================
with tab1:
    st.subheader("⚡ High-Probability Intraday Signals")
    st.info("Rule: 15-Min ORB + Volume Shockers above 50 EMA.")
    
    # Mock Intraday Data Structure
    intraday_data = {
        "Ticker": ["RELIANCE", "TCS", "INFY", "BHARTIARTL", "HDFCBANK"],
        "LTP": [2450.00, 4120.00, 1890.00, 1620.00, 1710.00],
        "Volume_Multiplier": [2.5, 0.8, 3.1, 1.9, 0.5], 
        "Signal": ["BUY", "NO SIGNAL", "BUY", "SHORT SELL", "NO SIGNAL"],
        "Stop_Loss": [2432.00, 0.0, 1871.00, 1632.00, 0.0],
        "Target": [2486.00, 0.0, 1928.00, 1596.00, 0.0]
    }
    df_intra = pd.DataFrame(intraday_data)
    
    # Filter for active signals
    active_intra = df_intra[df_intra["Signal"] != "NO SIGNAL"]
    
    for _, row in active_intra.iterrows():
        with st.expander(f"🟢 {row['Signal']} - {row['Ticker']} (LTP: ₹{row['LTP']})", expanded=True):
            col1, col2, col3 = st.columns(3)
            col1.metric("⚡ Entry Price", f"₹{row['LTP']:.2f}")
            col2.metric("🛑 Stop Loss", f"₹{row['Stop_Loss']:.2f}")
            col3.metric("🎯 Target", f"₹{row['Target']:.2f}")
            st.caption(f"💡 **Reason:** Volume Spike of `{row['Volume_Multiplier']}x` detected.")

# =========================================================================
# 2. OPTIONS CHAIN SEGMENT
# =========================================================================
with tab2:
    st.subheader("📊 NIFTY / BANKNIFTY Options Signal Matrix")
    st.info("Rule: PCR Trend + Highest OI Build-up (Support & Resistance)")
    
    # Dropdown for major indexes
    index_choice = st.selectbox("Select Index:", ["NIFTY", "BANKNIFTY"])
    
    # Mock Options Chain Data Fixed
    options_data = {
        "Strike Price":,
        "Call OI (Lakhs)": [12.4, 25.1, 48.9, 18.2, 35.6], 
        "Put OI (Lakhs)": [42.1, 33.4, 15.2, 8.4, 2.1],   
        "LTP CALL": [210.00, 142.00, 88.00, 48.00, 22.00],
        "LTP PUT": [15.00, 38.00, 79.00, 134.00, 212.00]
    }
    df_opt = pd.DataFrame(options_data)
    
    # Highlight highest Call and Put OI for support/resistance boundaries
    max_call_strike = df_opt.loc[df_opt["Call OI (Lakhs)"].idxmax(), "Strike Price"]
    max_put_strike = df_opt.loc[df_opt["Put OI (Lakhs)"].idxmax(), "Strike Price"]
    
    st.warning(f"🚨 **OI Range:** Strong Support at `{max_put_strike}` | Strong Resistance at `{max_call_strike}`")
    
    # Render option chain table cleanly on phone screen
    st.dataframe(df_opt, use_container_width=True, hide_index=True)
    
    # AI Suggested Derivative Play
    st.success("🤖 **AI Strategy Option Trigger:** Pullback to Put OI Support area. Suggest entering ATM CE if price sustains. SL: 15 pts | Target: 40 pts.")

# =========================================================================
# 3. MCX COMMODITIES SEGMENT
# =========================================================================
with tab3:
    st.subheader("🔥 Live MCX Commodity Setup")
    st.info("Rule: Supertrend (7,3) + RSI crossover for swing tracking.")
    
    # Mock MCX Data
    mcx_data = {
        "Commodity": ["CRUDEOIL", "GOLD", "SILVER", "NATURALGAS"],
        "LTP": [5840.00, 72350.00, 85400.00, 182.50],
        "Daily Trend": ["🚀 BULLISH", "🚀 BULLISH", "📉 BEARISH", "⚠️ SIDEWAYS"],
        "Signal Trigger": ["BUY", "BUY", "SHORT SELL", "WAIT"],
        "SL": [5790.00, 72100.00, 85900.00, 0.0],
        "TG": [5940.00, 72850.00, 84400.00, 0.0]
    }
    df_mcx = pd.DataFrame(mcx_data)
    
    for _, row in df_mcx.iterrows():
        with st.container():
            st.markdown(f"### `{row['Commodity']}` ({row['Daily Trend']})")
            if row["Signal Trigger"] in ["BUY", "SHORT SELL"]:
                c1, c2, c3 = st.columns(3)
                c1.metric("🟢 Entry (LTP)", f"{row['LTP']}")
                c2.metric("🛑 Stop Loss", f"{row['SL']}")
                c3.metric("🎯 Target", f"{row['TG']}")
            else:
                st.write("⏳ No high probability trade setup. Sitting on cash.")
            st.divider()
