import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium import webdriver
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

#############################################################################################3
driver = webdriver.Chrome()

COOKIE_FILE = "tradingview_cookies.pkl"


def save_cookies():
    """
        Save Cookie
    """
    with open(COOKIE_FILE, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
    # log_message("Save cookies")


def load_cookies():
    """
        Load Cookies
    """
    try:
        with open(COOKIE_FILE, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        # log_message("Set cookies")
    except FileNotFoundError:
        # log_message("Cookies Not found")
        print('Cookie Not Found')


try:

    driver.get("https://judotv.com/")

    load_cookies()

    driver.refresh()
    input('****')
    try:
        login_button = driver.find_element(By.XPATH,
                                           '//*[@id="judo-tv"]/div/div[2]/div/header/div[2]/div[1]/div[2]/button')
        login_button.click()
        sleep(5)
        input('---')
        username = driver.find_element(By.NAME, "Username")
        password = driver.find_element(By.NAME, "Password")
        username.send_keys("yivic44760@cotigz.com")  # username
        password.send_keys("mobin2003")  # password
        password.send_keys(Keys.RETURN)

        sleep(5)
        driver.switch_to.default_content()
        # log_message("Login")
        sleep(10)
        save_cookies()
    except:
        print('Login')
except:
    print('cant Login')

input('ok ?')
try:

    allow_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
    )
    allow_button.click()
    print("1 Cookie Button")
except:
    print("0 Cookie Button")
#####################################################################################################




def read_last_line(file_path):
    """خواندن آخرین خط از فایل"""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            return lines[-1].strip() if lines else None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def remove_last_line(file_path):
    """حذف آخرین خط از فایل"""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        with open(file_path, 'w') as file:
            file.writelines(lines[:-1])
    except Exception as e:
        print(f"Error removing last line: {e}")


def get_driver(url):
    get_page = driver.get(url=url)
    html_source = get_page.get_attribute('outerHTML')
    return html_source

def fetch_html(url):
    """دریافت HTML از URL"""
    try:
        response = get_driver(url)
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None


def determine_judo_winner(html_content):
    """تحلیل HTML و استخراج برنده و جزئیات مسابقه"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # استخراج نام و کشور جودوکاران
    judoka_elements = soup.find_all('div', class_='text-xs font-medium leading-4')
    judokas = []
    for elem in judoka_elements:
        name = elem.get_text(strip=True)
        country_elem = elem.find_previous('div', class_='w-full text-center text-xs font-bold')
        country = country_elem.get_text(strip=True) if country_elem else 'Unknown'
        judokas.append({'name': name, 'country': country})

    # استخراج امتیازات
    score_elements = soup.find_all('div', class_='grid text-center grid-cols-4 gap-1')
    scores = []
    for i, score_elem in enumerate(score_elements):
        score_data = {'name': judokas[i]['name'], 'country': judokas[i]['country'], 'ippon': 0, 'waza_ari': 0,
                      'yuko': 0, 'shido': 0}
        cells = score_elem.find_all('div', class_=['@xs:text-lg', '@xs:w-6 @xs:h-6 h-4 w-4 relative'])
        for cell in cells:
            if cell.get('title') == 'Ippon' and cell.get_text(strip=True).isdigit():
                score_data['ippon'] = int(cell.get_text(strip=True))
            elif cell.get('title') == 'Waza-ari' and cell.get_text(strip=True).isdigit():
                score_data['waza_ari'] = int(cell.get_text(strip=True))
            elif cell.get('title') == 'Yuko' and cell.get_text(strip=True).isdigit():
                score_data['yuko'] = int(cell.get_text(strip=True))
            elif cell.get('title') == 'Penalty' and cell.find('div', class_='bg-yellow'):
                score_data['shido'] += 1
        scores.append(score_data)

    # استخراج تکنیک‌ها و زمان‌بندی
    events = []
    event_elements = soup.find_all('div', class_='grid grid-cols-[1fr,auto,1fr] gap-4')
    for event_elem in event_elements:
        time_elem = event_elem.find('div', class_='flex items-center text-center text-sm font-bold')
        technique_elem = event_elem.find('h4', class_='text-base font-bold')
        if time_elem and technique_elem:
            time = time_elem.get_text(strip=True)
            technique = technique_elem.get_text(strip=True)
            # تشخیص جودوکار (بر اساس رنگ پس‌زمینه: سفید یا آبی)
            judoka_side = event_elem.find('button', class_='bg-white/80') or event_elem.find('button',
                                                                                             class_='bg-blue/80')
            judoka_name = scores[0]['name'] if 'bg-white' in judoka_side['class'] else scores[1]['name']
            events.append({'time': time, 'technique': technique, 'judoka': judoka_name})

    # تعیین برنده
    winner = None
    if scores[0]['ippon'] > scores[1]['ippon']:
        winner = f"{scores[0]['name']} ({scores[0]['country']})"
    elif scores[1]['ippon'] > scores[0]['ippon']:
        winner = f"{scores[1]['name']} ({scores[1]['country']})"
    elif scores[0]['waza_ari'] > scores[1]['waza_ari']:
        winner = f"{scores[0]['name']} ({scores[0]['country']})"
    elif scores[1]['waza_ari'] > scores[0]['waza_ari']:
        winner = f"{scores[1]['name']} ({scores[1]['country']})"
    elif scores[0]['yuko'] > scores[1]['yuko']:
        winner = f"{scores[0]['name']} ({scores[0]['country']})"
    elif scores[1]['yuko'] > scores[0]['yuko']:
        winner = f"{scores[1]['name']} ({scores[1]['country']})"
    elif scores[0]['shido'] < scores[1]['shido']:
        winner = f"{scores[0]['name']} ({scores[0]['country']})"
    elif scores[1]['shido'] < scores[0]['shido']:
        winner = f"{scores[1]['name']} ({scores[0]['country']})"
    else:
        winner = "Draw or insufficient data"

    return winner, scores, events


def main():
    file_path = 'watch.txt'
    output_dir = 'judo_results'

    # ایجاد پوشه برای ذخیره فایل‌های JSON
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    while True:
        # خواندن آخرین خط
        url = read_last_line(file_path)
        if not url:
            print("No more URLs to process.")
            break

        print(f"Processing URL: {url}")

        # دریافت HTML
        html_content = fetch_html(url)
        if not html_content:
            print(f"Skipping {url} due to fetch error.")
            remove_last_line(file_path)
            continue

        # تحلیل مسابقه
        winner, scores, events = determine_judo_winner(html_content)

        # استخراج شماره مسابقه از URL برای نام فایل منحصربه‌فرد
        contest_id = url.split('/')[-1]

        # ایجاد داده‌های JSON
        match_data = {
            'contest_id': contest_id,
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'judokas': [
                {
                    'name': scores[0]['name'],
                    'country': scores[0]['country'],
                    'scores': {
                        'ippon': scores[0]['ippon'],
                        'waza_ari': scores[0]['waza_ari'],
                        'yuko': scores[0]['yuko'],
                        'shido': scores[0]['shido']
                    }
                },
                {
                    'name': scores[1]['name'],
                    'country': scores[1]['country'],
                    'scores': {
                        'ippon': scores[1]['ippon'],
                        'waza_ari': scores[1]['waza_ari'],
                        'yuko': scores[1]['yuko'],
                        'shido': scores[1]['shido']
                    }
                }
            ],
            'events': events,
            'winner': winner
        }

        # نام فایل بر اساس برنده و شماره مسابقه
        winner_name = winner.split(' (')[0].replace(' ', '_') if winner != "Draw or insufficient data" else 'Draw'
        file_name = f"{winner_name}_{contest_id}.json"
        file_path_json = os.path.join(output_dir, file_name)

        # ذخیره JSON
        with open(file_path_json, 'w', encoding='utf-8') as f:
            json.dump(match_data, f, ensure_ascii=False, indent=4)

        print(f"Saved result to {file_path_json}")

        # حذف خط از فایل
        remove_last_line(file_path)


if __name__ == '__main__':
    main()