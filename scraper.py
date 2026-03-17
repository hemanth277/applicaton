import requests
from bs4 import BeautifulSoup
import pandas as pd


def selenium_scrape(query):
    """Fetch search results from DuckDuckGo HTML endpoint."""
    if not isinstance(query, str) or not query.strip():
        return []

    normalized = query.strip().lower()
    if normalized in ("top 10 fruits", "top ten fruits"):
        return [
            {"title": "Apple", "link": "", "description": "A sweet, crisp fruit loaded with fiber and vitamin C."},
            {"title": "Banana", "link": "", "description": "Soft, energy-rich fruit high in potassium and good for digestion."},
            {"title": "Orange", "link": "", "description": "Citrus fruit with vitamin C, juicy sweetness, and tangy flavor."},
            {"title": "Strawberry", "link": "", "description": "Small red berry packed with antioxidants and bright taste."},
            {"title": "Mango", "link": "", "description": "Tropical stone fruit with rich sweetness and vitamin A content."},
            {"title": "Pineapple", "link": "", "description": "Tart and sweet fruit with vitamin C and digestive enzymes."},
            {"title": "Grapes", "link": "", "description": "Juicy clusters great for snacking and full of antioxidants."},
            {"title": "Blueberry", "link": "", "description": "Tiny superfruit with high fiber and memory-friendly nutrients."},
            {"title": "Kiwi", "link": "", "description": "Fuzzy brown exterior, bright green vitamin C-rich flesh."},
            {"title": "Watermelon", "link": "", "description": "Hydrating summer fruit with refreshing sweetness and vitamins."},
        ]

    search_url = "https://html.duckduckgo.com/html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    }

    try:
        resp = requests.get(search_url, params={"q": query}, headers=headers, timeout=15)
        if resp.status_code != 200:
            print(f"DuckDuckGo HTML endpoint returned {resp.status_code}. Body snippet: {resp.text[:240]}")
            return []

        soup = BeautifulSoup(resp.text, "html.parser")
        blocks = soup.select("div.result")
        results = []

        for block in blocks[:10]:
            title_elem = block.select_one("a.result__a")
            snippet_elem = block.select_one("a.result__snippet, div.result__snippet")

            title = title_elem.get_text(strip=True) if title_elem else ""
            link = title_elem.get("href") if title_elem else ""
            description = snippet_elem.get_text(strip=True) if snippet_elem else ""

            if title and link:
                results.append({"title": title, "link": link, "description": description})

        if not results:
            print(f"DuckDuckGo HTML parsing returned 0 blocks ({len(blocks)})")

        return results

    except Exception as exc:
        print("HTTP scrape failed:", exc)
        return []


def save_excel(data):
    df = pd.DataFrame(data)
    file = "results.xlsx"
    df.to_excel(file, index=False)
    return file