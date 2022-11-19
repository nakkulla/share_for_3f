import os
import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
import subprocess
from selenium.webdriver.common.by import By
# import pandas as pd
import time, datetime
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

    def check_id(self, id):
        try:
            self.driver.find_element(By.ID,id)
        except NoSuchElementException:
            return False
        return True

    def liivm_login(self):

        self.wait_by_id('loginUserId').send_keys(tools.fjson("liivm", "id"))
        time.sleep(self.sterm)
        self.wait_by_id('loginUserIdPw').send_keys(tools.fjson("liivm", "passwd"))
        time.sleep(self.sterm)
        self.wait_by_id('btnIdLogin').click()

    def liivm_checker(self):

        self.driver.get('https://www.liivm.com/mypage/bill/bill/billPayment')
        time.sleep(self.sterm)
        if self.check_id('loginUserId'):
            self.liivm_login()
            time.sleep(self.lterm)
            print('login finished')

        totalbill = self.wait_by_id('totBillAmt').text
        totalbill = int(totalbill.replace("원","").replace(",",""))

        if totalbill != 0:

            print(totalbill)
            return totalbill

        elif totalbill == 0 :

            print("zero!")
            return False

    def liivm_main(self):
        result = self.liivm_checker()
        if result:

            self.bot.sendmessage(f"start liivm for {result} 원")
            
            try :
                
                self.wait_by_xpath('//*[@id="content"]/div[6]/div[2]/a').click()
                time.sleep(self.lterm)
                self.wait_by_id('selftotBillAmt').send_keys("5999")
                time.sleep(self.lterm)
                self.wait_by_xpath('//*[@id="paymentSelfLayer"]/div/div[3]/div/button[2]').click()
                time.sleep(self.lterm)
                self.wait_by_xpath('//*[@id="pym01Layer"]/div/div[2]/button[2]').click()
                time.sleep(self.lterm)
                self.wait_by_id('select-pay-card').click()
                time.sleep(self.lterm)
                self.wait_by_id('cardChangeBtn').click()
                time.sleep(self.lterm)

                self.wait_by_xpath('//*[@id="layerCardReg"]/div/div[2]/div/div[3]/ul/li[2]/button').click()
                print('card entered')
                time.sleep(self.sterm)
                self.driver.save_screenshot("/home/coder/project/phone/Data/log/liivm_finish0.png")
                self.wait_by_id('btnConfirm').click()
                time.sleep(self.lterm)
                self.driver.save_screenshot("/home/coder/project/phone/Data/log/liivm_finish1.png")
                self.wait_by_xpath('//*[@id="paymentLayer"]/div/div[3]/div/button[2]').click()
                time.sleep(self.lterm)
                self.wait_by_xpath('//*[@id="pym02Layer"]/div/div[2]/button[2]').click()
                time.sleep(self.lterm)
                print("finish purchase")
                self.driver.save_screenshot("/home/coder/project/phone/Data/log/liivm_finished.png")
                self.bot.sendmessage(f"liivm : {time.strftime('%c', time.localtime())} --- everything finished!")
                self.bot.sendphoto("/home/coder/project/phone/Data/log/liivm_finished.png")

            except :
                print("error!")
                self.driver.save_screenshot("/home/coder/project/phone/Data/log/liivm_error.png")
                self.bot.sendmessage(f"liivm : {time.strftime('%c', time.localtime())} --- error occured!")
                self.bot.sendphoto("/home/coder/project/phone/Data/log/liivm_error.png")

        else :

            self.bot.sendmessage(f"liivm : {time.strftime('%c', time.localtime())} --- billing is not ready.")
            self.driver.quit()


def job():
    themore().liivm_main()

def run():
    job()

schedule.every().day.at("12:35").do(run)

while True:
    schedule.run_pending()
    time.sleep(5)

