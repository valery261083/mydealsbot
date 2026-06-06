import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = os.getenv("TELEGRAM_CHANNEL")

text = """
🔥 Знижка на Amazon.se

Товар: Приклад навушників
Було: 999 kr
Зараз: 299 kr
Знижка: -70%

👉 https://www.amazon.se/
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

response = requests.post(url, json={
    "chat_id": CHANNEL,
    "text": text
})

print("Status:", response.status_code)
print("Response:", response.text)
