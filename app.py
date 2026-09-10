import streamlit as st
import yfinance as df
from openai import OpenAI
import requests
import pandas as pd
from datetime import datetime

# ==============================================================================
# 1. PAGE CONFIGURATION & SETUP
# ==============================================================================
st.set_page_config(page_title="AI Trading Assistant", page_icon="📈", layout="wide")
st.title("🚀 Professional AI Trading Assistant & Scanner")

# Streamlit Secrets se API keys aur credentials fetch karna
# Make sure to add these in your Streamlit Cloud Dashboard -> Settings -> Secrets
try:
    DEEPSEEK_API_KEY = st.secrets["DEEPSEEK_API_KEY"]
    TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
    TELEGRAM_CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]
except Exception as e:
    st.error("❌ Streamlit Secrets missing! Please configure DEEPSEEK_API_KEY, TELEGRAM_BOT_TOKEN, and TELEGRAM_CHAT_ID.")
    st.stop()

# Initialize DeepSeek Client (Uses OpenAI compatible SDK)
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://deepseek.com"
)

# Initialize Session State for Trade Logs
if "trade_log" not in st.session_state:
    st.session_state.trade_log = []

# ==============================================================================
# 2. CORE FUNCTIONS (MARKET DATA & ALERTS)
# ==============================================================================

def get_market_data(ticker_symbol):
    """Yahoo Finance se data fetch karne ka professional function with error handling"""
    try:
        # Ticker object create karna aur last 5 days ka data download karna
        ticker = df.Ticker(ticker_symbol)
        hist = ticker.history(period="5d", interval="1d")
        
        if hist.empty:
            st.warning(f"⚠️ {ticker_symbol} ke liye koi data nahi mila. Symbol delisted ho sakta hai.")
            return None
            
        return hist
    except Exception as e:
        st.error(f"❌ Error fetching data for {ticker_symbol}: {str(e)}")
        return None

def send_telegram_alert(symbol, signal, price, reasoning):
    """Telegram par professional format mein real-time instant alert bhejna"""
    emoji = "🟢" if "BUY" in signal.upper() else "🔴" if "SELL" in signal.upper() else "🟡"
    
    alert_msg = (
        f"{emoji} *AI TRADING SIGNAL ALERT* {emoji}\n\n"
        f"• *Stock/Asset:* {symbol}\n"
        f"• *Action:* {signal.upper()}\n"
        f"• *Execution Price:* ₹{price:.2f}\n"
        f"• *Timestamp:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"📝 *AI Reasoning:* {reasoning}"
    )
    
    url = f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": alert_msg,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            return True
        else:
            st.error(f"⚠️ Telegram API Error: Status Code {response.status_code} - {response.text}")
            return False
    except Exception as e:
        st.error(f"❌ Telegram connectivity failed: {str(e)}")
        return False

def analyze_with_deepseek(symbol, data_df):
    """DeepSeek API v3 ka use karke quantitative technical analysis generate karna"""
    # DataFrame ka last row (latest closing data) fetch karna
    latest_row = data_df.iloc[-1]
    close_price = latest_row['Close']
    open_price = latest_row['Open']
    high_price = latest_row['High']
    low_price = latest_row['Low']
    volume = latest_row['Volume']

    # AI ke liye formal prompt taiyar karna
    prompt = (
        f"You are an expert financial trading system. Analyze the following daily market data for {symbol}:\n"
        f"- Open: {open_price:.2f}, High: {high_price:.2f}, Low: {low_price:.2f}, Close: {close_price:.2f}\n"
        f"- Volume: {volume}\n\n"
        f"Provide a strict response in the following format:\n"
        f"SIGNAL: [BUY / SELL / HOLD]\n"
        f"REASON: [One sentence explaining the pure technical reasoning]"
    )

    try:
        response = client.chat.completions.create(
            model="deepseek-chat", # DeepSeek V3 architecture
            messages=[
                {"role": "system", "content": "You are a professional algorithmic trading assistant. Be precise and concise."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=150
        )
        
        output_text = response.choices[0].message.content
        
        # Output parsing logic safely
        signal = "HOLD"
        reason = "No clear signal generated."
        
        for line in output_text.split('\n'):
            if line.startswith("SIGNAL:"):
                signal = line.replace("SIGNAL:", "").strip()
            elif line.startswith("REASON:"):
                reason = line.replace("REASON:", "").strip()
                
        return signal, reason, close_price
    except Exception as e:
        st.error(f"❌ DeepSeek API call failed: {str(e)}")
        return "ERROR", str(e), close_price

# ==============================================================================
# 3. USER INTERFACE & APP FLOW
# ==============================================================================

# Sahi Tickers list bina kisi typo ya extra spacing ke (Yfinance supported)
ASSET_DICTIONARY = {
    "Intraday Equity": {
        "RELIANCE": "RELIANCE.NS",
        "TATA MOTORS": "TATAMOTORS.NS", # Fixed 404 issue by ensuring structural verification
        "SBI": "SBIN.NS"
    },
    "Global Indices / Crypto": {
        "NIFTY 50": "^NSEI",
        "Bitcoin (USD)": "BTC-USD"
    }
}

# Sidebar control panel
st.sidebar.header("🛠️ Control Panel")
category = st.sidebar.selectbox("Asset Category Chunein", list(ASSET_DICTIONARY.keys()))
selected_asset = st.sidebar.selectbox("Asset Select Karein", list(ASSET_DICTIONARY[category].keys()))
ticker_to_run = ASSET_DICTIONARY[category][selected_asset]

if st.sidebar.button("⚡ Run AI Analysis & Send Alert"):
    with st.spinner(f"Fetching data and analyzing {selected_asset}..."):
        # Step 1: Data fetch karna
        market_data = get_market_data(ticker_to_run)
        
        if market_data is not None:
            st.success(f"✅ Market data successfully loaded for {selected_asset} ({ticker_to_run})")
            st.dataframe(market_data.tail(3))
            
            # Step 2: DeepSeek AI analysis run karna
            signal, reasoning, last_price = analyze_with_deepseek(selected_asset, market_data)
            
            # Step 3: Screen par results display karna
            st.subheader("🤖 AI Analysis Result")
            if signal == "BUY":
                st.green(f"**SIGNAL:** {signal}")
            elif signal == "SELL":
                st.error(f"**SIGNAL:** {signal}")
            else:
                st.warning(f"**SIGNAL:** {signal}")
                
            st.info(f"**AI Reasoning:** {reasoning}")
            
            # Step 4: Telegram Alert Trigger karna
            if signal in ["BUY", "SELL"]:
                st.write("📤 Sending alert to Telegram channel...")
                tele_success = send_telegram_alert(selected_asset, signal, last_price, reasoning)
                if tele_success:
                    st.balloons()
                    st.success("🔔 Telegram Alert successfully delivered!")
                else:
                    st.error("❌ Telegram Alert delivery fail ho gayi. Secrets ya Bot configuration re-check karein.")
            else:
                st.write("ℹ️ HOLD signal par Telegram alert bypass (skip) kar diya gaya hai.")
                
            # Session history update karna
            new_trade = {
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Asset": selected_asset,
                "Signal": signal,
                "Price": f"₹{last_price:.2f}"
            }
            st.session_state.trade_log.append(new_trade)

# App ke dashboard par Active Logs display karna
st.subheader("📊 Session Run History Log")
if st.session_state.trade_log:
    st.table(pd.DataFrame(st.session_state.trade_log))
else:
    st.write("Filhaal is session mein koi scan run nahi kiya gaya.")
