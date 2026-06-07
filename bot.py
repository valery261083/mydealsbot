import os
import re
import json
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = os.getenv("TELEGRAM_CHANNEL")

SOURCES = [
    "https://www.pepperdeals.se/search?q=amazon",
    "https://www.hittarabatter.com/",
    "https://www.adealsweden.com
