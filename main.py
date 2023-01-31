import schedule
import sys
sys.path.append("/home/coder/project/merged/Program")
from themore import themore, tools
from qoo import qoo, qoo_err
from skylife import skylife, skylife_err
from amazon import amazon, amazon_err
from uplus import uplus, uplus_err
from liivm import liivm, liivm_err
import time

def job():
    try:
        # qoo('ilsun').main()
        # time.sleep(20)
        amazon('ilsun').main()
        time.sleep(20)
        skylife('ilsun').main()
        time.sleep(20)
        uplus('ilsun').main()
        time.sleep(20)
        liivm('ilsun').main()
        time.sleep(20)
    except qoo_err:
        print('qoo error!')
        qoo('ilsun').main()
    except amazon_err:
        print('amazon error!')
        amazon('ilsun').main()
    except skylife_err:
        print('skylife error!')
        skylife('ilsun').main()
    except uplus_err:
        print('uplus error!')
        uplus('ilsun').main()
    except liivm_err:
        print('liivm error!')
        liivm('ilsun').main()

def run():
    job()

schedule.every().day.at("17:46").do(run)

while True:
    schedule.run_pending()

