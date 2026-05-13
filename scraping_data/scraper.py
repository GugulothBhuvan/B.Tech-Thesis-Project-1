import requests
from bs4 import BeautifulSoup
import os
import json
import time
from urllib.parse import urljoin

BASE_URL = "https://wiki.metakgp.org"
START_PATH = "/w/Metakgp:About"   # starting page, can be changed
OUTPUT_DIR = "metakgp_pages"
os.makedirs(OUTPUT_DIR, exist_ok=True)

seen = set()
to_crawl = [START_PATH]


def clean_page(soup):
    # remove navigation & UI clutter
    for selector in ["#mw-navigation", "#p-personal", "#siteSub", ".editsection", ".mw-jump-link"]:
        for tag in soup.select(selector):
            tag.decompose()
    return soup


def extract_full_text(content_div):
    """
    Extract all meaningful text: paragraphs, lists, table cells, captions, references, etc.
    """
    texts = []
    for tag in content_div.find_all(["p", "li", "th", "td", "caption", "blockquote", "pre", "dd", "dt"], recursive=True):
        txt = tag.get_text(" ", strip=True)
        if txt:
            texts.append(txt)
    return texts


def parse_page(path):
    url = urljoin(BASE_URL, path)
    print("Fetching", url)
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    soup = clean_page(soup)

    # title
    title = soup.find("h1", {"id": "firstHeading"}).get_text(strip=True)

    # main content
    content_div = soup.find("div", {"id": "mw-content-text"})
    content_texts = extract_full_text(content_div)

    page_data = {
        "url": url,
        "title": title,
        "content": content_texts
    }
    return page_data, soup


while to_crawl:
    path = to_crawl.pop(0)
    if path in seen:
        continue
    seen.add(path)

    try:
        page_json, soup = parse_page(path)
    except Exception as e:
        print(f"Error parsing {path}: {e}")
        continue

    # save JSON
    safe_name = path.strip("/").replace("/", "_")
    filename = os.path.join(OUTPUT_DIR, safe_name + ".json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(page_json, f, ensure_ascii=False, indent=2)

    # extract links to other wiki pages
    for a in soup.select('a[href^="/w/"]'):
        href = a.get("href")
        if not href:
            continue
        href = href.split("#")[0]  # ignore in-page anchors
        if ":" in href and not href.startswith("/w/Metakgp:"):
            continue  # skip special/talk pages
        if href not in seen:
            to_crawl.append(href)

    time.sleep(1)  # politeness delay

print("✅ Scraping complete. Total pages crawled:", len(seen))
