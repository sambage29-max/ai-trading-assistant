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

return signal, score
