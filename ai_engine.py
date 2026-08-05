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

if rsi >= 60:
    score += 25

elif rsi <= 40:
    score -= 25
    return score
