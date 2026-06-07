import os
import re
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = os.getenv("TELEGRAM_CHANNEL")

SOURCES = [
    "https://www.pepperdeals.se/search?q=amazon",
    "https://www.hittarabatter.com/",
    "https://www.adealsweden.com/"
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

found_deals = []

def find_discount(text):
    matches = re.findall(r"(\d{2,3})\s?%", text)
    for m in matches:
        percent = int(m)
        if percent >= 70:
            return percent
    return None

for url in SOURCES:
    try:
        r = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")

        articles = soup.select("article, div, a")

        for item in articles:
            text = item.get_text(" ", strip=True)
            discount = find_discount(text)

            if discount:
                link_el = item if item.name == "a" else item.select_one("a")
                link = link_el.get("href") if link_el else url

                if link and link.startswith("/"):
                    base = url.split("/")[0] + "//" + url.split("/")[2]
                    link = base + link

                if text and len(text) > 20:
                    found_deals.append({
                        "discount": discount,
                        "text": text[:180],
                        "link": link
                    })

    except Exception as e:
        print(f"Error with {url}: {e}")

found_deals = sorted(found_deals, key=lambda x: x["discount"], reverse=True)

message = "🔥 Знижки мінімум -70%:\n\n"

if not found_deals:
    message = "❌ Знижок від 70% зараз не знайдено."
else:
    for deal in found_deals[:10]:
        message += f"🔥 -{deal['discount']}%\n"
        message += f"{deal['text']}\n"
        message += f"👉 {deal['link']}\n\n"

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(telegram_url, json={
    "chat_id": CHANNEL,
    "text": message
})

print(message)
