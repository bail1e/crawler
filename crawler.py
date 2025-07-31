import requests
from bs4 import BeautifulSoup
import time
import random

# Tor proxy settings
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# Example seed .onion URLs (MUST be public & safe - REPLACE these with academic .onion lists)
seed_urls = [
    "http://duskgytldkxiuqc6.onion",  # Example (DuckDuckGo on dark web)
]

# User-agent spoofing
headers = {
    "User-Agent": "Mozilla/5.0 (compatible; ResearchCrawler/1.0)"
}

visited = set()

def crawl(url, depth=1):
    if url in visited or depth <= 0:
        return

    try:
        print(f"[+] Crawling: {url}")
        visited.add(url)

        response = requests.get(url, proxies=proxies, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"[-] Failed: {url}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # Save or analyze the content
        with open("darkweb_pages.txt", "a", encoding="utf-8") as f:
            f.write(f"\n\n=== URL: {url} ===\n")
            f.write(soup.get_text())

        # Extract .onion links for further crawling
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            if ".onion" in href:
                if href.startswith('/'):
                    href = url + href
                elif not href.startswith("http"):
                    href = "http://" + href
                crawl(href, depth - 1)

        # Respectful crawling
        time.sleep(random.randint(3, 10))

    except Exception as e:
        print(f"[!] Error: {e}")

# Start crawling
for seed in seed_urls:
    crawl(seed, depth=2)
