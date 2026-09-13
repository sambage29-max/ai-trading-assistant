import requests
import pandas as pd
from typing import Dict, Any

def send_whatsapp_alert(message_content: str):
    """Sends production-grade WhatsApp alerts strictly using CallMeBot API Gateway."""
    # 📝 अपना सेटअप यहाँ भरें:
    phone_number = "YOUR_PHONE_NUMBER"  # उदाहरण: +9199999XXXXX
    api_key = "YOUR_CALLMEBOT_API_KEY"  # अपनी API Key यहाँ डालें
    
    if api_key != "YOUR_CALLMEBOT_API_KEY" and phone_number != "YOUR_PHONE_NUMBER":
        url = f"https://callmebot.com{phone_number}&text={requests.utils.quote(message_content)}&apikey={api_key}"
        try:
            requests.get(url, timeout=10)
        except Exception as e:
            print(f"CallMeBot WhatsApp Alert Failed: {e}")

def generate_trading_signal(df: pd.DataFrame, ticker_name: str, segment: str) -> Dict[str, Any]:
    """Generates segment-specific dynamic buy/sell signals with optimized sensitivity."""
    default_response = {"signal": "HOLD", "entry": 0.0, "target": 0.0, "sl": 0.0, "reason": "मार्केट न्यूट्रल है। सही ट्रेंड या कन्वर्जेंस का इंतज़ार करें।"}
    
    if df.empty or len(df) < 15:
        return default_response
        
    latest = df.iloc[-1]
    current_price = float(latest['Close'])
    atr = float(latest['ATR']) if 'ATR' in latest and not pd.isna(latest['ATR']) else (current_price * 0.008)
    
    rsi = float(latest['RSI']) if 'RSI' in latest and not pd.isna(latest['RSI']) else 50.0
    macd = float(latest['MACD']) if 'MACD' in latest and not pd.isna(latest['MACD']) else 0.0
    macd_sig = float(latest['MACD_Signal']) if 'MACD_Signal' in latest and not pd.isna(latest['MACD_Signal']) else 0.0
    
    # 🎯 सेगमेंट आधारित रिस्क-रिवॉर्ड सिस्टम (Risk-Reward Multipliers)
    if segment == "Options (Index/Stock)":
        target_multiplier, sl_multiplier = 3.0, 1.5
    elif segment == "MCX (Commodity)":
        target_multiplier, sl_multiplier = 2.0, 1.0
    elif segment == "Delivery (Long Term)":
        target_multiplier, sl_multiplier = 4.5, 2.5
    else:  # Intraday Equity
        target_multiplier, sl_multiplier = 2.0, 1.0
        
    # 📊 ऑप्टिमाइज्ड डायनेमिक कंडीशंस (जल्दी सिग्नल्स पकड़ने के लिए सेंसिटिविटी बढ़ाई गई है)
    bullish_momentum = macd > macd_sig or rsi < 45
    bearish_momentum = macd < macd_sig or rsi > 55
    
    # 🟢 BUY SIGNAL MATRIX
    if rsi < 48 and bullish_momentum:
        setup = {
            "signal": "BUY 🟢",
            "entry": round(current_price, 2),
            "target": round(current_price + (atr * target_multiplier), 2),
            "sl": round(current_price - (atr * sl_multiplier), 2),
            "reason": f"Bullish structure alignment. RSI ({rsi:.1f}) in demand zone with supportive MACD trajectory."
        }
        msg = f"🚨 *AI TRADING ALERT ({segment})* 🚨\n\nAsset: *{ticker_name}*\nSignal: *{setup['signal']}*\nEntry: {setup['entry']}\n🎯 Target: {setup['target']}\n🛑 Stoploss: {setup['sl']}\n\nReason: {setup['reason']}"
        send_whatsapp_alert(msg)
        return setup
        
    # 🔴 SELL SIGNAL MATRIX
    elif rsi > 52 and bearish_momentum:
        setup = {
            "signal": "SELL / SHORT 🔴",
            "entry": round(current_price, 2),
            "target": round(current_price - (atr * target_multiplier), 2),
            "sl": round(current_price + (atr * sl_multiplier), 2),
            "reason": f"Bearish structure confirmation. RSI ({rsi:.1f}) showing overhead supply pressure."
        }
        msg = f"🚨 *AI TRADING ALERT ({segment})* 🚨\n\nAsset: *{ticker_name}*\nSignal: *{setup['signal']}*\nEntry: {setup['entry']}\n🎯 Target: {setup['target']}\n🛑 Stoploss: {setup['sl']}\n\nReason: {setup['reason']}"
        send_whatsapp_alert(msg)
        return setup
        
    return default_response
