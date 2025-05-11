from selenium import webdriver
import pickle
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
import os
import copy
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup




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




def determine_judo_winner(html_content):
    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract judoka names and countries
    judoka_elements = soup.find_all('div',
                                    class_='text-xs font-medium leading-4 @md:text-base @md:leading-5 @2xl:text-lg @2xl:leading-6')
    judoka1 = judoka_elements[0].find('a').text.strip().replace('\n', ' ')
    judoka2 = judoka_elements[1].find('a').text.strip().replace('\n', ' ')

    country_elements = soup.find_all('div',
                                     class_='text-neutral-100 w-full text-center text-xs font-bold leading-4 tracking-tight')
    country1 = country_elements[0].text.strip()
    country2 = country_elements[1].text.strip()

    # Initialize scores
    scores = {
        'judoka1': {'name': f"{judoka1} ({country1})", 'ippon': 0, 'waza_ari': 0, 'yuko': 0, 'shido': 0},
        'judoka2': {'name': f"{judoka2} ({country2})", 'ippon': 0, 'waza_ari': 0, 'yuko': 0, 'shido': 0}
    }

    # Extract scores for both judokas
    score_sections = soup.find_all('div', class_='grid text-center grid-cols-4 gap-1')

    # Judoka 1 scores (left side)
    judoka1_scores = score_sections[0].find_all('div', class_=[
        '@xs:text-lg @xs:w-6 @xs:h-6 @xs:leading-6 h-4 w-4 text-xs font-bold leading-4',
        '@xs:w-6 @xs:h-6 h-4 w-4 relative'])
    scores['judoka1']['ippon'] = int(judoka1_scores[0].text.strip()) if judoka1_scores[0].text.strip() else 0
    scores['judoka1']['waza_ari'] = int(judoka1_scores[1].text.strip()) if judoka1_scores[1].text.strip() else 0
    scores['judoka1']['yuko'] = int(judoka1_scores[2].text.strip()) if judoka1_scores[2].text.strip() else 0
    scores['judoka1']['shido'] = len(judoka1_scores[3].find_all('div', class_='bg-yellow'))

    # Judoka 2 scores (right side)
    judoka2_scores = score_sections[1].find_all('div', class_=[
        '@xs:text-lg @xs:w-6 @xs:h-6 @xs:leading-6 h-4 w-4 text-xs font-bold leading-4',
        '@xs:w-6 @xs:h-6 h-4 w-4 relative'])
    scores['judoka2']['ippon'] = int(judoka2_scores[0].text.strip()) if judoka2_scores[0].text.strip() else 0
    scores['judoka2']['waza_ari'] = int(judoka2_scores[1].text.strip()) if judoka2_scores[1].text.strip() else 0
    scores['judoka2']['yuko'] = int(judoka2_scores[2].text.strip()) if judoka2_scores[2].text.strip() else 0
    scores['judoka2']['shido'] = len(judoka2_scores[3].find_all('div', class_='bg-yellow'))

    # Determine winner based on judo rules
    if scores['judoka1']['ippon'] > scores['judoka2']['ippon']:
        return f"Winner: {scores['judoka1']['name']}", scores
    elif scores['judoka2']['ippon'] > scores['judoka1']['ippon']:
        return f"Winner: {scores['judoka2']['name']}", scores

    if scores['judoka1']['waza_ari'] > scores['judoka2']['waza_ari']:
        return f"Winner: {scores['judoka1']['name']}", scores
    elif scores['judoka2']['waza_ari'] > scores['judoka1']['waza_ari']:
        return f"Winner: {scores['judoka2']['name']}", scores

    if scores['judoka1']['yuko'] > scores['judoka2']['yuko']:
        return f"Winner: {scores['judoka1']['name']}", scores
    elif scores['judoka2']['yuko'] > scores['judoka1']['yuko']:
        return f"Winner: {scores['judoka2']['name']}", scores

    # If scores are tied, fewer shidos win
    if scores['judoka1']['shido'] < scores['judoka2']['shido']:
        return f"Winner: {scores['judoka1']['name']}", scores
    elif scores['judoka2']['shido'] < scores['judoka1']['shido']:
        return f"Winner: {scores['judoka2']['name']}", scores

    return "Match is a draw or data is inconclusive", scores


# Example usage
if __name__ == "__main__":
    # Replace with actual HTML content (e.g., from your provided HTML)
    with open("match.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    winner, scores = determine_judo_winner(html_content)
    print(winner)
    print("Scores:")
    for judoka, score in scores.items():
        print(
            f"{score['name']}: Ippon={score['ippon']}, Waza-ari={score['waza_ari']}, Yuko={score['yuko']}, Shido={score['shido']}")