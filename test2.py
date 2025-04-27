from selenium import webdriver
import pickle
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json



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
        print('load cookie')
    

try:
    
    driver.get("https://judotv.com/")

    load_cookies()
    driver.refresh()
    
    try :
        login_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/header/div[2]/div[1]/div[2]/button")
        login_button.click()
        sleep(2)
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
    print(1)
    
judo_button = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div/aside/nav/a[4]')
judo_button.click()
sleep(2)

input('---')
try:
    while True: 
        judo_button = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div/main/div[2]/div[1]/div/div[5]/button')
        judo_button.click()
        sleep(2)
except:
    pass


links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/judoka/']")





player_ids = []
for link in links:
    href = link.get_attribute("href")
    if href:
        player_id = href.split("/judoka/")[-1]
        if player_id.isdigit():
            player_ids.append(player_id)
print(player_ids)



for p_id in player_ids :
    driver.get(f'https://judotv.com/judoka/{p_id}')
    # driver.get(f'https://judotv.com/judoka/79453')
    sleep(2)
    player_name = driver.find_element(By.XPATH ,'/html/body/div[1]/div/div[2]/div/main/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/h1').text
    try:
        while True :
            judo_button = driver.find_element(By.XPAplayer_idTH,'/html/body/div[1]/div/div[2]/div/main/div[2]/div[1]/div/div[5]/button')
            judo_button.click()
            sleep(2)
    except :
        pass
    links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/competitions/'][href*='/contests/']")
    hrefs = [link.get_attribute("href") for link in links]
    print
    all_matches=[]
    for ur in hrefs :
        driver.get(ur)
        
        judoka_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/judoka/']")
        
        names = []
        seen_ids = set()
        
        for link in judoka_links:
            href = link.get_attribute("href")
            judoka_id = href.split("/")[-1]
        
            if judoka_id not in seen_ids:
                name = link.text.strip().replace("\n", " ")
                if name:
                    names.append(name)
                    seen_ids.add(judoka_id)
        
            if len(names) == 2:
                break 

        grid = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div/main/div[2]/div/div[2]/div[2]/div[2]')
        columns = grid.find_elements(By.XPATH, "./div")
        events = []
        i = 0
        while i < len(columns):
            col1 = columns[i].text.strip()
            col2 = columns[i+1].text.strip() if i+1 < len(columns) else ''
            col3 = columns[i+2].text.strip() if i+2 < len(columns) else ''
        
            left = col1 if col1 else None
            time = col2 if col2 else None
            right = col3 if col3 else None
        

            if not time or ":" not in time:
                time = col1 if ":" in col1 else None
                left = None
                right = col2
        
            events.append({
                "time": time,
                names[0]: left,
                names[1]: right
            })

            i += 3

            match_data = {
                "judoka_1": names[0],
                "judoka_2": names[1],
                "winner": names[1],  
                "events": events
            }
        all_matches.append(match_data)
    print(json.dumps(all_matches, indent=2, ensure_ascii=False))
    with open(f'data/{player_name}.json', "w", encoding="utf-8") as f:
        json.dump(all_matches, f, ensure_ascii=False, indent=2)
        