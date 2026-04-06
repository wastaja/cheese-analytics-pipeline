import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
    "Connection": "keep-alive",
}

# wczytaj listę serów
cheeses_df = pd.read_csv("data/raw/cheeses_list.csv")

details = []

def clean_text(value):
    if value is None:
        return None
    value = str(value).strip()
    value = " ".join(value.split())
    return value if value else None

def extract_tasting_notes(soup):
    """
    Extracts tasting notes from the left-hand content section.
    Prefers paragraph text near the TASTING NOTES header.
    """
    header = soup.find(
        lambda tag: tag.name in ["h1", "h2", "h3", "h4"]
        and "TASTING NOTES" in tag.get_text(" ", strip=True).upper()
    )

    if not header:
        return None

    # znajdź najbliższy większy kontener sekcji
    container = header.find_parent(["div", "section"])
    if not container:
        return None

    paragraphs = container.find_all("p")
    text_parts = []

    for p in paragraphs:
        text = clean_text(p.get_text(" ", strip=True))
        if text and len(text) > 30:
            text_parts.append(text)

    if text_parts:
        return " ".join(text_parts)

    return None


def extract_key_facts(soup):
    """
    Parses only the KEY FACTS section, not the whole page.
    """
    key_facts = {
        "age": None,
        "country_of_origin": None,
        "milk_type": None,
        "organic": None,
        "pasteurisation": None,
        "region": None,
        "strength_of_cheese": None,
        "style_of_cheese": None,
    }

    key_facts_header = soup.find(
        lambda tag: tag.name in ["h1", "h2", "h3", "h4"]
        and "KEY FACTS" in tag.get_text(" ", strip=True).upper()
    )

    if not key_facts_header:
        return key_facts

    # try to find the nearest parent container that holds the section
    section_container = key_facts_header.find_parent()

    if not section_container:
        return key_facts

    section_text = section_container.get_text("\n", strip=True)
    lines = [clean_text(line) for line in section_text.split("\n")]
    lines = [line for line in lines if line]

    labels_map = {
        "Age": "age",
        "Country Of Origin": "country_of_origin",
        "Milk Type": "milk_type",
        "Organic": "organic",
        "Pasteurisation": "pasteurisation",
        "Region": "region",
        "Strength Of Cheese": "strength_of_cheese",
        "Style Of Cheese": "style_of_cheese",
    }

    for i, line in enumerate(lines):
        if line in labels_map and i + 1 < len(lines):
            key_facts[labels_map[line]] = lines[i + 1]

    return key_facts


for idx, row in cheeses_df.iterrows():
    cheese_name = row["cheese_name"]
    cheese_url = row["cheese_url"]

    print(f"[{idx + 1}/{len(cheeses_df)}] Scraping: {cheese_name}")

    try:
        response = requests.get(cheese_url, headers=HEADERS, timeout=20)

        if response.status_code != 200:
            print(f"Skipping {cheese_name} - status {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        tasting_notes = extract_tasting_notes(soup)
        key_facts = extract_key_facts(soup)

        details.append({
            "cheese_name": clean_text(cheese_name),
            "cheese_url": cheese_url,
            "tasting_notes": tasting_notes,
            "age": clean_text(key_facts.get("age")),
            "country_of_origin": clean_text(key_facts.get("country_of_origin")),
            "milk_type": clean_text(key_facts.get("milk_type")),
            "organic": clean_text(key_facts.get("organic")),
            "pasteurisation": clean_text(key_facts.get("pasteurisation")),
            "region": clean_text(key_facts.get("region")),
            "strength_of_cheese": clean_text(key_facts.get("strength_of_cheese")),
            "style_of_cheese": clean_text(key_facts.get("style_of_cheese")),
        })

        time.sleep(1)

    except Exception as e:
        print(f"Error scraping {cheese_name}: {e}")

details_df = pd.DataFrame(details)

print("\nPreview:")
print(details_df.head())

details_df.to_csv("data/raw/cheese_details.csv", index=False)
print("\nSaved to data/raw/cheese_details.csv")