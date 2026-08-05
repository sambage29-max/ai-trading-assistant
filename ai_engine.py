def ai_decision(rsi, ema20, ema50, macd, adx):
    """
    AI Brain
    Input:
        RSI
        EMA20
        EMA50
        MACD
        ADX

    Output:
        Signal
        Score
        Confidence
    """

    score = 0
# RSI Analysis

# MACD Analysis

# EMA Analysis

# ADX Analysis

if adx >= 25:
    score += 25

else:
    score -= 10

if ema20 > ema50:
    score += 25

else:
    score -= 25
if macd == "Bullish":
    score += 25

else:
    score -= 25
if rsi >= 60:
    score += 25

elif rsi <= 40:
    score -= 25

  # Final Decision

if score >= 75:
    signal = "STRONG BUY"

elif score >= 25:
    signal = "BUY"

elif score <= -75:
    signal = "STRONG SELL"

elif score <= -25:
    signal = "SELL"

else:
    signal = "WAIT"

# Confidence Score
confidence_score = abs(score)

if confidence_score >= 75:
    trade_rating = "⭐⭐⭐⭐⭐"

elif confidence_score >= 50:
    trade_rating = "⭐⭐⭐⭐"

elif confidence_score >= 25:
    trade_rating = "⭐⭐⭐"

else:
    trade_rating = "⭐⭐"

# Market Mood

if score >= 75:
    market_mood = "🚀 Strong Bullish"

elif score >= 25:
    market_mood = "🟢 Bullish"

elif score <= -75:
    market_mood = "🔴 Strong Bearish"

elif score <= -25:
    market_mood = "🟠 Bearish"

else:
    market_mood = "🟡 Sideways"

return (
    signal,
    score,
    confidence_score,
    trade_rating,
    market_mood,
)
