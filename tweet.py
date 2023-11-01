import pandas as pd
from pytz import timezone
from dateutil import parser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import traceback
import time
from fastapi import FastAPI, Query
import uvicorn
from typing import List

app = FastAPI()


class EngageX:
    def __init__(self):
        self.driver = self.Init_browser()

    def Init_browser(self):
        try:
            options = Options()
            options.add_argument('disable-infobars')
            options.add_argument("--disable-notifications")
            # options.add_argument("--headless")
            options.add_argument("--log-level=3")
            options.add_argument('--disable-logging')
            options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
            options.add_argument("window-size=1200x600")
            driver = webdriver.Chrome(options=options)

            driver.implicitly_wait(10)
            driver.get("https://www.google.com/")
            return driver
        except Exception:
            traceback.print_exc()

    def Login(self, username, password):
        time.sleep(2.5)
        self.driver.get('https://twitter.com/i/flow/login')
        time.sleep(2.5)
        username_textarea = self.driver.find_element(
            "xpath", '//input[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]')
        time.sleep(2.5)
        username_textarea.send_keys(username.encode('utf-8').decode())
        time.sleep(2.5)
        next_button = self.driver.find_element(
            "xpath", '//div[@class="css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu"]')
        time.sleep(2.5)
        next_button.click()
        time.sleep(2.5)
        password_textarea = self.driver.find_element(
            "xpath", '//input[@name="password"]')
        time.sleep(2.5)
        password_textarea.send_keys(password.encode('utf-8').decode())
        time.sleep(2.5)
        login_button = self.driver.find_element(
            "xpath", '//div[@data-testid="LoginForm_Login_Button"]')
        time.sleep(2.5)
        login_button.click()
        time.sleep(5)

    def DM(self, target_account_name, text):
        try:
            link = f"https://twitter.com/messages/compose"
            self.driver.get(link)
            time.sleep(10)
            username_area = self.driver.find_element(
                "xpath", '//input[@placeholder="Search people"]')
            time.sleep(3)
            username_area.send_keys(
                target_account_name.encode('utf-8').decode())
            time.sleep(3)
            goto_button = self.driver.find_element(
                "xpath", '//div[@data-testid="TypeaheadUser"]')
            time.sleep(3)
            goto_button.click()
            time.sleep(3)
            next_button = self.driver.find_element(
                "xpath", '//div[@data-testid="nextButton"]')
            time.sleep(3)
            next_button.click()
            time.sleep(3)
            message_textarea = self.driver.find_element(
                "xpath", '//div[@class="public-DraftStyleDefault-block public-DraftStyleDefault-ltr"]')
            time.sleep(3)
            message_textarea.send_keys(text.format(
                account_name=target_account_name))
            time.sleep(3)
            send_button = self.driver.find_element(
                "xpath", '//div[@data-testid="dmComposerSendButton"]')
            time.sleep(3)
            send_button.click()
            time.sleep(2)
            self.driver.get("https://twitter.com")
            time.sleep(3)
            print(f"DM Done to @{target_account_name} --> {text}")
        except Exception as e:
            print("This person cannot be directly messaged!")
            print(e)
            pass

    def quit(self):
        self.driver.quit()
        print("Browser session terminated successfully.")


@app.get("/send-dm")
def send_dm(username: str = Query(...), password: str = Query(...), target_account_names: List[str] = Query(...), text: str = Query(...)):
    E = EngageX()
    E.Login(username, password)
    for account_name in target_account_names:
        E.DM(account_name, text)
        time.sleep(10)
    return {"message": "Login and Direct messages sent"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
