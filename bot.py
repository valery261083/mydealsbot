import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = os.getenv("TELEGRAM_CHANNEL")

headers = {
    "User-Agent": "Mozilla/5.0"
}

search_url = "https://www.amazon.se/s?k=rea"

r = requests.get(search_url, headers=headers, timeout=20)
soup = BeautifulSoup(r.text, "html.parser")

products = soup.select("div[data-component-type='s-search-result']")

text = "🔎 Пошук Amazon.se: rea\n\n"

found = 0

for product in products[:5]:
    title_el = product.select_one("h2 span")
    link_el = product.select_one("a.a-link-normal.s-no-outline")
    price_el = product.select_one("span.a-price span.a-offscreen")

    if title_el and link_el and price_el:
        title = title_el.get_text(strip=True)
        price = price_el.get_text(strip=True)
        link = "https://www.amazon.se" + link_el.get("href").split("?")[0]

        text += f"🔥 {title}\n"
        text += f"Pris: {price}\n"
        text += f"👉 {link}\n\n"
        found += 1

if found == 0:
    text = "❌ Товари не знайдено через пошук. Amazon блокує або ховає результати."

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(telegram_url, json={
    "chat_id": CHANNEL,
    "text": text
})

print(text)
