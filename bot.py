import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = os.getenv("TELEGRAM_CHANNEL")

url = "https://www.pepperdeals.se/search?q=amazon"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers, timeout=20)
soup = BeautifulSoup(r.text, "html.parser")

text = "🔥 Знижки, повʼязані з Amazon.se:\n\n"

deals = soup.select("article")

found = 0

for deal in deals[:5]:
    title_el = deal.select_one("a")
    if title_el:
        title = title_el.get_text(" ", strip=True)
        link = title_el.get("href")

        if link and link.startswith("/"):
            link = "https://www.pepperdeals.se" + link

        if title:
            text += f"🔥 {title}\n👉 {link}\n\n"
            found += 1

if found == 0:
    text = "❌ Не вдалося знайти знижки на Pepper Deals."

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(telegram_url, json={
    "chat_id": CHANNEL,
    "text": text
})

print(text)
