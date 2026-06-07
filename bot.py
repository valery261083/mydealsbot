import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = os.getenv("TELEGRAM_CHANNEL")

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://www.amazon.se/deals"

r = requests.get(url, headers=headers, timeout=20)
soup = BeautifulSoup(r.text, "html.parser")

items = soup.select("a[href*='/dp/']")

links = []
for item in items:
    href = item.get("href")
    if href and "/dp/" in href:
        full_link = "https://www.amazon.se" + href.split("?")[0]
        if full_link not in links:
            links.append(full_link)

text = "🔎 Знайдено товарів на Amazon Deals:\n\n"

for link in links[:5]:
    text += f"👉 {link}\n"

if not links:
    text = "❌ Товари не знайдено. Amazon може приховувати їх від бота."

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(telegram_url, json={
    "chat_id": CHANNEL,
    "text": text
})

print(text)
