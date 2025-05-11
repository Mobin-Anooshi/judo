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

