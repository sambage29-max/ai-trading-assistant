import yfinance as yf
import time
from indicators import calculate_advanced_indicators
from ai_engine import generate_trading_signal

# Watchlist of high liquidity assets
WATCHLIST = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]

def scan_markets():
    print(f"\n===[ Running Systematic Market Scan: {time.ctime()} ]===")
    for ticker in WATCHLIST:
        try:
            df = yf.download(ticker, period="5d", interval="15m", progress=False)
            if df.empty:
                continue
            df = calculate_advanced_indicators(df)
            setup = generate_trading_signal(df)
            
            if setup["signal"] != "HOLD":
                print(f"🚨 ALERT | {ticker} -> VERDICT: {setup['signal']} | Entry: {setup['entry']} | Target: {setup['target']} | SL: {setup['sl']}")
            else:
                print(f"📊 Stable | {ticker} -> Market Neutral (Hold)")
        except Exception as e:
            print(f"❌ Error scanning {ticker}: {str(e)}")

if __name__ == "__main__":
    # Standard daemon trigger loop
    scan_markets()
