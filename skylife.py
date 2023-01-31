import time
import sys
sys.path.append("/home/coder/project/merged/Program")
sys.path.append("/home/coder/project/.Resource")
from themore import themore, tools, Keys, WebDriverWait, EC, TimeoutException
import schedule

class enter_card_error(Exception):
    pass
class no_amount(Exception):
    pass
class login_err(Exception):
    pass
class skylife_err(Exception):
    pass

class skylife(themore):

    def __init__(self,username):
        super().__init__()
        self.username = username
        self.card_n = tools.fjson(username, 'card', 'number')
        self.card_pwd = tools.fjson(username, 'card', 'passwd')
        self.id = tools.fjson(username, 'skylife', 'id')
        self.passwd = tools.fjson(username, 'skylife', 'passwd')
        self.card_bday = tools.fjson(username, 'card', 'birthday')
        self.card_name = tools.fjson(username, 'card', 'name')
        self.card_valid = tools.fjson(username, 'card', 'valid')

    def enter_card(self, charge_rate):
        try:
            self.wait_by_id("cardNo-1").send_keys(self.card_n[0:4])
            self.wait_by_id("cardNo-2").send_keys(self.card_n[4:8])
            self.wait_by_id("cardNo-3").send_keys(self.card_n[8:12])
            self.wait_by_id("cardNo-4").send_keys(self.card_n[12:16])
            # 년
            self.wait_by_xpath('//*[@id="payCreditCard"]/div/div[2]/div[1]/div/table/tbody/tr[3]/td/div/span[1]/div').click()
            self.wait_by_xpath(f'//*[@id="payCreditCard"]/div/div[2]/div[1]/div/table/tbody/tr[3]/td/div/span[1]/div/div[3]/div/ul/li[text()=20{self.card_valid[2:4]}]').click()
            # 월
            self.wait_by_xpath('//*[@id="payCreditCard"]/div/div[2]/div[1]/div/table/tbody/tr[3]/td/div/span[2]/div/div[2]').click()
            self.wait_by_xpath(f'//*[@id="payCreditCard"]/div/div[2]/div[1]/div/table/tbody/tr[3]/td/div/span[2]/div/div[3]/div/ul/li[text()={self.card_valid[0:2]}]').click()
            # 생년
            self.wait_by_xpath('//*[@id="payCreditCard"]/div/div[2]/div[1]/div/table/tbody/tr[4]/td/div/span[1]/div/div[2]/span').click()
            self.wait_by_xpath(f'//*[@id="payCreditCard"]/div/div[2]/div[1]/div/table/tbody/tr[4]/td/div/span[1]/div/div[3]/div/ul/li[text()={self.card_bday[0:4]}]').click()
            # 월
            self.wait_by_xpath('//*[@id="payCreditCard"]/div/div[2]/div[1]/div/table/tbody/tr[4]/td/div/span[2]/div/div[2]/span').click()
            self.wait_by_xpath(f'//*[@id="payCreditCard"]/div/div[2]/div[1]/div/table/tbody/tr[4]/td/div/span[2]/div/div[3]/div/ul/li[text()={self.card_bday[4:6]}]').click()
            # 일
            self.wait_by_xpath('//*[@id="payCreditCard"]/div/div[2]/div[1]/div/table/tbody/tr[4]/td/div/span[3]/div/div[2]/span').click()
            self.wait_by_xpath(f'//*[@id="payCreditCard"]/div/div[2]/div[1]/div/table/tbody/tr[4]/td/div/span[3]/div/div[3]/div/ul/li[text()={self.card_bday[6:8]}]').click()

            self.wait_by_id("monthlyCharge").send_keys(charge_rate)
            self.wait_by_id("uPass").send_keys(self.card_pwd[:2])

            time.sleep(self.sterm)
            self.wait_by_xpath('//*[@id="payCreditCard"]/div/div[2]/div[2]/a/span').click()
            print("card entered!")
            time.sleep(self.sterm)

        except:
            print("error!")
            raise enter_card_error()

        else:
            print("purchased!")
            return True

    def login(self):
        try :
            self.driver.get("https://www.skylife.co.kr/member/login")
            self.wait_by_id("uId").send_keys(self.id)
            self.wait_by_id("uPass").send_keys(self.passwd+Keys.ENTER)
            time.sleep(self.lterm)
            print(self.driver.title)

            if self.driver.title == 'kt Skylife - 회원':
                self.wait_by_xpath('//*[@id="sub-contents"]/div[3]/div/div[2]/a[3]/span').click()
                time.sleep(self.sterm)
                print(self.driver.title)

            if self.driver.title != 'kt Skylife - 메인':
                raise login_err()

        except login_err:
            return False

        else:
            print("login finished!")
            return True

    def checker(self):
        value = self.wait_by_xpath('//*[@id="userIdDetail"]/div[1]/span/b').text.replace(',','')
        return int(value)

    def handle_alert(self):
        try:
            time.sleep(self.sterm)
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            print("alert accepted")

        except TimeoutException:
            print("no alert")

    def main(self):
        try:
            for _ in range(3):
                try:
                    for _ in range(5):
                        if self.login() == True:
                            break
                        else:
                            print("login failed!")
                            self.bot.sendmessage(f"skylife : {time.strftime('%c', time.localtime())} --- login failed! try again...")

                    self.driver.get("https://www.skylife.co.kr/my/charge/pay/unpaid")
                    time.sleep(self.lterm)
                    total_amount = self.checker()
                    charge_amount = 0

                    if total_amount >= 5999:
                        charge_amount = 5999
                        self.wait_by_xpath('//*[@id="userIdDetail"]/div[4]/div[2]/a/span').click()
                        print(f"charge {charge_amount} in {total_amount}")
                        time.sleep(self.sterm)
                        self.enter_card(charge_amount)
                        time.sleep(self.sterm)
                        self.handle_alert()
                        time.sleep(self.sterm)
                    elif total_amount == 0:
                        print("billing is not ready")
                        self.bot.sendmessage(f"skylife : {time.strftime('%c', time.localtime())} --- skylife billing is not ready!")
                    else :
                        self.bot.sendmessage(f"skylife : {time.strftime('%c', time.localtime())} --- skylife billing is less 5999!")
                        charge_amount = total_amount
                        self.wait_by_xpath('//*[@id="userIdDetail"]/div[4]/div[2]/a/span').click()
                        print(f"charge {charge_amount} in {total_amount}")
                        time.sleep(self.sterm)
                        self.enter_card(charge_amount)
                        time.sleep(self.sterm)
                        self.handle_alert()
                        time.sleep(self.sterm)

                except enter_card_error:
                    print("error!!!")
                    self.driver.save_screenshot(f"/home/coder/project/phone/Data/log/skylife_enter_card_error_{self.username}.png")
                    self.bot.sendmessage(f"skylife : {time.strftime('%c', time.localtime())} --- skylife_enter_card_error occured!")
                    self.bot.sendphoto(f"/home/coder/project/phone/Data/log/skylife_enter_card_error_{self.username}.png")

                except login_err:
                    print("login error!!!")
                    print(inst)
                    self.driver.save_screenshot(f"/home/coder/project/phone/Data/log/skylife_loginerr_{self.username}.png")
                    self.bot.sendmessage(f"skylife : {time.strftime('%c', time.localtime())} --- skylife_login_err_{self.username} occured!")
                    self.bot.sendphoto(f"/home/coder/project/phone/Data/log/skylife_loginerr_{self.username}.png")

                except Exception as inst:
                    print("other error!!!")
                    print(inst)
                    self.driver.save_screenshot(f"/home/coder/project/phone/Data/log/skylife_error_{self.username}.png")
                    self.bot.sendmessage(f"skylife : {time.strftime('%c', time.localtime())} --- skylife_error_{self.username} occured!")
                    self.bot.sendphoto(f"/home/coder/project/phone/Data/log/skylife_error_{self.username}.png")
                    
                else:
                    self.driver.save_screenshot(f"/home/coder/project/phone/Data/log/skylife_finished_{self.username}.png")
                    time.sleep(self.sterm)
                    print("everything finished!")
                    print(time.strftime('%c', time.localtime()))
                    self.bot.sendmessage(f"skylife : {time.strftime('%c', time.localtime())} --- {self.username} success!")
                    self.bot.sendphoto(f"/home/coder/project/phone/Data/log/skylife_finished_{self.username}.png")
                    break
                    
                finally:
                    self.driver.delete_all_cookies()

        except:
            raise skylife_err()