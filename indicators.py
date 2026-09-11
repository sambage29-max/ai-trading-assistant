import pandas as pd
import pandas_ta as ta  # Install via: pip install pandas-ta

def calculate_world_class_signals(df):
    """
    Calculates technical indicators and generates a high-probability 
    Delivery Signal based on Trend, Momentum, and Volume confluence.
    """
    if len(df) < 200:
        return df
    
    # 1. Trend Indicators
    df['EMA_50'] = ta.ema(df['close'], length=50)
    df['EMA_200'] = ta.ema(df['close'], length=200)
    
    # 2. Momentum Indicators
    df['RSI'] = ta.rsi(df['close'], length=14)
    macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
    df = pd.concat([df, macd], axis=1)
    
    # 3. Volume Benchmark (5-day rolling average)
    df['Vol_Avg'] = df['volume'].rolling(window=5).mean()
    
    # 4. High-Probability Signal Generation Logic
    df['Signal'] = 'HOLD'
    
    # Conditions for Delivery Buy
    strong_trend = df['EMA_50'] > df['EMA_200']
    oversold_reversal = (df['RSI'] > 35) & (df['RSI'].shift(1) <= 35)
    volume_breakout = df['volume'] > (df['Vol_Avg'] * 1.8)
    
    df.loc[strong_trend & oversold_reversal & volume_breakout, 'Signal'] = 'BUY'
    return df
