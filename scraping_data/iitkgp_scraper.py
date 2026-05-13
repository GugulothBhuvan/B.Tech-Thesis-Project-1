import requests
from bs4 import BeautifulSoup
import os
import json
import time
from urllib.parse import urljoin, urlparse

BASE_URL = "https://www.iitkgp.ac.in"
START_PATH = "/"
OUTPUT_DIR = "iitkgp_pages"
FILES_DIR = os.path.join(OUTPUT_DIR, "downloads")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FILES_DIR, exist_ok=True)

seen = set()
to_crawl = [START_PATH]

def clean_page(soup):
    # Remove navigation, footer, scripts, etc.
    for selector in ["script", "style", "footer", "nav"]:
        for tag in soup.select(selector):
            tag.decompose()
    return soup

def extract_text(soup):
    texts = []
    for tag in soup.find_all(["p", "li", "th", "td", "caption", "blockquote", "pre", "dd", "dt", "h1","h2","h3","h4","h5","h6"], recursive=True):
        txt = tag.get_text(" ", strip=True)
        if txt:
            texts.append(txt)
    return texts

def download_file(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        filename = os.path.basename(urlparse(url).path)
        if not filename:  # handle URLs ending with /
            filename = f"file_{int(time.time())}"
        filepath = os.path.join(FILES_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(r.content)
        return filepath
    except Exception as e:
        print(f"⚠️ Failed to download {url}: {e}")
        return None

def parse_page(path):
    url = urljoin(BASE_URL, path)
    print("Fetching", url)
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    soup = clean_page(soup)

    title = soup.title.get_text(strip=True) if soup.title else url
    content_texts = extract_text(soup)

    images = []
    files = []

    # Collect images
    for img in soup.select("img[src]"):
        img_url = urljoin(url, img["src"])
        local_path = download_file(img_url)
        if local_path:
            images.append(local_path)

    # Collect PDFs, docs, etc.
    for a in soup.select('a[href]'):
        link = urljoin(url, a["href"])
        if link.endswith((".pdf", ".docx", ".doc", ".xls", ".xlsx", ".zip")):
            local_path = download_file(link)
            if local_path:
                files.append(local_path)

    page_data = {
        "url": url,
        "title": title,
        "content": content_texts,
        "images": images,
        "files": files
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

    # Save JSON
    safe_name = path.strip("/").replace("/", "_") or "home"
    filename = os.path.join(OUTPUT_DIR, safe_name + ".json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(page_json, f, ensure_ascii=False, indent=2)

    # Extract internal links
    for a in soup.select('a[href]'):
        href = a.get("href")
        if not href:
            continue
        full_url = urljoin(BASE_URL, href)
        if urlparse(full_url).netloc == urlparse(BASE_URL).netloc:  # stay inside site
            rel_path = urlparse(full_url).path
            if rel_path not in seen:
                to_crawl.append(rel_path)

    time.sleep(1)

print("✅ Scraping complete. Total pages crawled:", len(seen))
