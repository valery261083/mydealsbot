import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = os.getenv("TELEGRAM_CHANNEL")

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

text = """
🔥 Тестове повідомлення

Якщо ти бачиш це повідомлення в каналі, бот працює.
"""

requests.post(url, json={
    "chat_id": CHANNEL,
    "text": text
})

print("Message sent")
