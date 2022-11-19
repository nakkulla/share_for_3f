import os
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
import subprocess
from selenium.webdriver.common.by import By
# import pandas as pd
import time
import schedule
import sys
sys.path.append("/home/coder/project/.Resource")
import tools
from amazoncaptcha import AmazonCaptcha

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
        self.lterm = 10
        self.sterm = 3
        self.bot = tools.mybot(token = tools.fjson('telegram','token'), id = tools.fjson('telegram','id'))

    def wait_by_id(self, id):
        return self.wait.until(EC.visibility_of_element_located((By.ID, id)))

    def wait_by_xpath(self, xpath):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def wait_by_title(self, title):
        return self.wait.until(EC.title_contains(title))

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    def check_exists_by_id(self, id):
        try:
            self.driver.find_element(By.ID, id)
        except NoSuchElementException:
            return False
        return True

    def get_currency(self):
        try :
            self.driver.get('https://themorehelp.com/')
            self.value = self.driver.find_element(By.ID,"currency_amount").get_attribute("value")
            print ("Got Currency!")
            print (f"USD {self.value}")
            self.wait_by_id('qoo10').click()
            self.driver.switch_to.active_element
            self.qvalue = self.wait_by_xpath('//*[@id="qoorate_QUUBE"]/th').text
            print ("Got Qoovalue!")
            print (f"Qoo value : {self.qvalue}")
            self.driver.save_screenshot("/home/coder/project/amazon/Data/log/currency.png")
            return True
        
        except :
            print("get_currency : error!")
            return False

    def amazon_login(self):
        try :
            self.driver.get('https://www.amazon.com/asv/reload/')
            print("link to amazon.com!")
            time.sleep(self.sterm)    
            self.wait_by_id('nav-link-accountList').click()
            time.sleep(self.lterm)
            self.wait_by_id('ap_email')

        except :
            print("login error!")
            time.sleep(self.sterm)
            self.driver.save_screenshot("/home/coder/project/amazon/Data/log/captcha.png")
            captcha = AmazonCaptcha.fromdriver(self.driver)
            solution = captcha.solve()
            self.driver.find_element(By.ID,'captchacharacters').send_keys(solution)
            self.driver.find_element(By.ID,'captchacharacters').submit()
            time.sleep(self.sterm)
            self.driver.save_screenshot("/home/coder/project/amazon/Data/log/captcha_result.png")
            print("captcha soloved!")
            print(self.driver.title)
            self.wait_by_id('nav-link-accountList').click()
            time.sleep(self.lterm)
            print(self.driver.title)

        finally:
            self.driver.get('https://www.amazon.com/asv/reload/')
            time.sleep(self.sterm)
            self.wait_by_id('nav-link-accountList').click()
            self.wait_by_id('ap_email').send_keys(tools.fjson("amazon", "id"))
            self.wait_by_id('continue').click()
            self.wait_by_id('ap_password').send_keys(tools.fjson("amazon", "passwd"))
            self.wait_by_id('signInSubmit').click()
            time.sleep(self.lterm)
            print("login finished")

    def amazon_reload(self):
        try :
            self.driver.get('https://www.amazon.com/asv/reload/')
            self.wait_by_id('gcui-asv-reload-form-custom-amount').send_keys(self.value)
            time.sleep(self.sterm)
            self.wait_by_id('gcui-asv-reload-buynow-button').click()
            time.sleep(self.sterm)
            self.wait_by_id('orderSummaryPrimaryActionBtn').click()
            time.sleep(self.lterm)
            if self.check_exists_by_id('a-popover-content-4'):
                self.driver.find_element(By.XPATH, '//*[@id="a-popover-2"]/div/button').click()
                time.sleep(self.lterm)
            self.wait_by_id('submitOrderButtonId').click()
            time.sleep(self.lterm)
            print(self.driver.title)
            if self.wait_by_title('Thanks You'):
                return True
            else :
                return False

        except Exception as inst:
            print("amazon error : reload")
            print(inst)
            self.driver.save_screenshot("/home/coder/project/amazon/Data/log/amazon_error_reload.png")
            self.bot.sendmessage(f"amazon : {time.strftime('%c', time.localtime())} --- reload error!")

            return False

    def amazon_main(self):

        if self.get_currency() :
            try : 
                self.amazon_login()
                if self.amazon_reload():
                    self.driver.save_screenshot("/home/coder/project/amazon/Data/log/amazon_finished.png")
                    self.bot.sendmessage(f"amazon : {time.strftime('%c', time.localtime())} --- everything finished!")
                    self.bot.sendphoto("/home/coder/project/amazon/Data/log/amazon_finished.png")
                    self.driver.quit()
                    print ("Finished!")
                    print(time.strftime('%c', time.localtime()))

                else :
                    self.driver.save_screenshot("/home/coder/project/amazon/Data/log/amazon_error.png")
                    self.bot.sendmessage(f"amazon : {time.strftime('%c', time.localtime())} --- error!")
                    self.bot.sendphoto("/home/coder/project/amazon/Data/log/amazon_error.png")
                    self.driver.quit()
                    print ("error!")
                    print(time.strftime('%c', time.localtime()))

            except Exception as inst:
                print("qoo error : reload")
                print(inst)
                self.driver.save_screenshot("/home/coder/project/amazon/Data/log/amazon_error2.png")
                self.bot.sendmessage(f"amazon : {time.strftime('%c', time.localtime())} --- error2!")
                self.bot.sendphoto("/home/coder/project/amazon/Data/log/amazon_error2.png")

        else :
            print("get_currency : error!")


def job():
    themore().amazon_main()

def run():
    job()

schedule.every().day.at("12:40").do(run)

while True:
    schedule.run_pending()
    time.sleep(1)
