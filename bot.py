import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = os.getenv("TELEGRAM_CHANNEL")

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

text = "🔥 Тест. Бот працює."

response = requests.post(url, json={
    "chat_id": CHANNEL,
    "text": text
})

print("Status:", response.status_code)
print("Response:", response.text)
print("Channel:", CHANNEL)
