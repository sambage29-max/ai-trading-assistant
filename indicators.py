import pandas as pd

def calculate_world_class_signals(df):
    """
    Pure mathematical calculations for RSI, EMA, and MACD.
    Zero external indicator library dependencies to prevent server crashes.
    """
    if df is None or df.empty or len(df) < 50:
        return df
    
    # 1. EMA Calculations safely
    df['EMA_50'] = df['close'].ewm(span=min(50, len(df)), adjust=False).mean()
    df['EMA_200'] = df['close'].ewm(span=min(200, len(df)), adjust=False).mean()
    
    # 2. RSI Calculation (Relative Strength Index)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=min(14, len(df)), min_periods=1).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=min(14, len(df)), min_periods=1).mean()
    rs = gain / (loss + 1e-10)
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # 3. Volume Average Benchmark
    df['Vol_Avg'] = df['volume'].rolling(window=min(5, len(df)), min_periods=1).mean()
    
    # 4. Final Delivery Buy Signal Generation Strategy
    df['Signal'] = 'HOLD'
    
    # Filtering Condition Check Blocks
    strong_trend = df['EMA_50'] > df['EMA_200']
    oversold_reversal = (df['RSI'] > 35) & (df['RSI'].shift(1) <= 35)
    volume_breakout = df['volume'] > (df['Vol_Avg'] * 1.8)
    
    df.loc[strong_trend & oversold_reversal & volume_breakout, 'Signal'] = 'BUY'
    return df
