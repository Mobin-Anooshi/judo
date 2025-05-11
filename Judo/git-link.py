# import requests
# import json
#
# base_url = "https://judotv.com/api/v2/competitions/"
# headers = {
#     "User-Agent": "Mozilla/5.0"
# }
#
# # Fetch competitions from 2014 to 2019
# date_from = "2014-01-01"
# date_to = "2025-12-31"
# page = 1
# all_competitions = []
#
# # Step 1: Fetch all competitions
# while True:
#     params = {
#         "DateFrom": date_from,
#         "DateTo": date_to,
#         "PerPage": 50,
#         "Page": page,
#         "SortingField": "date_from.asc"
#     }
#     print(f"📄 Fetching competitions page {page}...")
#     response = requests.get(base_url, params=params, headers=headers)
#
#     if response.status_code != 200:
#         print(f"❌ Failed to fetch page {page}: Status code {response.status_code}")
#         break
#
#     try:
#         data = response.json()
#     except Exception as e:
#         print("❌ Failed to parse JSON:", e)
#         break
#
#     competitions = data.get("list", [])
#     if not competitions:
#         print("✅ No more competitions.")
#         break
#
#     all_competitions.extend(competitions)
#     page += 1
#
# # Step 2: Fetch match/draw data for each competition
# all_matches = []
# for comp in all_competitions:
#     external_id = comp["externalId"]
#     match_url = f"https://judotv.com/api/v2/competitions/{external_id}/draw"  # Hypothetical endpoint
#     print(f"📄 Fetching matches for competition {external_id}...")
#
#     response = requests.get(match_url, headers=headers)
#
#     if response.status_code != 200:
#         print(f"❌ Failed to fetch matches for {external_id}: Status code {response.status_code}")
#         continue
#
#     try:
#         match_data = response.json()
#         matches = match_data.get("matches", [])  # Adjust based on actual API structure
#         filtered_matches = [
#             {
#                 "competition_id": external_id,
#                 "match_id": match.get("id"),
#                 "players": match.get("players"),
#                 "result": match.get("result"),
#                 "category": match.get("category")
#             }
#             for match in matches
#         ]
#         all_matches.extend(filtered_matches)
#     except Exception as e:
#         print(f"❌ Failed to parse matches for {external_id}: {e}")
#         continue
#
# # Step 3: Save matches to JSON
# with open("filtered_matches_2014_2025.json", "w") as f:
#     json.dump(all_matches, f, indent=2)
#
# print(f"✅ Done. Total matches processed: {len(all_matches)}")
import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

base_url = "https://judotv.com/api/v2/competitions/"
draw_base_url = "https://judotv.com/competitions/{}/draw"
headers = {
    "User-Agent": "Mozilla/5.0"
}

# تنظیمات selenium برای سرعت بیشتر
chrome_options = Options()
chrome_options.add_argument("--headless")  # بدون باز کردن مرورگر
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)

# گرفتن مسابقات از ۲۰۱۴ تا ۲۰۱۹
date_from = "2014-01-01"
date_to = "2019-12-31"
page = 1
all_competitions = []

while True:
    params = {
        "DateFrom": date_from,
        "DateTo": date_to,
        "PerPage": 50,
        "Page": page,
        "SortingField": "date_from.asc"
    }
    print(f"📄 در حال گرفتن صفحه {page} از مسابقات...")
    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code != 200:
        print(f"❌ خطا در گرفتن صفحه {page}: کد وضعیت {response.status_code}")
        break

    try:
        data = response.json()
    except Exception as e:
        print(f"❌ خطا در تجزیه JSON: {e}")
        break

    competitions = data.get("list", [])
    if not competitions:
        print("✅ دیگه مسابقه‌ای نیست.")
        break

    all_competitions.extend(competitions)
    page += 1

# گرفتن داده‌های draw با selenium
all_matches = []
for comp in all_competitions[:5]:  # فقط ۵ مسابقه برای تست
    external_id = comp.get("externalId")
    if not external_id or external_id == "None":
        print(f"❌ externalId نامعتبر برای مسابقه: {comp.get('name')}")
        continue

    draw_url = draw_base_url.format(external_id)
    print(f"📄 در حال اسکرپ کردن draw برای مسابقه {external_id}...")

    try:
        driver.get(draw_url)
        time.sleep(2)  # صبر برای لود کامل صفحه
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # فرض: بازی‌ها تو تگ div با کلاس "match-item" (باید با HTML واقعی جایگزین بشه)
        match_elements = soup.find_all("div", class_="match-item")  # کلاس واقعی رو پیدا کن
        matches = []
        for match in match_elements:
            match_data = {
                "competition_name": comp.get("name"),
                "competition_externalId": external_id,
                "dateFrom": comp.get("dateFrom"),
                "dateTo": comp.get("dateTo"),
                "match_id": match.get("data-id", "unknown"),
                "players": match.find("span", class_="players").text if match.find("span", class_="players") else "N/A",
                "result": match.find("span", class_="result").text if match.find("span", class_="result") else "N/A",
                "category": match.find("span", class_="category").text if match.find("span",
                                                                                     class_="category") else "N/A"
            }
            matches.append(match_data)
        all_matches.extend(matches)
        print(f"✅ {len(matches)} بازی برای {external_id} پیدا شد.")
    except Exception as e:
        print(f"❌ خطا در اسکرپ کردن draw برای {external_id}: {e}")
        continue

    time.sleep(1)  # فاصله بین درخواست‌ها

driver.quit()

# ذخیره داده‌ها به صورت JSON
with open("scraped_matches_2015 _2019.json", "w") as f:
    json.dump(all_matches, f, indent=2)

print(f"✅ تموم شد. تعداد کل بازی‌های پردازش‌شده: {len(all_matches)}")