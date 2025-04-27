from selenium import webdriver
import pickle
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys





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
        pass

try:
    
    driver.get("https://judotv.com/")

    load_cookies()
    driver.refresh()
    
    try :
        login_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/header/div[2]/div[1]/div[2]/button")
        login_button.click()
        sleep(2)
        
        input('-')
        username = driver.find_element(By.NAME, "Username")
        password = driver.find_element(By.NAME, "Password")
        input('--')
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
    
    judo_button = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div/aside/nav/a[4]')
    judo_button.click()
    sleep(2)
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
        # فرض می‌کنیم لینک‌ها به شکل https://.../judoka/12345 هستن
        if href:
            player_id = href.split("/judoka/")[-1]
            if player_id.isdigit():
                player_ids.append(player_id)
    print(player_ids)
    
    
    for p_id in player_id :
        driver.get(f'https://judotv.com/judoka/{p_id}')
        sleep(2)
        try:
            while True :
                judo_button = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div/main/div[2]/div[1]/div/div[5]/button')
                judo_button.click()
                sleep(2)
        except :
            pass
        links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/competitions/'][href*='/contests/']")
        hrefs = [link.get_attribute("href") for link in links]
        print (len(hrefs))

        

    
    
except:
    print('Hello')    

    
    
    
    
    
    
# /html/body/div[1]/div/div[2]/div/header/div[2]/div[1]/div[2]/button   Button
# //*[@id="email"] Email
# //*[@id="password"] password
# /html/body/div/div[1]/div[1]/form/button
# /html/body/div[1]/div/div[2]/div/aside/nav/a[4] Judoko Button
# /html/body/div[1]/div/div[2]/div/main/div[2]/div[1]/div/div[5]/button Load more
# /html/body/div[1]/div/div[2]/div/main/div[2]/div[1]/div/div[4]/a[1]/div/div[4]/div[1]/div player name
# /html/body/div[1]/div/div[2]/div/main/div[2]/div[2]/div/div[2]/div[2]/button Load more
# /html/body/div[1]/div/div[2]/div/main/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/div[2]/a/div Replay
# /html/body/div[1]/div/div[2]/div/main/div[2]/div/div[1]/div/div[1]/div[2] test







