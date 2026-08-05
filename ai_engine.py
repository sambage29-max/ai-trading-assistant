def ai_decision(rsi, ema20, ema50, macd, adx, candle):

    score = 0
    reasons = []

    # ==========================
    # RSI
    # ==========================
    if rsi >= 60:
        score += 20
        reasons.append("✅ RSI Bullish")
    elif rsi <= 40:
        score -= 20
        reasons.append("🔴 RSI Bearish")
    else:
        reasons.append("🟡 RSI Neutral")

    # ==========================
    # EMA
    # ==========================
    if ema20 > ema50:
        score += 20
        reasons.append("✅ EMA Uptrend")
    else:
        score -= 20
        reasons.append("🔴 EMA Downtrend")

    # ==========================
    # MACD
    # ==========================
    if macd == "Bullish 🟢":
        score += 20
        reasons.append("✅ MACD Bullish")
    else:
        score -= 20
        reasons.append("🔴 MACD Bearish")

    # ==========================
    # ADX
    # ==========================
    if adx >= 30:
        score += 20
        reasons.append("✅ Strong Trend")
    elif adx >= 25:
        score += 10
        reasons.append("🟢 Moderate Trend")
    else:
        reasons.append("🟡 Weak Trend")

    # ==========================
    # Candle
    # ==========================
    if candle == "Bullish 🟢":
        score += 20
        reasons.append("🕯️ Bullish Candle")
    elif candle == "Bearish 🔴":
        score -= 20
        reasons.append("🕯️ Bearish Candle")

    # ==========================
    # Signal
    # ==========================
    if score >= 60:
        signal = "BUY 🟢"
    elif score <= -60:
        signal = "SELL 🔴"
    else:
        signal = "WAIT 🟡"

    # ==========================
    # Confidence
    # ==========================
    confidence = min(abs(score), 100)

    # ==========================
    # Trade Rating
    # ==========================
    if confidence >= 80:
        trade_rating = "⭐⭐⭐⭐⭐"
    elif confidence >= 60:
        trade_rating = "⭐⭐⭐⭐"
    elif confidence >= 40:
        trade_rating = "⭐⭐⭐"
    else:
        trade_rating = "⭐⭐"

    # ==========================
    # Market Mood
    # ==========================
    if score >= 60:
        market_mood = "🚀 Strong Bullish"
    elif score >= 20:
        market_mood = "🟢 Bullish"
    elif score <= -60:
        market_mood = "🔴 Strong Bearish"
    elif score <= -20:
        market_mood = "🟠 Bearish"
    else:
        market_mood = "🟡 Sideways"

    # ==========================
    # Probability
    # ==========================
    buy_probability = max(min((score + 100) / 2, 100), 0)
    sell_probability = 100 - buy_probability

    return (
        signal,
        score,
        confidence,
        trade_rating,
        market_mood,
        int(buy_probability),
        int(sell_probability),
        reasons,
    )