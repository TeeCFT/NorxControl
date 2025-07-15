
import requests
import time

API_KEY = "CLIWIVGLHVS1X4W6"
SYMBOL = "EURUSD"
INTERVAL = "1min"

def get_candles():
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={SYMBOL}&interval={INTERVAL}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    time_series_key = f"Time Series ({INTERVAL})"
    if time_series_key not in data:
        print("❌ Error fetching data or hit rate limit.")
        return []

    candles = []
    for timestamp, values in list(data[time_series_key].items())[:20]:
        candles.append({
            "time": timestamp,
            "open": float(values["1. open"]),
            "high": float(values["2. high"]),
            "low": float(values["3. low"]),
            "close": float(values["4. close"])
        })
    candles.reverse()
    return candles

def detect_patterns(candles):
    for i in range(5, len(candles)):
        c1 = candles[i-2]
        c2 = candles[i-1]
        c3 = candles[i]

        if c1["low"] > c2["high"]:
            print(f"[{c3['time']}] 🔷 Bullish FVG Detected")
        if c1["high"] < c2["low"]:
            print(f"[{c3['time']}] 🔶 Bearish FVG Detected")

        if c3["high"] > c1["high"] and c3["close"] > c1["high"]:
            print(f"[{c3['time']}] 📈 Break of Structure (Up)")
        if c3["low"] < c1["low"] and c3["close"] < c1["low"]:
            print(f"[{c3['time']}] 📉 Break of Structure (Down)")

        swing_high = max(c["high"] for c in candles[i-5:i-1])
        swing_low = min(c["low"] for c in candles[i-5:i-1])

        if c3["low"] < swing_low and c3["close"] > c3["open"] and (c3["open"] - c3["low"] > abs(c3["close"] - c3["open"])):
            print(f"[{c3['time']}] 🔺 Bullish Liquidity Sweep")

        if c3["high"] > swing_high and c3["close"] < c3["open"] and (c3["high"] - c3["open"] > abs(c3["close"] - c3["open"])):
            print(f"[{c3['time']}] 🔻 Bearish Liquidity Sweep")

def run():
    while True:
        try:
            candles = get_candles()
            if candles:
                detect_patterns(candles)
            print("⏳ Waiting 5 minutes...")
            time.sleep(300)
        except Exception as e:
            print("⚠️ Error:", e)
            time.sleep(60)

run()
