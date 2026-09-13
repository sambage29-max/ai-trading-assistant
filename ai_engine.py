import requests
import pandas as pd
from typing import Dict, Any

def send_whatsapp_alert(message_content: str):
    """Sends production-grade WhatsApp alerts strictly using CallMeBot API Gateway."""
    # 📝 अपना सेटअप यहाँ भरें:
    # 1. https://callmebot.com पर जाएं
    # 2. उनके निर्देशानुसार मैसेज भेजकर अपनी API Key और फोन नंबर प्राप्त करें।
    phone_number = "YOUR_PHONE_NUMBER"  # उदाहरण: +9199999XXXXX
    api_key = "YOUR_CALLMEBOT_API_KEY"  # अपनी API Key यहाँ डालें
    
    if api_key != "YOUR_CALLMEBOT_API_KEY" and phone_number != "YOUR_PHONE_NUMBER":
        url = f"https://callmebot.com{phone_number}&text={requests.utils.quote(message_content)}&apikey={api_key}"
        try:
            # बैकग्राउंड में बिना ऐप को धीमा किए रिक्वेस्ट भेजेगा
            requests.get(url, timeout=10)
        except Exception as e:
            print(f"CallMeBot WhatsApp Alert Failed: {e}")

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
    
    # Dynamic Multipliers by Segment
    if segment == "Options (Index/Stock)":
        target_multiplier, sl_multiplier = 3.5, 2.0
    elif segment == "MCX (Commodity)":
        target_multiplier, sl_multiplier = 2.0, 1.0
    elif segment == "Delivery (Long Term)":
        target_multiplier, sl_multiplier = 5.0, 3.0
    else:  # Intraday Equity
        target_multiplier, sl_multiplier = 2.5, 1.5
        
    bullish_crossover = macd > macd_sig
    bearish_crossover = macd < macd_sig
    
    # BUY Trigger Matrix
    if rsi < 42 and bullish_crossover and current_price <= (bb_lower * 1.02):
        setup = {
            "signal": "BUY 🟢",
            "entry": round(current_price, 2),
            "target": round(current_price + (atr * target_multiplier), 2),
            "sl": round(current_price - (atr * sl_multiplier), 2),
            "reason": f"Oversold convergence (RSI: {rsi:.1f}) near BB Lower Band."
        }
        msg = f"🚨 *AI TRADING ALERT ({segment})* 🚨\n\nAsset: *{ticker_name}*\nSignal: *{setup['signal']}*\nEntry: {setup['entry']}\n🎯 Target: {setup['target']}\n🛑 Stoploss: {setup['sl']}\n\nReason: {setup['reason']}"
        send_whatsapp_alert(msg)
        return setup
        
    # SELL Trigger Matrix
    elif rsi > 58 and bearish_crossover and current_price >= (bb_upper * 0.98):
        setup = {
            "signal": "SELL / SHORT 🔴",
            "entry": round(current_price, 2),
            "target": round(current_price - (atr * target_multiplier), 2),
            "sl": round(current_price + (atr * sl_multiplier), 2),
            "reason": f"Overbought rejection (RSI: {rsi:.1f}) near BB Upper Band."
        }
        msg = f"🚨 *AI TRADING ALERT ({segment})* 🚨\n\nAsset: *{ticker_name}*\nSignal: *{setup['signal']}*\nEntry: {setup['entry']}\n🎯 Target: {setup['target']}\n🛑 Stoploss: {setup['sl']}\n\nReason: {setup['reason']}"
        send_whatsapp_alert(msg)
        return setup
        
    return default_response
