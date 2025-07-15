import requests
import time

API_KEY = "CLIWIVGLHVS1X4W6"
SYMBOL = "EURUSD"
INTERVAL = "1min"
WEBHOOK_URL = "https://hook.us2.make.com/f7mcutb8igms2jxy5vkavmqpocy7f4e8"

def send_to_webhook(signal_type, time_label):
    data = {
        "symbol": SYMBOL,
        "signal": signal_type,
        "time": time_label
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 200:
            print(f"✅ Sent to webhook: {signal_type}")
        else:
            print(f"❌ Webhook failed with status: {response.status_code}")
    except Exception as e:
        print("⚠️ Webhook error:", e)

def get_candles():
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={SYMBOL}&interval={INTERVAL}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    key = f"Time Series ({INTERVAL})"
    if key not in data:
        print("❌ Data error or API limit hit")
        return []

    candles
