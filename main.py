import time
from binance_pairs import get_all_pairs
from signals import generate_signal_multi
from scanner import get_klines
from chart import draw_chart
from telegram_sender import send_signal

print("🚀 PRO Crypto Bot with Multi-Timeframe & SR starting...")

pairs = get_all_pairs()
print(f"✅ Total USDT pairs: {len(pairs)}")

while True:
    print("\n🔄 New scan cycle starting...")
    
    for symbol in pairs[:50]:  # change to all pairs in production
        try:
            print(f"📊 Checking {symbol}")
            df = get_klines(symbol, interval="1h")
            print(f"✔ Data loaded for {symbol}")
            
            signal = generate_signal_multi(symbol)
            print(f"🔍 Signal result for {symbol}: {signal}")
            
            if signal:
                trade, entry, sl, tp1, tp2, tp3 = signal
                print(f"🚨 SIGNAL FOUND on {symbol} -> {trade}")
                
                print("📸 Generating chart...")
                chart_file = draw_chart(df, symbol, trade, entry, sl, tp1, tp2, tp3)
                
                message = f"""
💹 ${symbol.replace('USDT','')} — {trade}
Entry: {entry:.4f}
SL: {sl:.4f}
TP1: {tp1:.4f}
TP2: {tp2:.4f}
TP3: {tp3:.4f}
DYOR
"""
                print("📤 Sending signal to Telegram...")
                send_signal(message, chart_file)
                print("✅ Signal sent successfully")
        
        except Exception as e:
            print(f"❌ ERROR on {symbol}: {e}")
    
    print("\n⏳ Waiting 5 minutes before next scan...\n")
    time.sleep(300)
