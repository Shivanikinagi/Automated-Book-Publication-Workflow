from playwright.sync_api import sync_playwright
import os
import re

def scrape_chapter():
    print("[Web Scraper] Starting scrape_chapter...")
    url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    try:
        with sync_playwright() as p:
            print("[Web Scraper] Launching browser...")
            browser = p.chromium.launch()
            page = browser.new_page()
            print(f"[Web Scraper] Navigating to {url}...")
            page.goto(url)
            print("[Web Scraper] Waiting for content...")
            page.wait_for_selector("#mw-content-text", timeout=10000)
            print("[Web Scraper] Capturing screenshot...")
            page.screenshot(path="screenshots/chapter.png")
            print("[Web Scraper] Extracting text...")
            content = page.inner_text("#mw-content-text")
            content = re.sub(r'\[\d+\]', '', content)
            content = re.sub(r'\s+', ' ', content).strip()
            content = ''.join(c for c in content if c.isprintable())
            print("[Web Scraper] Saving text to data/chapter_original.txt...")
            with open("data/chapter_original.txt", "w", encoding="utf-8") as f:
                f.write(content)
            browser.close()
            print("[Web Scraper] Scrape completed successfully.")
            return content
    except Exception as e:
        print(f"[Web Scraper] Scrape failed: {e}")
        raise