import requests

def get_all_pairs():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    data = requests.get(url).json()
    pairs = [s["symbol"] for s in data["symbols"] 
             if s["quoteAsset"] == "USDT" and s["status"] == "TRADING"]
    return pairs
