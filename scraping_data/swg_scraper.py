import os
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json
import time

async def scrape_site(base_url, output_dir="swg_json"):
    os.makedirs(output_dir, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(base_url, wait_until="networkidle")
        
        # Get all internal page links
        soup = BeautifulSoup(await page.content(), "html.parser")
        links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith(base_url)]
        links = list(set(links))  # remove duplicates

        for idx, link in enumerate(links, start=1):
            try:
                await page.goto(link, wait_until="networkidle")
                page_soup = BeautifulSoup(await page.content(), "html.parser")

                # Extract title and textual content
                title_tag = page_soup.find(['h1', 'h2', 'title'])
                title = title_tag.get_text(strip=True) if title_tag else f"Page {idx}"

                paragraphs = page_soup.find_all('p')
                content = "\n".join([p.get_text(strip=True) for p in paragraphs])

                # Save as JSON
                page_data = {
                    "url": link,
                    "title": title,
                    "content": content
                }

                filename = os.path.join(output_dir, f"page_{idx}.json")
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(page_data, f, indent=4, ensure_ascii=False)

                print(f"✅ Scraped: {link}")

                time.sleep(1)  # polite scraping

            except Exception as e:
                print(f"⚠️ Failed to scrape {link}: {e}")

        await browser.close()
    print("🎉 Scraping complete.")

# Run the scraper
asyncio.run(scrape_site("https://swgiitkgp.org/"))
