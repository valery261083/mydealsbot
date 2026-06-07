import os
import json
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = os.getenv("TELEGRAM_CHANNEL")

with open("deals.json", "r", encoding="utf-8") as f:
    deals = json.load(f)

deal = deals[0]

text = f"""
🔥 {deal['title']}

Було: {deal['old_price']}
Зараз: {deal['new_price']}
Знижка: {deal['discount']}

👉 {deal['link']}
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    json={
        "chat_id": CHANNEL,
        "text": text
    }
)

print("Deal sent")
