import numpy as np

def detect_support_resistance(df, n=5):
    """
    Detect support and resistance levels
    n = number of recent candles to consider
    """
    highs = df['high'][-n:]
    lows = df['low'][-n:]
    resistance = np.max(highs)
    support = np.min(lows)
    return support, resistance
