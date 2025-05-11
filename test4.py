from selenium import webdriver
import pickle
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import copy
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC





# chrome_options = Options()
# chrome_options.add_argument("--headless")  #  headless
# chrome_options.add_argument("--disable-gpu")  # GPU
# chrome_options.add_argument("--window-size=1920,1080")
# driver = webdriver.Chrome(options=chrome_options)

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
    try :
        login_button = driver.find_element(By.XPATH, '//*[@id="judo-tv"]/div/div[2]/div/header/div[2]/div[1]/div[2]/button')
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
    except :
        print('Login')
except :
    print('cant Login')
    
input('ok ?')
try:
    # ﻢﻨﺘﻇﺭ ﻢﯿﻣﻮﻨﯿﻣ ﺕﺍ ﺪﮑﻤﻫ ﺎﮕﻫ ﺏﺎﺸﻫ ﻝﻭﺩ ﺐﺸﻫ
    allow_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
    )
    allow_button.click()
    print("ﺪﮑﻤﻫ ﭗﯾﺩﺍ ﺵﺩ ﻭ ﮏﻠﯿﮐ ﺵﺩ.")
except:
    print("ﺪﮑﻤﻫ ﻦﺑﻭﺩ، ﺍﺩﺎﻤﻫ ﻢﯾﺪﯿﻣ.")

#final
fin = {}

def process_data(data_list, z, ro):
    result = []
    for data in data_list:
        items = [item.strip() for item in data.split('\n') if item.strip()]
        
        for i in range(0, len(items), 2):
            if i + 1 < len(items):
                result.append({
                    'country': items[i],
                    'name': items[i + 1]
                })
    
    # اگر کلید z.text.replace('\n', ' ') در fin وجود نداشت، آن را ایجاد کن
    if z.text.replace('\n', ' ') not in fin:
        fin[z.text.replace('\n', ' ')] = {}
    
    # اگر کلید rounddd در داخل این بخش وجود نداشت، آن را ایجاد کن
    if ro not in fin[z.text.replace('\n', ' ')]:
        fin[z.text.replace('\n', ' ')][ro] = []
    
    # افزودن نتیجه پردازش شده به دیکشنری
    fin[z.text.replace('\n', ' ')][ro].append(result)
    
    return result




# چاپ دیکشنری نهایی
# print(fin)


def flatten_matches(matches):
    """تبدیل لیست‌های تو در تو به لیست تخت"""
    flat_matches = []
    for match_group in matches:
        if isinstance(match_group, list):
            flat_matches.extend(match_group)
        else:
            flat_matches.append(match_group)
    return flat_matches

def restructure_data(data):
    data = copy.deepcopy(data)
    new_data = {}
    
    for stage_name, stage_data in data.items():
        new_data[stage_name] = {}
        # مرتب‌سازی راند‌ها بر اساس شماره (مثل round 1-8, 1-4, ...)
        rounds = sorted(stage_data.keys(), key=lambda x: int(x.split('-')[1]) if '-' in x else 0, reverse=True)
        
        for round_name in rounds:
            current_matches = stage_data[round_name]
            next_round_matches = []
            if round_name != rounds[-1]:  # اگر راند آخر نیست
                next_round_idx = rounds.index(round_name) + 1
                next_round_matches = flatten_matches(stage_data[rounds[next_round_idx]])
            
            # جمع‌آوری نام و کشور بازیکنان در راند بعدی
            next_round_players = {(player['name'], player['country']) for player in next_round_matches}
            
            new_matches = []
            for match in current_matches:
                if isinstance(match, list):
                    players = match
                else:
                    players = [match]
                
                # شناسایی برنده
                winner = None
                for player in players:
                    if (player['name'], player['country']) in next_round_players:
                        winner = player['name']
                        break
                
                # ایجاد ساختار جدید برای مسابقه
                new_match = [
                    {'country': player['country'], 'name': player['name']}
                    for player in players
                ]
                if winner:
                    new_match.append({'winner': winner})
                
                new_matches.append(new_match)
            
            # برای راند آخر، حذف تکرارهای تک‌نفره
            if round_name == rounds[-1]:
                filtered_matches = []
                seen_players = set()
                for match in new_matches:
                    # فقط مسابقاتی که بیش از یک بازیکن دارند یا اولین حضور بازیکن هستند
                    player_names = tuple(player['name'] for player in match if 'name' in player)
                    if len(player_names) > 1 or player_names not in seen_players:
                        filtered_matches.append(match)
                        seen_players.add(player_names)
                new_matches = filtered_matches
            
            # اگر راند آخر است و فقط یک مسابقه با دو بازیکن وجود دارد
            if round_name == rounds[-1] and len(new_matches) == 1 and len(new_matches[0]) > 2:
                players = new_matches[0][:-1]  # حذف فیلد winner
                # فرض می‌کنیم بازیکن دوم برنده است (یا می‌توانید منطق دیگری اعمال کنید)
                winner = players[-1]['name']
                new_matches = [[*players, {'winner': winner}]]
            
            new_data[stage_name][round_name] = new_matches
    
    return new_data
# qq = mark_winners(fin)
# qq = restructure_data(fin)
# with open(f'{amir2.text}.json', 'w') as json_file:
#     json.dump(qq, json_file, indent=4)





with open('filtered_competitions_2014_2019.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

count = len(data)
external_ids = [item['externalId'] for item in data if item['externalId'] is not None]
for url_sit in external_ids :
    driver.get(f'https://judotv.com/competitions/{url_sit}/draw')
    current_url = driver.current_url
    count -=1
    print(count)
    print(current_url) 
    if "Apologies for the error on our website" in driver.page_source:
        print(f'EROORRR  ---> {current_url}')   
        with open('Apologies-error.txt', 'a', encoding='utf-8') as log_file:
                log_file.write(f"{current_url}\n") 
    else :
        try :            
            arash1 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/main/div[3]/div[2]/div[1]/div/div')
            arash2 = arash1.find_elements('xpath','./nav')
            for amir0 in range(len(arash2)):
                mobin1 = driver.find_element(By.XPATH ,f'/html/body/div[1]/div/div[2]/div/main/div[3]/div[2]/div[1]/div/div/nav[{amir0+1}]/div')
                mobin2 = mobin1.find_elements('xpath','./div')
                if len(arash2) == 2:
                    mehdi=2
                else:
                    mehdi=1
                if amir0 +1 == 2:
                    Woman = True
                else : 
                    Woman = False
                for amir1 in range(mehdi,len(mobin2)+1):
                    amir2 = driver.find_element(By.XPATH,f'/html/body/div[1]/div/div[2]/div/main/div[3]/div[2]/div[1]/div/div/nav[{amir0+1}]/div/div[{amir1}]')
                    amir2.click()
                    # print(amir2.text)
                    stages = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/main/div[3]/div[2]/div[2]')
                    child_divs_stages = stages.find_elements("xpath", "./div")
                    
                    
                    for stage in range(1, len(child_divs_stages)):
                        z = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[2]/div/main/div[3]/div[2]/div[2]/div[{stage}]/div/div/div/div/div[1]/h3/div[1]')
                        # print(z.text)
                        
                    
                        if z.text.replace('\n', ' ') not in fin:
                            fin[z.text.replace('\n', ' ')] = {}
                        
                        a = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[2]/div/main/div[3]/div[2]/div[2]/div[{stage}]/div/div/div/div/div[2]')
                        b = a.find_elements('xpath', './div')
                        
                        # پردازش هر راند (round)
                        for step in b:
                            steps = step.find_elements('xpath', './div')
                            rr = len(steps)
                            # print(f'round 1-{rr}')
                            rounddd = f'round 1-{rr}'
                            
                    
                            if rounddd not in fin[z.text.replace('\n', ' ')]:
                                fin[z.text.replace('\n', ' ')][rounddd] = []
                            
                    
                            for match in steps:
                                aa = []
                                aa.append(match.text)
                                process_data(aa, z, rounddd)
                        
                        # print('----')
                    folder_path = f"/home/mobin/Desktop/mr.abdollahi/test14-19/{url_sit}"
                    os.makedirs(folder_path, exist_ok=True) 
                    
                    qq = restructure_data(fin)
                    if Woman :
                        no = 'F'
                    else :
                        no = 'M'
                    file_path = os.path.join(folder_path, f"{no}-{amir2.text}.json")  # مسیر درست فایل
                    
                    with open(file_path, 'w') as json_file:
                        json.dump(qq, json_file, indent=4)
                        fin = {}

        except:
            print(f'cant use this {current_url}')
            with open('World-log.txt', 'a', encoding='utf-8') as log_file:
                log_file.write(f"{current_url}\n")