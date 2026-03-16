import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        }

        response = requests.get(url, headers=headers, timeout=10)

        print("Status code:", response.status_code)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")

        text = " ".join([p.get_text() for p in paragraphs])

        if not text.strip():
            return None

        return text

    except Exception as e:
        print("Scraping error:", e)
        return None