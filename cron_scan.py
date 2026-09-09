import pandas as pd
import yfinance as yf
import numpy as np
import requests
import streamlit as st
from openai import OpenAI

# ==========================================
# 🔑 Telegram Configuration
# ==========================================
TELEGRAM_TOKEN = "8680517650:AAHYrpb5j88XNGIoK-xu-hC-qZWs3RtCHkk"
TELEGRAM_CHAT_ID = "7374819912"

def send_telegram_alert(message):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code != 200:
            print(f"❌ Telegram Error: {response.text}")
    except Exception as e:
        print(f"⚠️ Telegram Connection Fault: {str(e)}")

# ==========================================
# 🤖 DeepSeek AI Analysis Engine
# ==========================================
def get_deepseek_decision(stock_name, price, rsi, signal):
    try:
        # Streamlit Secrets se automatically key uthayega
        client = OpenAI(
            api_key=st.secrets["DEEPSEEK_API_KEY"],
            base_url="https://deepseek.com"
        )
        
        prompt = f"""
        Analyze this live market setup as an institutional trader:
        Asset: {stock_name}
        Current Price: ₹{price}
        RSI (5m): {rsi}
        Indicator Signal: {signal}
        
        Provide your decision in clean Hinglish. Format strictly as:
        ⚡ *Decision:* BUY / SHORT SELL / STAY CASH
        🎯 *Reason:* (Strictly 1 simple sentence)
        """
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=150
        )
        return response.choices.message.content
    except Exception as e:
        return f"⚠️ DeepSeek Analysis Failed: {str(e)}"

# ==========================================
# 📈 Ticker Universe & Execution
# ==========================================
ticker_universe = {
    "NIFTY 50": "^NSEI",
    "BANK NIFTY": "^NSEBANK",
    "FINNIFTY": "NIFTY_FIN_SERVICE.NS",
    "RELIANCE": "RELIANCE.NS",
    "TATAMOTORS": "TATAMOTORS.NS",
    "SBIN": "SBIN.NS",
    "CRUDE OIL": "CL=F"
}

print("Starting Global Autopilot Institutional Market Scan with DeepSeek...")
