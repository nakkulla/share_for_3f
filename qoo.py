import time
import sys
sys.path.append("/home/coder/project/merged/Program")
sys.path.append("/home/coder/project/.Resource")
from themore import themore, By, Keys, TimeoutException, WebDriverWait, EC, tools, AmazonCaptcha
import pickle
import schedule

class reload_error(Exception):
    pass
class login_err(Exception):
    pass
class qoo_err(Exception):
    pass

class qoo(themore):

    def __init__(self, username):
        super().__init__()
        self.cvc = tools.fjson(username,"card", "cvc")
        self.name = tools.fjson(username,"card", "name")
        self.pickle = tools.fjson(username,"qoo", "pickle")

    def handle_alert(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")

    def reload(self):
        try : 
            print(f"charging : {self.qvalue}")
            self.driver.find_element(By.ID,'order_cnt').send_keys(Keys.BACKSPACE+Keys.BACKSPACE+self.qvalue)
            self.wait_by_id('a_subOptionAddDirect').click()
            self.wait_by_xpath('//*[@id="CommonShipLangCurrencyBtn"]').click()
            self.wait_by_xpath('//*[@id="CommonShipLangCurrencyBtn"]').click()
            self.wait_by_xpath('//*[@id="CurrencySelector"]').click()
            self.wait_by_xpath('//*[@id="layer_currency"]/li[1]/a').click()
            self.wait_by_xpath('//*[@id="ShipToLangCurrencySelector"]/a').click()
            self.wait_by_id('chkAgree1').click()
            self.wait_by_id('chkAgree3').click()
            self.wait_by_id('goOrder').click()
            print("okay")
            self.handle_alert()
            time.sleep(3)
            self.driver.switch_to.frame("iframeCardLayer")
            time.sleep(self.sterm)
            print("okay")
            self.wait_by_id('card_cvc_no').send_keys(self.cvc)
            time.sleep(self.sterm)
            print(self.driver.title)
            self.wait_by_id('go_Payment').click()
            time.sleep(self.lterm)
            print(self.driver.title)

        except Exception as inst:
            print("qoo error : reload")
            print(inst)
            self.driver.save_screenshot("/home/coder/project/qoo/Data/log/qoo_error_reload.png")
            self.bot.sendmessage(f"qoo : {time.strftime('%c', time.localtime())} --- reload error!")
            self.bot.sendphoto("/home/coder/project/qoo/Data/log/qoo_error_reload.png")
            raise reload_error()

        else:
            return True
    
    def login(self):
        try:
            self.driver.get('https://www.qoo10.com')
            self.driver.delete_all_cookies()
            cookies = pickle.load(open(self.pickle, "rb"))

            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.get('https://www.qoo10.com/item/4-3-Q-COIN-TOP-UP-VOUCHER/705045258')
            if self.wait_by_xpath('//*[@id="ul_pc_header_setting_info"]/li[1]/div/a[2]').text != self.name:
                raise login_err()

        except login_err:
            print("login error!")
        else:
            print("login finished!")

    def main(self):
        try:
            for _ in range(3):
                try:
                    self.get_currency()
                    self.login()
                    self.driver.get('https://www.qoo10.com/item/4-3-Q-COIN-TOP-UP-VOUCHER/705045258')
                    time.sleep(self.sterm)
                    self.reload()
                    time.sleep(self.sterm)


                except Exception as inst:
                    print(inst)
                    time.sleep(self.sterm)

                else:
                    self.driver.save_screenshot("/home/coder/project/qoo/Data/log/qoo_finished.png")
                    self.bot.sendmessage(f"qoo : {time.strftime('%c', time.localtime())} --- success!")
                    self.bot.sendphoto("/home/coder/project/qoo/Data/log/qoo_finished.png")
                    time.sleep(self.sterm)
                    break
                
                finally:
                    self.driver.delete_all_cookies()
        except:
            raise qoo_err()
            


qoo('ilsun').main()
