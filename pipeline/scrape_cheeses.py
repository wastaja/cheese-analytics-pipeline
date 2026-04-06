import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.thecheesesociety.co.uk"
START_URL = f"{BASE_URL}/products/cheese/"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/124.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
    "Connection": "keep-alive",
}

all_cheeses = []

excluded_keywords = [
    "voucher",
    "gift voucher",
    "gift vouchers",
]

for page_num in range(1, 5):
    if page_num == 1:
        url = START_URL
    else:
        url = f"{START_URL}?page={page_num}"

    print(f"Scraping page {page_num}: {url}")

    response = requests.get(url, headers=headers, timeout=20)
    print("status_code:", response.status_code)

    if response.status_code != 200:
        print(f"Skipping page {page_num} due to status {response.status_code}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    page_cheeses = []

    for a in soup.find_all("a", href=True):
        href = a["href"]

        name = a.get("title") or a.get_text(" ", strip=True)

        if name:
            name = name.split("£")[0].strip()
            name = " ".join(name.split())

        if "/product/" in href and name:
            full_url = href if href.startswith("http") else BASE_URL + href

            name_lower = name.lower()
            href_lower = href.lower()

            if any(keyword in name_lower for keyword in excluded_keywords):
                continue

            if any(keyword in href_lower for keyword in excluded_keywords):
                continue

            page_cheeses.append({
                "cheese_name": name,
                "cheese_url": full_url,
                "source_page": page_num
            })

    page_df = pd.DataFrame(page_cheeses).drop_duplicates()
    print(f"Found {len(page_df)} product links on page {page_num}")

    all_cheeses.extend(page_cheeses)

    time.sleep(1)

df = pd.DataFrame(all_cheeses).drop_duplicates()

print("\nFinal preview:")
print(df.head(20))
print("rows:", len(df))

df.to_csv("data/raw/cheeses_list.csv", index=False)
print("saved to data/raw/cheeses_list.csv")