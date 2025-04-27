# competition_links.py
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://judotv.com/competitions")
    
    # اسکرول چند مرحله‌ای
    for _ in range(20):
        page.mouse.wheel(0, 2000)
        page.wait_for_timeout(1500)

    links = page.query_selector_all("a.card")
    for link in links:
        href = link.get_attribute("href")
        if href:
            print(href)

    browser.close()
