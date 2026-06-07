import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = os.getenv("TELEGRAM_CHANNEL")

headers = {
    "User-Agent": "Mozilla/5.0"
}

url = "https://www.amazon.se/deals"

try:
    r = requests.get(url, headers=headers, timeout=20)

    text = f"✅ Amazon Deals сторінка доступна\nКод відповіді: {r.status_code}"

except Exception as e:
    text = f"❌ Помилка\n{e}"

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    json={
        "chat_id": CHANNEL,
        "text": text
    }
)

print(text)
