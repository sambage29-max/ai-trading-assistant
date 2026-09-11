import streamlit as st
import pandas as pd

# Mobile responsive configuration
st.set_page_config(page_title="AI Trading App", layout="centered")

st.title("🎯 Pro AI Signal Generator")
st.caption("Intraday | Options Chain | MCX Commodities")
st.divider()

# 3 Navigation Tabs for phone screens
tab1, tab2, tab3 = st.tabs(["⚡ Intraday", "📊 Options", "🔥 MCX"])

# 1. INTRADAY SECTION
with tab1:
    st.subheader("⚡ Intraday Signals")
    data_intra = {
        "Ticker": ["RELIANCE", "INFY", "BHARTIARTL"],
        "LTP": [2450.0, 1890.0, 1620.0],
        "Signal": ["BUY", "BUY", "SHORT"]
    }
    st.dataframe(pd.DataFrame(data_intra), use_container_width=True, hide_index=True)

# 2. OPTIONS CHAIN SECTION
with tab2:
    st.subheader("📊 NIFTY Options Chain")
    data_opt = {
        "Strike":,
        "Call_OI_Lakhs": [12.4, 25.1, 48.9, 18.2],
        "Put_OI_Lakhs": [42.1, 33.4, 15.2, 8.4]
    }
    st.dataframe(pd.DataFrame(data_opt), use_container_width=True, hide_index=True)
    st.warning("🚨 Resistance at 25000 | Support at 24800")

# 3. MCX COMMODITIES SECTION
with tab3:
    st.subheader("🔥 MCX Live Setup")
    data_mcx = {
        "Commodity": ["CRUDEOIL", "GOLD", "SILVER"],
        "LTP": [5840.0, 72350.0, 85400.0],
        "Trend": ["BULLISH", "BULLISH", "BEARISH"]
    }
    st.dataframe(pd.DataFrame(data_mcx), use_container_width=True, hide_index=True)
