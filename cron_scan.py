import pandas as pd
import yfinance as yf
import numpy as np
import requests

TELEGRAM_TOKEN = "8680517650:AAHYrpb5j88XNGIoK-xu-hC-qZWs3RtCHkk"
TELEGRAM_CHAT_ID = "7374819912"

def send_telegram_alert(message):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

# Complete Tracking Universe Portfolio Matrix
ticker_universe = {
    "NIFTY 50": "^NSEI", 
    "BANK NIFTY": "^NSEBANK",
    "FINNIFTY": "NIFTY_FIN_SERVICE.NS",
    "RELIANCE": "RELIANCE.NS",
    "TATA MOTORS": "TATAMOTORS.NS",
    "SBI": "SBIN.NS",
    "CRUDE OIL": "CL=F"
}

print("Starting Global Autopilot Institutional Market Scan...")

for asset_name, ticker_symbol in ticker_universe.items():
    try:
        df = yf.download(tickers=ticker_symbol, period="5d", interval="5m")
        if df.empty:
            continue
            
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
            
        df['EMA_9'] = df['Close'].ewm(span=9, adjust=False).mean()
        df['EMA_21'] = df['Close'].ewm(span=21, adjust=False).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-10)
        df['RSI'] = 100 - (100 / (1 + rs))
        
        df['Vol_Baseline'] = df['Volume'].rolling(window=20).mean()
        df['TR'] = np.maximum(df['High'] - df['Low'], np.maximum(abs(df['High'] - df['Close'].shift(1)), abs(df['Low'] - df['Close'].shift(1))))
        df['ATR'] = df['TR'].rolling(window=14).mean()
        
        last = df.iloc[-1]
        prev = df.iloc[-2]
        
        current_price = float(last['Close'])
        current_rsi = float(last['RSI'])
        atr_band = float(last['ATR']) if float(last['ATR']) > 0 else (current_price * 0.004)
        volume_shock = float(last['Volume']) > (1.3 * float(df['Vol_Baseline'].iloc[-1]))
        
        bullish_structure = (last['EMA_9'] > last['EMA_21']) and (last_node['EMA_21'] > last_node['EMA_50'])
        bearish_structure = (last['EMA_9'] < last_node['EMA_21']) and (last_node['EMA_21'] < last_node['EMA_50'])
        
        bullish_momentum = current_rsi >= 58 and prev['RSI'] < 58
        bearish_momentum = current_rsi <= 42 and prev['RSI'] > 42
        
        # Check Strategy Entry Triggers
        if bullish_structure and (bullish_momentum or current_rsi > 60) and volume_shock:
            sl = round(current_price - (1.5 * atr_band), 2)
            target = round(current_price + (2.5 * atr_band), 2)
            tsl = round(current_price - (0.8 * atr_band), 2)
            
            msg = f"🚀 *AUTOPILOT BREAKOUT BUY*\n📦 *Asset:* {asset_name}\n💵 *Price:* ₹{current_price:.2f}\n🎯 *Tgt:* ₹{target}\n🛡️ *SL:* ₹{sl}\n📈 *TSL:* ₹{tsl}"
            send_telegram_alert(msg)
            print(f"Signal sent for {asset_name}")
            
        elif bearish_structure and (bearish_momentum or current_rsi < 40) and volume_shock:
            sl = round(current_price + (1.5 * atr_band), 2)
            target = round(current_price - (2.5 * atr_band), 2)
            tsl = round(current_price + (0.8 * atr_band), 2)
            
            msg = f"⚠️ *AUTOPILOT BREAKDOWN SHORT*\n📦 *Asset:* {asset_name}\n💵 *Price:* ₹{current_price:.2f}\n🎯 *Tgt:* ₹{target}\n🛡️ *SL:* ₹{sl}\n📈 *TSL:* ₹{tsl}"
            send_telegram_alert(msg)
            print(f"Signal sent for {asset_name}")
            
    except Exception as e:
        print(f"Error scanning {asset_name}: {str(e)}")

print("Autopilot Session Completed Successfully.")
