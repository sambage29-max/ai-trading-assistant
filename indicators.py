import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD

def calculate_advanced_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates world-class technical indicators cleanly handling pandas multi-indices."""
    if df.empty:
        return df
        
    df = df.copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
        
    # 1. RSI (Relative Strength Index)
    df['RSI'] = RSIIndicator(close=df['Close'], window=14).rsi()
    
    # 2. MACD (Moving Average Convergence Divergence)
    macd_obj = MACD(close=df['Close'])
    df['MACD'] = macd_obj.macd()
    df['MACD_Signal'] = macd_obj.macd_signal()
    
    # 3. Bollinger Bands (Volatility & Target Anchors)
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['StdDev'] = df['Close'].rolling(window=20).std()
    df['BB_Upper'] = df['MA20'] + (df['StdDev'] * 2)
    df['BB_Lower'] = df['MA20'] - (df['StdDev'] * 2)
    
    # 4. ATR (Average True Range for Dynamic Stoploss)
    high_low = df['High'] - df['Low']
    high_cp = np.abs(df['High'] - df['Close'].shift())
    low_cp = np.abs(df['Low'] - df['Close'].shift())
    df['TR'] = pd.concat([high_low, high_cp, low_cp], axis=1).max(axis=1)
    df['ATR'] = df['TR'].rolling(window=14).mean()
    
    # Drop temp columns to keep it clean
    df.drop(columns=['StdDev', 'TR'], errors='ignore', inplace=True)
    return df
