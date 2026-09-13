import pandas as pd
from typing import Dict, Any

def generate_trading_signal(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyzes the latest matrix state to produce institutional grade signals."""
    default_response = {"signal": "HOLD", "entry": 0.0, "target": 0.0, "sl": 0.0, "reason": "No clear trend convergence."}
    
    if df.empty or len(df) < 20:
        return default_response
        
    latest = df.iloc[-1]
    current_price = float(latest['Close'])
    atr = float(latest['ATR']) if 'ATR' in latest and not pd.isna(latest['ATR']) else (current_price * 0.01)
    
    rsi = float(latest['RSI'])
    macd = float(latest['MACD'])
    macd_sig = float(latest['MACD_Signal'])
    bb_upper = float(latest['BB_Upper'])
    bb_lower = float(latest['BB_Lower'])
    
    # Institutional Check Conditions
    bullish_crossover = macd > macd_sig
    bearish_crossover = macd < macd_sig
    
    # Dynamic Risk Management Structure (Using 2x ATR for Target, 1.5x ATR for SL)
    if rsi < 42 and bullish_crossover and current_price <= (bb_lower * 1.02):
        return {
            "signal": "BUY",
            "entry": round(current_price, 2),
            "target": round(current_price + (atr * 2.5), 2),
            "sl": round(current_price - (atr * 1.5), 2),
            "reason": f"Oversold convergence (RSI: {rsi:.1f}) near Bollinger Lower Band with active MACD bullish cross."
        }
        
    elif rsi > 58 and bearish_crossover and current_price >= (bb_upper * 0.98):
        return {
            "signal": "SELL / SHORT",
            "entry": round(current_price, 2),
            "target": round(current_price - (atr * 2.5), 2),
            "sl": round(current_price + (atr * 1.5), 2),
            "reason": f"Overbought rejection (RSI: {rsi:.1f}) near Bollinger Upper Band with active MACD bearish cross."
        }
        
    return default_response
