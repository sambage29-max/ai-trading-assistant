import unittest
import pandas as pd
import numpy as np
from indicators import calculate_advanced_indicators
from ai_engine import generate_trading_signal

class TestTradingSuite(unittest.TestCase):
    
    def setUp(self):
        """Creates dummy historic DataFrame structure to simulate candles."""
        np.random.seed(42)
        date_range = pd.date_range(start="2026-01-01", periods=30, freq="15min")
        self.mock_data = pd.DataFrame({
            'Open': np.random.uniform(100, 110, size=30),
            'High': np.random.uniform(110, 120, size=30),
            'Low': np.random.uniform(90, 100, size=30),
            'Close': np.random.uniform(100, 110, size=30)
        }, index=date_range)

    def test_indicator_calculation(self):
        """Validates indicators append safely without altering dimensional matrices."""
        processed_df = calculate_advanced_indicators(self.mock_data)
        self.assertIn('RSI', processed_df.columns)
        self.assertIn('MACD', processed_df.columns)
        self.assertIn('ATR', processed_df.columns)
        self.assertFalse(processed_df.isna().all().all(), "Engine returned fully absolute empty columns.")

    def test_ai_engine_logic(self):
        """Validates AI decisions fall within bounded strategic parameters."""
        processed_df = calculate_advanced_indicators(self.mock_data)
        decision = generate_trading_signal(processed_df)
        self.assertIn("signal", decision)
        self.assertIn("target", decision)
        self.assertIsInstance(decision["signal"], str)

if __name__ == "__main__":
    unittest.main()
