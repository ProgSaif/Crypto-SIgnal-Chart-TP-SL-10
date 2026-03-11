import pandas as pd
from scanner import get_klines
from config import EMA_FAST, EMA_SLOW, RSI_PERIOD, RSI_LONG_MAX, RSI_SHORT_MIN, INTERVALS

def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def generate_signal_multi(symbol):
    trends = []
    last_closes = []
    
    for interval in INTERVALS:
        df = get_klines(symbol, interval=interval)
        df['ema_fast'] = df['close'].ewm(span=EMA_FAST, adjust=False).mean()
        df['ema_slow'] = df['close'].ewm(span=EMA_SLOW, adjust=False).mean()
        df['rsi'] = calculate_rsi(df, RSI_PERIOD)
        last = df.iloc[-1]
        
        if last['ema_fast'] > last['ema_slow'] and last['rsi'] < RSI_LONG_MAX:
            trends.append("LONG")
        elif last['ema_fast'] < last['ema_slow'] and last['rsi'] > RSI_SHORT_MIN:
            trends.append("SHORT")
        else:
            trends.append("NEUTRAL")
        
        last_closes.append(float(last['close']))
    
    # Confirm signal if all intervals align
    if all(t == "LONG" for t in trends):
        entry = last_closes[-1]
        sl = entry * 0.98
        tp1 = entry * 1.02
        tp2 = entry * 1.04
        tp3 = entry * 1.06
        return ("LONG", entry, sl, tp1, tp2, tp3)
    
    elif all(t == "SHORT" for t in trends):
        entry = last_closes[-1]
        sl = entry * 1.02
        tp1 = entry * 0.98
        tp2 = entry * 0.96
        tp3 = entry * 0.94
        return ("SHORT", entry, sl, tp1, tp2, tp3)
    
    return None
