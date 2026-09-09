import pandas as pd
import yfinance as yf
import numpy as np
import requests

# ==========================================
# 🔑 Aapki Details Successfully Configured Hain
# ==========================================
TELEGRAM_TOKEN = "8680517650:AAHYrpb5j88XNGIoK-xu-hC-qZWs3RtCHkk"
TELEGRAM_CHAT_ID = "7374819912"

def send_telegram_alert(message):
    # Fixed URL Structure with api.telegram.org/bot
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code != 200:
            print(f"❌ Telegram Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"⚠️ Telegram Connection Fault: {str(e)}")

# ==========================================
# 📈 Fixed Ticker Universe (No Spaces)
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

print("Starting Global Autopilot Institutional Market Scan...")
