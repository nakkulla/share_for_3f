import time
import sys
sys.path.append("/home/coder/project/merged/Program")
sys.path.append("/home/coder/project/.Resource")
from themore import themore, By, tools, AmazonCaptcha
import schedule
import pickle

class solve_captcha_error(Exception):
    pass

class reload_error(Exception):
    pass
class amazon_err(Exception):
    pass

class amazon(themore):
    def __init__(self,username):
        super().__init__()
        self.username = username
        self.id = tools.fjson(username, 'amazon', 'id')
        self.passwd = tools.fjson(username, 'amazon', 'passwd')

    def solve_captcha(self):
        try:
            captcha = AmazonCaptcha.fromdriver(self.driver)
            solution = captcha.solve()
            self.driver.find_element(By.ID,'captchacharacters').send_keys(solution)
            self.driver.find_element(By.ID,'captchacharacters').submit()
            time.sleep(self.sterm)
            print("captcha soloved!")
            print(self.driver.title)

        except:
            raise solve_captcha_error()

    def login(self):
        for _ in range(2):
            try :
                self.driver.get("https://www.amazon.com")
                self.driver.delete_all_cookies()
                time.sleep(self.sterm)
                cookies = pickle.load(open("/home/coder/project/amazon/Data/cookies/amazon_cookies.pkl", "rb"))
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                time.sleep(self.sterm)
                self.driver.get('https://www.amazon.com')
                # self.driver.get('https://www.amazon.com/asv/reload/')
                # time.sleep(self.sterm)    
                # self.wait_by_id('nav-link-accountList').click()
                # time.sleep(self.lterm)
                # self.wait_by_id('ap_email').send_keys(self.id)
                # self.wait_by_id('continue').click()
                # time.sleep(self.sterm)    
                # self.wait_by_id('ap_password').send_keys(self.passwd)
                # time.sleep(self.sterm)    
                # self.wait_by_id('signInSubmit').click()
                # time.sleep(self.lterm)
                # print("login finished")
                break
            except :
                print("captcha popped!")
                time.sleep(self.sterm)
                self.solve_captcha()
                continue

    def reload(self):
        try :
            print("reload start!")
            self.driver.get('https://www.amazon.com/asv/reload/')
            time.sleep(self.sterm)
            self.wait_by_id('gcui-asv-reload-form-custom-amount').send_keys(self.value)
            time.sleep(self.sterm)
            self.wait_by_id('gcui-asv-reload-buynow-button').click()
            time.sleep(self.sterm)
            self.driver.save_screenshot("/home/coder/project/amazon/Data/log/1.png")
            if self.check_exists_by_id('submitOrderButtonId'):
                self.wait_by_id('submitOrderButtonId').click()
            else:
                self.wait_by_id('orderSummaryPrimaryActionBtn').click()
                time.sleep(self.lterm)
                if self.check_exists_by_id('a-popover-content-4'):
                    self.driver.find_element(By.XPATH, '//*[@id="a-popover-2"]/div/button').click()
                    time.sleep(self.lterm)
                self.wait_by_id('submitOrderButtonId').click()
                time.sleep(self.lterm)
            print(self.driver.title)
            self.wait_by_title('Thanks You')

        except Exception as inst:
            print("amazon error : reload")
            print("submit password again")
            self.wait_by_id('ap_password').send_keys(self.passwd)
            self.wait_by_id('signInSubmit').click()
            time.sleep(self.lterm)
            print("login finished")
            print(inst)
            self.driver.save_screenshot("/home/coder/project/amazon/Data/log/error_reload.png")
            self.bot.sendmessage(f"amazon : {time.strftime('%c', time.localtime())} --- reload error!")
            self.bot.sendphoto("/home/coder/project/amazon/Data/log/amazon_error.png")
            raise reload_error()

        else:
            return True

    def main(self):
        try:
            for _ in range(1):
                try:
                    self.get_currency()
                    time.sleep(self.sterm)
                    self.login()
                    time.sleep(self.sterm)
                    self.reload()
                    time.sleep(self.sterm)

                except Exception as inst:
                    print(inst)
                    time.sleep(self.sterm)
                    self.driver.save_screenshot("/home/coder/project/amazon/Data/log/amazon_error.png")
                    self.bot.sendmessage(f"amazon : {time.strftime('%c', time.localtime())} --- error!")
                    self.bot.sendphoto("/home/coder/project/amazon/Data/log/amazon_error.png")
                    print ("error!")
                    print(time.strftime('%c', time.localtime()))

                else:
                    self.driver.save_screenshot("/home/coder/project/amazon/Data/log/amazon_finished.png")
                    self.bot.sendmessage(f"amazon : {time.strftime('%c', time.localtime())} --- everything finished!")
                    self.bot.sendphoto("/home/coder/project/amazon/Data/log/amazon_finished.png")
                    break

                finally:
                    self.driver.delete_all_cookies()

        except:
            raise amazon_err()

amazon('ilsun').main()