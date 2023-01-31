import time
import sys
sys.path.append("/home/coder/project/merged/Program")
sys.path.append("/home/coder/project/.Resource")
from themore import themore, tools
import schedule

class checker_error(Exception):
    pass
class charger_error(Exception):
    pass
class liivm_err(Exception):
    pass

class liivm(themore):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.id = tools.fjson(username, 'liivm', 'id')
        self.passwd = tools.fjson(username, 'liivm', 'passwd')
        self.card_n = tools.fjson(username, 'card', 'number')
        self.card_pwd = tools.fjson(username, 'card', 'passwd')
        self.card_bday = tools.fjson(username, 'card', 'birthday')
        self.card_name = tools.fjson(username, 'card', 'name')
        self.card_valid = tools.fjson(username, 'card', 'valid')

    def login(self):
        self.wait_by_id('loginUserId').send_keys(self.id)
        time.sleep(self.sterm)
        self.wait_by_id('loginUserIdPw').send_keys(self.passwd)
        time.sleep(self.sterm)
        self.wait_by_id('btnIdLogin').click()

    def checker(self):
        try:
            self.driver.get('https://www.liivm.com/mypage/bill/bill/billPayment')
            time.sleep(self.sterm)
            if self.check_exists_by_id('loginUserId'):
                self.login()
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
        except:
            raise checker_error()

    def charger(self, charge_rate):
        try:
            print(f"charge for {charge_rate}")
            self.wait_by_xpath('//*[@id="content"]/div[6]/div[2]/a').click()
            time.sleep(self.lterm)
            self.wait_by_id('selftotBillAmt').send_keys(charge_rate)
            time.sleep(self.lterm)
            self.wait_by_xpath('//*[@id="paymentSelfLayer"]/div/div[3]/div/button[2]').click()
            time.sleep(self.lterm)
            self.wait_by_xpath('//*[@id="pym01Layer"]/div/div[2]/button[2]').click()
            time.sleep(self.lterm)
            self.wait_by_id('select-pay-card').click()
            time.sleep(self.lterm)
            self.wait_by_id('cardChangeBtn').click()
            time.sleep(self.lterm)
            self.wait_by_id('cardNo_1').send_keys(self.card_n[0:4])
            time.sleep(self.sterm)
            self.wait_by_id('cardNo_2').send_keys(self.card_n[4:8])
            time.sleep(self.sterm)
            self.wait_by_id('cardNo_3').send_keys(self.card_n[8:12])
            time.sleep(self.sterm)
            self.wait_by_id('cardNo_4').send_keys(self.card_n[12:16])
            time.sleep(self.sterm)
            self.wait_by_id('cardEffcprd').send_keys(self.card_valid)
            time.sleep(self.sterm+1)
            self.wait_by_id("payCustNm").send_keys(self.card_name)
            time.sleep(self.sterm+1)
            self.wait_by_id('birthGender').send_keys(self.card_bday)
            time.sleep(self.sterm+1)
            self.wait_by_xpath('//*[@id="layerCardReg"]/div/div[2]/div/div[3]/ul/li[2]/button').click()
            print('card entered')
            time.sleep(self.sterm)
            self.wait_by_id('btnConfirm').click()
            time.sleep(self.lterm)
            self.wait_by_xpath('//*[@id="paymentLayer"]/div/div[3]/div/button[2]').click()
            time.sleep(self.lterm)
            self.wait_by_xpath('//*[@id="pym02Layer"]/div/div[2]/button[2]').click()
            time.sleep(self.lterm)
            print("finish purchase")
        except :
            raise charger_error()
        else :
            return True

    def main(self):
        try:
            for _ in range(3):
                try :
                    result = self.checker()

                    if result:
                        self.bot.sendmessage(f"start liivm for {result} 원")
                        charge_rate = 0

                        if result >= 5999:
                            charge_rate = "5999"
                        else:
                            charge_rate = str(result)
                        self.charger(charge_rate)
                    
                    else :
                        self.bot.sendmessage(f"liivm : {time.strftime('%c', time.localtime())} --- {self.username} --- billing is not over 5999")

                except checker_error:
                    print("liivm_checker_error!")
                    self.driver.save_screenshot(f"/home/coder/project/phone/Data/log/liivm_checker_error_{self.username}.png")
                    self.bot.sendmessage(f"liivm : {time.strftime('%c', time.localtime())} --- {self.username} --- checker_error!")
                    self.bot.sendphoto(f"/home/coder/project/phone/Data/log/liivm_checker_error_{self.username}.png")

                except charger_error:
                    print("liivm_charger_error!")
                    self.driver.save_screenshot(f"/home/coder/project/phone/Data/log/liivm_charger_error_{self.username}.png")
                    self.bot.sendmessage(f"liivm : {time.strftime('%c', time.localtime())} --- {self.username} --- charger_error!")
                    self.bot.sendphoto(f"/home/coder/project/phone/Data/log/liivm_charger_error_{self.username}.png")
                
                except :
                    print("liivm_error!")
                    self.driver.save_screenshot(f"/home/coder/project/phone/Data/log/liivm_error_{self.username}.png")
                    self.bot.sendmessage(f"liivm : {time.strftime('%c', time.localtime())} --- {self.username} --- error!")
                    self.bot.sendphoto(f"/home/coder/project/phone/Data/log/liivm_error_{self.username}.png")
                
                else :
                    self.driver.save_screenshot(f"/home/coder/project/phone/Data/log/liivm_finish_{self.username}.png")
                    self.bot.sendmessage(f"liivm : {time.strftime('%c', time.localtime())} --- {self.username} --- success!")
                    self.bot.sendphoto(f"/home/coder/project/phone/Data/log/liivm_finish_{self.username}.png")
                    break

                finally:
                    self.driver.delete_all_cookies()


        except :
            raise liivm_err()