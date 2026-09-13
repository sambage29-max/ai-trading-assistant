import os
import requests
import pandas as pd
from typing import Dict, Any
from twilio.rest import Client

def send_whatsapp_alert(message_content: str):
    """Sends production-grade WhatsApp alerts using CallMeBot or Twilio API Gateway."""
    phone_number = "YOUR_PHONE_NUMBER"  # अपना फोन नंबर यहां डालें (+91...)
    api_key = "YOUR_CALLMEBOT_API_KEY"  # अपनी CallMeBot API Key यहां डालें
    
    if api_key != "YOUR_CALLMEBOT_API_KEY":
        url = f"https://callmebot.com{phone_number}&text={requests.utils.quote(message_content)}&apikey={api_key}"
        try:
            requests.get(url, timeout=10)
            return
        except Exception as e:
            print(f"WhatsApp Alert Failed: {e}")

def generate_trading_signal(df: pd.DataFrame, ticker_name: str, segment: str) -> Dict[str, Any]:
    """Generates segment-specific institutional grade buy/sell signals."""
    default_response = {"signal": "HOLD", "entry": 0.0, "target": 0.0, "sl": 0.0, "reason": "मार्केट न्यूट्रल है। सही एंट्री का इंतज़ार करें।"}
    
    if df.empty or len(df) < 20:
        return default_response
        
    latest = df.iloc[-1]
    current_price = float(latest['Close'])
    atr = float(latest['ATR']) if 'ATR' in latest and not pd.isna(latest['ATR']) else (current_price * 0.01)
    
    rsi = float(latest['RSI'])
    macd = float(latest['MACD'])
    macd_sig = float(latest['MACD_Signal'])
    bb_lower = float(latest['BB_Lower'])
    bb_upper = float(latest['BB_Upper'])
    
    # 🎯 सेगमेंट आधारित डायनेमिक रिस्क मैनेजमेंट (Dynamic Multipliers)
    if segment == "Options (Index/Stock)":
        target_multiplier, sl_multiplier = 3.5, 2.0  # ऑप्शंस में बड़ा टारगेट, कड़ा स्टॉपलॉस
    elif segment == "MCX (Commodity)":
        target_multiplier, sl_multiplier = 2.0, 1.0  # कमोडिटी के लिए सटीक लेवल्स
    elif segment == "Delivery (Long Term)":
        target_multiplier, sl_multiplier = 5.0, 3.0  # लॉन्ग टर्म के लिए बड़ा विज़न
    else:  # Intraday Equity
        target_multiplier, sl_multiplier = 2.5, 1.5
        
    # Technical Conditions
    bullish_crossover = macd > macd_sig
    bearish_crossover = macd < macd_sig
    
    # Buy Signal Generation
    if rsi < 42 and bullish_crossover and current_price <= (bb_lower * 1.02):
        setup = {
            "signal": "BUY 🟢",
            "entry": round(current_price, 2),
            "target": round(current_price + (atr * target_multiplier), 2),
            "sl": round(current_price - (atr * sl_multiplier), 2),
            "reason": f"Oversold Zone (RSI: {rsi:.1f}) near BB Lower band with MACD confirmation."
        }
        msg = f"🚨 *AI TRADING ALERT ({segment})* 🚨\n\nAsset: *{ticker_name}*\nSignal: *{setup['signal']}*\nEntry: {setup['entry']}\n🎯 Target: {setup['target']}\n🛑 Stoploss: {setup['sl']}\n\nReason: {setup['reason']}"
        send_whatsapp_alert(msg)
        return setup
        
    # Sell Signal Generation
    elif rsi > 58 and bearish_crossover and current_price >= (bb_upper * 0.98):
        setup = {
            "signal": "SELL / SHORT 🔴",
            "entry": round(current_price, 2),
            "target": round(current_price - (atr * target_multiplier), 2),
            "sl": round(current_price + (atr * sl_multiplier), 2),
            "reason": f"Overbought Zone (RSI: {rsi:.1f}) near BB Upper band with MACD rejection."
        }
        msg = f"🚨 *AI TRADING ALERT ({segment})* 🚨\n\nAsset: *{ticker_name}*\nSignal: *{setup['signal']}*\nEntry: {setup['entry']}\n🎯 Target: {setup['target']}\n🛑 Stoploss: {setup['sl']}\n\nReason: {setup['reason']}"
        send_whatsapp_alert(msg)
        return setup
        
    return default_response
