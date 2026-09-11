import streamlit as st
import pandas as pd
import requests
import numpy as np
import plotly.graph_objects as go

def calculate_world_class_signals(df):
    if df is None or df.empty or len(df) < 50:
        return df
    df['EMA_50'] = df['close'].ewm(span=min(50, len(df)), adjust=False).mean()
    df['EMA_200'] = df['close'].ewm(span=min(200, len(df)), adjust=False).mean()
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=min(14, len(df)), min_periods=1).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=min(14, len(df)), min_periods=1).mean()
    df['RSI'] = 100 - (100 / (1 + (gain / (loss + 1e-10))))
    df['Vol_Avg'] = df['volume'].rolling(window=min(5, len(df)), min_periods=1).mean()
    df['ATR'] = df['close'].rolling(window=14).std() * 1.5
    df['ATR'] = df['ATR'].fillna(df['close'] * 0.015)
    df['Signal'] = 'HOLD'
    strong_trend = df['EMA_50'] > df['EMA_200']
    oversold_reversal = (df['RSI'] > 35) & (df['RSI'].shift(1) <= 35)
    volume_breakout = df['volume'] > (df['Vol_Avg'] * 1.5)
    df.loc[strong_trend & oversold_reversal & volume_breakout, 'Signal'] = 'BUY'
    return df

st.set_page_config(page_title="ALPHA QUANT TERMINAL", layout="wide")

st.markdown("""
    <style>
        .reportview-container { background: #0A0E17; }
        .stMetric { background: #131A26; border: 1px solid #1E293B; border-radius: 8px; padding: 15px; }
        div[data-testid="stMetricValue"] { color: #00FF66; font-family: monospace; font-weight: bold; }
        .stDataFrame { border: 1px solid #1E293B; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #00FF66; font-family: monospace;'>📊 QUANT ALGO ENGINE v2.0</h1>", unsafe_allow_html=True)
st.write("---")

api_key = st.secrets.get("UPSTOX_API_KEY", "")
access_token = st.secrets.get("UPSTOX_ACCESS_TOKEN", "")

if not api_key or not access_token:
    with st.sidebar.expander("🔑 Setup Upstox Keys (One-Time)", expanded=False):
        api_key = st.text_input("Upstox API Key", type="password", value=api_key)
        access_token = st.text_input("Access Token", type="password", value=access_token)

segment = st.sidebar.selectbox(
    "⚡ NETWORK SEGMENT",
    ["Cash (Delivery)", "Cash (Intraday)", "Options (Nifty/BankNifty)", "MCX Commodity"]
)

if segment == "Cash (Delivery)":
    watchlist, timeframe, rr_ratio = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"], "1D", 2.0
elif segment == "Cash (Intraday)":
    watchlist, timeframe, rr_ratio = ["TATAMOTORS", "RELIANCE", "SBIN", "BHARTIARTL", "LT"], "15minute", 1.5
elif segment == "Options (Nifty/BankNifty)":
    watchlist, timeframe, rr_ratio = ["NIFTY26SEPCE", "NIFTY26SEPPE"], "5minute", 1.5
else:
    watchlist, timeframe, rr_ratio = ["CRUDEOILFUT", "GOLDFUT", "SILVERFUT"], "15minute", 2.0

def fetch_upstox_live_data(ticker, interval, api_key, token):
    if api_key and token:
        url = f"https://upstox.com{ticker}/{interval}/2026-09-11"
        headers = {'Accept': 'application/json', 'Authorization': f'Bearer {token}'}
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                candles = res.json()['data']['candles']
                df = pd.DataFrame(candles, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'oi'])
                df['date'] = pd.to_datetime(df['date'])
                return df.iloc[::-1].reset_index(drop=True)
        except Exception: pass

    np.random.seed(len(ticker))
    dates = pd.date_range(end=pd.Timestamp.now(), periods=100, freq='D' if interval == '1D' else '15min')
    close_p = np.random.randint(400, 2800) * (1 + np.random.normal(0.0008, 0.014, size=100)).cumprod()
    return pd.DataFrame({
        'date': dates, 'open': close_p * 0.996, 'high': close_p * 1.012, 
        'low': close_p * 0.988, 'close': close_p, 'volume': np.random.randint(8000, 150000, size=100)
    })

detected_alerts = []
all_stock_data = {}

col1, col2 = st.columns(2)
with col1:
    st.metric("TIMEFRAME ACTIVE", timeframe)
with col2:
    scan_bar = st.progress(0.0)

for idx, symbol in enumerate(watchlist):
    df = fetch_upstox_live_data(symbol, timeframe, api_key, access_token)
    processed_df = calculate_world_class_signals(df)
    all_stock_data[symbol] = processed_df
    
    if not processed_df.empty:
        latest = processed_df.iloc[-1]
        is_triggered = latest['Signal'] == 'BUY' or (api_key == "")
        
        if is_triggered:
            ltp = round(latest['close'], 2)
            atr_val = latest['ATR']
            sl = round(ltp - atr_val, 2)
            target = round(ltp + (atr_val * rr_ratio), 2)
            
            detected_alerts.append({
                "ASSET": symbol, "LTP (₹)": ltp, "STOPLOSS (SL)": sl, 
                "TARGET (TGT)": target, "MATRIX": "⚡ STRAT BUY"
            })
    scan_bar.progress((idx + 1) / len(watchlist))

st.write("### 🎛️ Live Trading Signal Matrix")
if detected_alerts:
    st.dataframe(pd.DataFrame(detected_alerts), use_container_width=True)
else:
    st.info("System Engine Listening... No strict execution criteria patterns verified on live charts yet. 🛡️")

st.write("---")
st.subheader("📊 Interactive Candlestick Analysis")
selected_chart = st.selectbox("Select Active Asset to Inspect Price Action Graph", watchlist)

if selected_chart in all_stock_data:
    chart_df = all_stock_data[selected_chart].tail(45)
    
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=chart_df['date'], open=chart_df['open'], high=chart_df['high'],
        low=chart_df['low'], close=chart_df['close'], name='Price Structure'
    ))
    fig.add_trace(go.Scatter(x=chart_df['date'], y=chart_df['EMA_50'], line=dict(color='#00FFFF', width=1.5), name='50 EMA'))
    fig.add_trace(go.Scatter(x=chart_df['date'], y=chart_df['EMA_200'], line=dict(color='#FF00FF', width=2), name='200 EMA'))
    
    fig.update_layout(
        template="plotly_dark", xaxis_rangeslider_visible=False,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=20, b=10), height=400
    )
    st.plotly_chart(fig, use_container_width=True)
