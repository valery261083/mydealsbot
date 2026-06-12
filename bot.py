import os
import re
import json
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = os.getenv("TELEGRAM_CHANNEL")

SOURCES = [
    {
        "name": "PepperDeals",
        "url": "https://www.pepperdeals.se/search?q=amazon"
    },
    {
        "name": "HittaRabatter",
        "url": "https://www.hittarabatter.com/"
    },
    {
        "name": "Adealsweden",
        "url": "https://www.adealsweden.com/"
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def load_sent_links():
    try:
        with open("sent_links.json", "r", encoding="utf-8") as f:
            return set(json.load(f))
    except:
        return set()

def save_sent_links(links):
    with open("sent_links.json", "w", encoding="utf-8") as f:
        json.dump(list(links)[-500:], f, ensure_ascii=False, indent=2)

def analyze_deal(text):
    text_low = text.lower()

    if "prisfel" in text_low or "felpris" in text_low:
        return True, "⚠️ PRISFEL"

    patterns = [
        r"(\d{2,3})\s?%\s?rabatt",
        r"rabatt\s?(\d{2,3})\s?%",
        r"(\d{2,3})\s?%\s?off",
        r"discount\s?(\d{2,3})\s?%"
    ]

    for pattern in patterns:
        match = re.search(pattern, text_low)
        if match:
            percent = int(match.group(1))

            if percent >= 70:
                return True, f"🔥 -{percent}%"

            if percent >= 50 and "amazon" in text_low:
                return True, f"🔥 -{percent}% Amazon"

    return False, None

def clean_text(text):
    text = re.sub(r"\s+", " ", text).strip()
    return text[:180]

sent_links = load_sent_links()
new_sent_links = set(sent_links)
found = []

for source in SOURCES:
    try:
        r = requests.get(source["url"], headers=HEADERS, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")

        for item in soup.select("article, a"):
            text = item.get_text(" ", strip=True)
            ok, label = analyze_deal(text)

            if not ok or len(text) < 20:
                continue

            link_el = item if item.name == "a" else item.select_one("a")
            if not link_el:
                continue

            link = link_el.get("href")
            if not link:
                continue

            if link.startswith("/"):
                base = source["url"].split("/")[0] + "//" + source["url"].split("/")[2]
                link = base + link

            if link in sent_links:
                continue

            found.append({
                "source": source["name"],
                "label": label,
                "text": clean_text(text),
                "link": link
            })

            new_sent_links.add(link)

    except Exception as e:
        print("Error:", source["name"], e)

if found:
    message = "🔥 Нові сильні знижки:\n\n"

    for deal in found[:10]:
        message += f"{deal['label']} | {deal['source']}\n"
        message += f"{deal['text']}\n"
        message += f"👉 {deal['link']}\n\n"

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(telegram_url, json={
        "chat_id": CHANNEL,
        "text": message
    })

    save_sent_links(new_sent_links)
    print(message)
else:
    print("Нових сильних знижок немає.")
