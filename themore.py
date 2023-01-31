from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, UnexpectedAlertPresentException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
sys.path.append("/home/coder/project/.Resource")
import tools
from amazoncaptcha import AmazonCaptcha

class get_currency_error(Exception):
    pass

class themore:

    def __init__(self):
        print("themore start")
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
        self.bot = tools.mybot(token = tools.fjson('ilsun','telegram','token'), id = tools.fjson('ilsun','telegram','id'))

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
            self.qvalue = self.wait_by_xpath('//*[@id="qoorate_USD"]/td[1]').text
            print ("Got Qoovalue!")
            print (f"Qoo value : {self.qvalue}")
            self.driver.save_screenshot("/home/coder/project/amazon/Data/log/currency.png")
            
        except :
            print("get_currency : error!")
            raise get_currency_error()
