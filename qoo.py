import os
import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, UnexpectedAlertPresentException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import subprocess
from selenium.webdriver.common.by import By
# import pandas as pd
import time, datetime
import schedule
import pickle
import math
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
        self.wait = WebDriverWait(self.driver, 10) 
        self.sterm = 3
        self.lterm = 7
        self.bot = tools.mybot(token = tools.fjson('telegram','token'), id = tools.fjson('telegram','id'))

    def wait_by_id(self, id):
        return self.wait.until(EC.visibility_of_element_located((By.ID, id)))

    def wait_by_xpath(self, xpath):
        wait = WebDriverWait(self.driver, 10)
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def get_currency(self):

        try :
            self.driver.get('https://themorehelp.com/')
            self.value = self.driver.find_element(By.ID,"currency_amount").get_attribute("value")
            print ("Got Currency!")
            print (f"USD {self.value}")
            self.wait_by_id('qoo10').click()
            self.driver.switch_to.active_element
            self.qvalue = self.wait_by_xpath('//*[@id="qoorate_USD"]/td[1]').text
            print ("Got Qoovalue!")
            print (f"Qoo value : {self.qvalue}")
            self.driver.save_screenshot("/home/coder/project/qoo/Data/log/currency.png")
            return True
        
        except :
            print("get_currency : error!")
            return False


    def qoo_reload(self):

        try : 
            self.driver.find_element(By.ID,'order_cnt').send_keys(Keys.BACKSPACE+Keys.BACKSPACE+self.qvalue)
            self.wait_by_id('a_subOptionAddDirect').click()
            self.wait_by_xpath('//*[@id="CommonShipLangCurrencyBtn"]').click()
            self.wait_by_xpath('//*[@id="CommonShipLangCurrencyBtn"]').click()
            self.wait_by_xpath('//*[@id="CurrencySelector"]').click()
            self.wait_by_xpath('//*[@id="layer_currency"]/li[1]/a').click()
            self.wait_by_xpath('//*[@id="ShipToLangCurrencySelector"]/a').click()
            self.wait_by_id('goOrder').click()

            try:
                WebDriverWait(self.driver, 3).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                alert.accept()
                print("alert accepted")

            except TimeoutException:
                print("no alert")

            self.driver.save_screenshot("/home/coder/project/qoo/Data/log/test_qoo0.png")
            self.driver.switch_to.frame("iframeCardLayer")
            time.sleep(2)
            print("okay")
            self.wait_by_id('card_cvc_no').send_keys(tools.fjson("card", "cvc"))
            time.sleep(2)
            self.driver.save_screenshot("/home/coder/project/qoo/Data/log/test_qoo2.png")
            print(self.driver.title)
            self.wait_by_id('go_Payment').click()
            time.sleep(10)
            self.driver.save_screenshot("/home/coder/project/qoo/Data/log/test_qoo3.png")
            print(self.driver.title)

            return True
        
        except Exception as inst:
            print("qoo error : reload")
            print(inst)
            self.driver.save_screenshot("/home/coder/project/qoo/Data/log/qoo_error_reload.png")
            self.bot.sendmessage(f"qoo : {time.strftime('%c', time.localtime())} --- reload error!")
            self.bot.sendphoto("/home/coder/project/qoo/Data/log/qoo_error_reload.png")

            return False

    def qoo_main(self):

        if self.get_currency() :
            print("link to qoo10")
            self.driver.get('https://www.qoo10.com')
            self.driver.delete_all_cookies()
            cookies = pickle.load(open("/home/coder/project/qoo/Data/cookies/cookies.pkl", "rb"))

            for cookie in cookies:
                self.driver.add_cookie(cookie)

            self.driver.get('https://www.qoo10.com/item/4-3-Q-COIN-TOP-UP-VOUCHER/705045258')
            print("login finished!")

            if self.qoo_reload():
                print("qoo reload finished")
                self.driver.save_screenshot("/home/coder/project/qoo/Data/log/qoo_finished.png")
                self.bot.sendmessage(f"qoo : {time.strftime('%c', time.localtime())} --- everythin finished!")
                self.bot.sendphoto("/home/coder/project/qoo/Data/log/qoo_finished.png")
                time.sleep(self.sterm)
                self.driver.quit()

            else :
                # print("qoo error!")
                # self.driver.save_screenshot("/home/coder/project/qoo/Data/log/qoo_error.png")
                # self.bot.sendmessage(f"qoo : {time.strftime('%c', time.localtime())} --- error!")
                # self.bot.sendphoto("/home/coder/project/qoo/Data/log/qoo_error.png")
                time.sleep(self.sterm)
                self.driver.quit()

        else :
            print("get_currency : error!")


def job():
    themore().qoo_main()

def run():
    job()

schedule.every().day.at("12:50").do(run)

while True:
    schedule.run_pending()
    time.sleep(1)
