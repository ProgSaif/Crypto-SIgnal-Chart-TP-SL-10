import matplotlib.pyplot as plt
import numpy as np
from utils import detect_support_resistance

def draw_chart(df, symbol, trade, entry, sl, tp1, tp2, tp3):
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12,6))
    df = df[-50:]
    df['index'] = np.arange(len(df))
    
    # Candlesticks
    for idx, row in df.iterrows():
        color = 'green' if row['close'] >= row['open'] else 'red'
        ax.plot([row['index'], row['index']], [row['low'], row['high']], color='white')
        ax.add_patch(plt.Rectangle((row['index']-0.3, row['open']),
                                   0.6, row['close']-row['open'], color=color))
    
    # Entry / SL / TP
    if trade == "LONG":
        ax.hlines([entry], df['index'].min(), df['index'].max(), colors='blue', linestyles='solid', label='Entry')
        ax.hlines([sl], df['index'].min(), df['index'].max(), colors='red', linestyles='dashed', label='SL')
        ax.hlines([tp1,tp2,tp3], df['index'].min(), df['index'].max(), colors='lime', linestyles='dashed', label='TP')
    elif trade == "SHORT":
        ax.hlines([entry], df['index'].min(), df['index'].max(), colors='blue', linestyles='solid', label='Entry')
        ax.hlines([sl], df['index'].min(), df['index'].max(), colors='red', linestyles='dashed', label='SL')
        ax.hlines([tp1,tp2,tp3], df['index'].min(), df['index'].max(), colors='lime', linestyles='dashed', label='TP')
    
    # Support/Resistance
    support, resistance = detect_support_resistance(df, n=10)
    ax.hlines([support, resistance], df['index'].min(), df['index'].max(), colors='orange', linestyles='dotted', label='S/R')
    
    ax.set_title(f"{symbol} - {trade} Signal", fontsize=14)
    ax.set_xlabel("Candles")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    
    filename = f"{symbol}.png"
    plt.savefig(filename)
    plt.close(fig)
    return filename
