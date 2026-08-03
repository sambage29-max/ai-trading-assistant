 import ta

def calculate_indicators(df_live):

    price = float(df_live["Close"].iloc[-1])

    # RSI
    rsi = ta.momentum.RSIIndicator(df_live["Close"]).rsi().iloc[-1]

    # EMA 20
    ema20 = ta.trend.EMAIndicator(
        df_live["Close"],
        window=20
    ).ema_indicator().iloc[-1]

    # EMA 50
    ema50 = ta.trend.EMAIndicator(
        df_live["Close"],
        window=50
    ).ema_indicator().iloc[-1]

    # MACD
    macd_indicator = ta.trend.MACD(df_live["Close"])

    macd_line = macd_indicator.macd().iloc[-1]
    signal_line = macd_indicator.macd_signal().iloc[-1]

    macd = "Bullish" if macd_line > signal_line else "Bearish"

    # ATR
    atr = ta.volatility.AverageTrueRange(
        high=df_live["High"],
        low=df_live["Low"],
        close=df_live["Close"],
        window=14
    ).average_true_range().iloc[-1]

    # ADX
    adx = ta.trend.ADXIndicator(
        high=df_live["High"],
        low=df_live["Low"],
        close=df_live["Close"],
        window=14
    ).adx().iloc[-1]

    # Current Candle
    open_price = float(df_live["Open"].iloc[-1])
    close_price = float(df_live["Close"].iloc[-1])

    if close_price > open_price:
        candle = "Bullish 🟢"
    elif close_price < open_price:
        candle = "Bearish 🔴"
    else:
        candle = "Doji 🟡"

    return {
        "price": price,
        "rsi": rsi,
        "ema20": ema20,
        "ema50": ema50,
        "macd": macd,
        "atr": atr,
        "adx": adx,
        "candle": candle
    }