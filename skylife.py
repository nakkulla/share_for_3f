import os
import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.chrome.options import Options
import subprocess
from selenium.webdriver.common.by import By
import time, datetime
import urllib.request
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import schedule
import sys
sys.path.append("/home/coder/project/.Resource")
import tools


class themore:

    def __init__(self):
        chrome_path='/home/coder/chromedriver'
        options = webdriver.ChromeOptions()
        options.add_argument('start-minimized')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument("window-size=1400,1000")
        self.driver = webdriver.Chrome(chrome_options=options, executable_path=chrome_path)   
        self.wait = WebDriverWait(self.driver, 20) 
        self.sterm = 3
        self.lterm = 7
        self.bot = tools.mybot(token = tools.fjson('telegram','token'), id = tools.fjson('telegram','id'))


    def wait_by_id(self, id):
        return self.wait.until(EC.visibility_of_element_located((By.ID, id)))

    def wait_by_xpath(self, xpath):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    
    def wait_by_title(self, title):
        return self.wait.until(EC.title_contains(title))

    def check_id(self, id):
        try:
            self.driver.find_element(By.ID,id)
        except NoSuchElementException:
            return False
        return True
    
    def skylife_enter_card(self):



    def skylife_login(self):

        self.driver.get("https://www.skylife.co.kr/member/login")
        self.wait_by_id("uId").send_keys(tools.fjson("skylife", "id"))
        self.wait_by_id("uPass").send_keys(tools.fjson("skylife", "passwd")+Keys.ENTER)
        time.sleep(self.lterm)
        try :
            self.wait_by_title('kt Skylife - 메인')
            return False
        
        except :
            return True

    def skylife_checker(self):

        value = self.wait_by_xpath('//*[@id="userIdDetail"]/div[1]/span/b').text.replace(',','')
        return int(value)

    def skylife_main(self):

        try:
            while self.skylife_login():
                print("login failed!")
                self.bot.sendmessage(f"skylife : {time.strftime('%c', time.localtime())} --- login failed!")

            print("login finished!")

            self.driver.get("https://www.skylife.co.kr/my/charge/pay/unpaid")
            if self.skylife_checker() > 5998:

                self.wait_by_xpath('//*[@id="userIdDetail"]/div[4]/div[2]/a/span').click()
                self.skylife_enter_card()
                time.sleep(self.sterm)
                print("card entered!")

                self.wait_by_xpath('//*[@id="payCreditCard"]/div/div[2]/div[2]/a').click()
                time.sleep(self.lterm)
                print("purchased!")

                try:

                    WebDriverWait(self.driver, 3).until(EC.alert_is_present())
                    alert = self.driver.switch_to.alert
                    alert.accept()
                    print("alert accepted")

                except TimeoutException:

                    print("no alert")
                    
                self.driver.save_screenshot("/home/coder/project/phone/Data/log/skylife_finished.png")
                time.sleep(self.sterm)
                print("everything finished!")
                self.driver.quit()
                print(time.strftime('%c', time.localtime()))
                self.bot.sendmessage(f"skylife : {time.strftime('%c', time.localtime())} --- everything finished!")
                self.bot.sendphoto("/home/coder/project/phone/Data/log/skylife_finished.png")
            
            else :

                self.driver.save_screenshot("/home/coder/project/phone/Data/log/skylife_finished.png")
                time.sleep(self.sterm)
                print("everything finished!")
                self.driver.quit()
                print(time.strftime('%c', time.localtime()))
                self.bot.sendmessage(f"skylife : {time.strftime('%c', time.localtime())} --- bill is not ready or less than 5999!")
                self.bot.sendphoto("/home/coder/project/phone/Data/log/skylife_finished.png")

        except Exception as inst:

            print("error!!!")
            print(inst)
            self.driver.save_screenshot("/home/coder/project/phone/Data/log/skylife_error.png")
            self.bot.sendmessage(f"skylife : {time.strftime('%c', time.localtime())} --- error occured!")
            self.bot.sendphoto("/home/coder/project/phone/Data/log/skylife_error.png")

def job():
    themore().skylife_main()

def run():
    job()

schedule.every().day.at("12:30").do(run)

while True:
    schedule.run_pending()
    time.sleep(1)
