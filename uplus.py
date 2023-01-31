import time
import sys
sys.path.append("/home/coder/project/merged/Program")
sys.path.append("/home/coder/project/.Resource")
from themore import themore, tools, Keys
import schedule


class login_err(Exception):
    pass
class charger_err(Exception):
    pass
class main_err(Exception):
    pass
class uplus_err(Exception):
    pass

class uplus(themore):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.id = tools.fjson(username, 'uplus', 'id')
        self.passwd = tools.fjson(username, 'uplus', 'passwd')
        self.card_n = tools.fjson(username, 'card', 'number')
        self.card_pwd = tools.fjson(username, 'card', 'passwd')
        self.card_bday = tools.fjson(username, 'card', 'birthday')
        self.card_name = tools.fjson(username, 'card', 'name')
        self.card_valid = tools.fjson(username, 'card', 'valid')
        self.card_gender = tools.fjson(username, 'card', 'gender')
        self.log = '/home/coder/project/phone/Data/log/uplus'
        tools.folder_maker(self.log)

    def login(self):
        try:
            self.wait_by_id('id').send_keys(self.id)
            time.sleep(self.sterm)
            self.wait_by_id('password').send_keys(self.passwd+Keys.ENTER)
            time.sleep(self.sterm)
        except :
            raise login_err()
        else:
            self.driver.get("https://www.uplusumobile.com/bill/pay/info")

    def charger(self, charge_rate):
        try:
            
            self.wait_by_xpath('//*[@id="wrap"]/main/div/section/div[2]/div[2]/div[2]/div[1]/ul/li[2]').click()
            time.sleep(self.sterm)
            self.wait_by_id('payAmountPart').send_keys(str(charge_rate))
            time.sleep(self.sterm)
            self.wait_by_xpath('//*[@id="wrap"]/main/div/section/div[2]/div[2]/div[3]/button').click()
            time.sleep(self.sterm)
            self.wait_by_xpath('//*[@id="test-layer01"]/div/div[2]/div/a[2]').click()
            time.sleep(self.sterm)
            self.wait_by_xpath('//*[@id="wrap"]/main/div/section/div[2]/div[2]/fieldset/div[1]/ul/li[1]/label').click()
            
            time.sleep(self.sterm)
            self.wait_by_xpath('/html/body/div[1]/main/div/section/div[2]/div[2]/fieldset/div[4]/div/input').send_keys(self.card_bday)
            time.sleep(self.sterm)
            if self.card_gender == 'male':
                self.wait_by_xpath('//*[@id="wrap"]/main/div/section/div[2]/div[2]/fieldset/div[6]/ul/li[2]/label').click()
            elif self.card_gender =='female':
                self.wait_by_xpath('//*[@id="wrap"]/main/div/section/div[2]/div[2]/fieldset/div[6]/ul/li[1]/label').click()
            time.sleep(self.sterm)
            self.wait_by_xpath('//*[@id="wrap"]/main/div/section/div[2]/div[2]/div[2]/button').click()
            time.sleep(self.sterm)
            self.wait_by_id("cardNum").send_keys(self.card_n)
            time.sleep(self.sterm)
            self.wait_by_id("periodMonth").send_keys(self.card_valid[:2])
            time.sleep(self.sterm)
            self.wait_by_id("periodYear").send_keys(self.card_valid[2:])
            time.sleep(self.sterm)
            self.wait_by_xpath('//*[@id="billCreditPopup"]/div[3]/div/button').click()
            time.sleep(self.sterm)

            # try:
            #     self.wait_by_xpath('//*[@id="wrap"]/main/div/section/div[2]/div[2]/div[2]/button').click()
            # except:
            #     print("button wrong")
            #     self.wait_by_xpath('//*[@id="wrap"]/main/div/section/div[2]/div[2]/div[3]/button').click()
            # time.sleep(self.sterm)
            # self.wait_by_id("cardBirthDay").send_keys(self.card_bday)
            # time.sleep(self.sterm)
            # if self.card_gender == 'male':
            #     self.wait_by_xpath('//*[@id="wrap"]/main/div/section/div[2]/div[2]/fieldset/div[5]/ul/li[2]/label').click()
            # elif self.card_gender =='female':
            #     self.wait_by_xpath('//*[@id="wrap"]/main/div/section/div[2]/div[2]/fieldset/div[5]/ul/li[1]/label').click()
            # else:
            #     print("error")
            # time.sleep(self.sterm)
            # self.wait_by_xpath('//*[@id="wrap"]/main/div/section/div[2]/div[2]/div[2]/button').click()
            # time.sleep(self.sterm)
            # self.wait_by_id("payAmount").send_keys("5999")
            # time.sleep(self.sterm)
            # self.wait_by_id("cardNum").send_keys(self.card_n)
            # time.sleep(self.sterm)
            # self.wait_by_id("periodMonth").send_keys(self.card_valid[:2])
            # time.sleep(self.sterm)
            # self.wait_by_id("periodYear").send_keys(self.card_valid[2:])
            # time.sleep(self.sterm)
            # self.wait_by_xpath('//*[@id="billCreditPopup"]/div[3]/div/button').click()
            # time.sleep(self.sterm)
            print('finish')
            return self.wait_by_xpath('//*[@id="test-layer01"]/div/div[1]/strong').text
        except Exception as inst:
            print(inst)
            raise charger_err()



    def main(self):
        try:
            for _ in range(3):
                try:
                    self.driver.get("https://www.uplusumobile.com/bill/pay/info")
                    self.login()
                    time.sleep(self.sterm)
                    total_amount = int(self.wait_by_xpath('//*[@id="wrap"]/main/div/section/div[2]/div[2]/div[1]/div/div/a/strong/span').text.replace(',',''))

                    if total_amount >= 5999:
                        print("total amount is over 5999")
                        result = self.charger(5999)
                        print(result)
                        if result == '요금납부를 완료하였습니다.':
                            self.wait_by_xpath('//*[@id="test-layer01"]/div/div[2]/div/a').click()
                            time.sleep(self.sterm)
                        else:
                            raise main_err()
                    elif total_amount == 0:
                        print("billing is not ready")
                        self.bot.sendmessage(f"skylife : {time.strftime('%c', time.localtime())} --- skylife billing is not ready!")
                    else :
                        self.bot.sendmessage(f"skylife : {time.strftime('%c', time.localtime())} --- skylife billing is not over 5999!")
                        result = self.charger(total_amount)
                        print(result)
                        if result == '요금납부를 완료하였습니다.':
                            self.wait_by_xpath('//*[@id="test-layer01"]/div/div[2]/div/a').click()
                            time.sleep(self.sterm)
                        else:
                            raise main_err()

                except login_err:
                    print("login error!!!")
                    self.driver.save_screenshot(f"{self.log}/login_err_{self.username}.png")
                    self.bot.sendmessage(f"uplus : {time.strftime('%c', time.localtime())} --- login_err occured!")
                    self.bot.sendphoto(f"{self.log}/login_err_{self.username}.png")
                except charger_err:
                    print("charger_err error!!!")
                    self.driver.save_screenshot(f"{self.log}/charger_err_{self.username}.png")
                    self.bot.sendmessage(f"uplus : {time.strftime('%c', time.localtime())} --- charger_err occured!")
                    self.bot.sendphoto(f"{self.log}/charger_err_{self.username}.png")
                except main_err:
                    print("main_err error!!!")
                    self.driver.save_screenshot(f"{self.log}/main_err_{self.username}.png")
                    self.bot.sendmessage(f"uplus : {time.strftime('%c', time.localtime())} --- main_err occured!")
                    self.bot.sendphoto(f"{self.log}/main_err_{self.username}.png")
                
                else:
                    self.driver.save_screenshot(f"{self.log}/finish_{self.username}.png")
                    print("everything finished!")
                    print(time.strftime('%c', time.localtime()))
                    self.bot.sendmessage(f"uplus : {time.strftime('%c', time.localtime())} --- {self.username} success!")
                    self.bot.sendphoto(f"{self.log}/finish_{self.username}.png")
                    break
                
                finally:
                    self.driver.delete_all_cookies()

        except:
            raise uplus_err()