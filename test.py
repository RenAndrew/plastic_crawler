# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains  #鼠标操作
import time
import json

# from pyvirtualdisplay import Display
# display = Display(visible=0, size=(1920, 1080))  
# display.start()


browser = webdriver.Chrome()
#browser = webdriver.Chrome('C:/Python27/chromedriver', service_args=['--verbose'], service_log_path='./chromelog.log')
browser.implicitly_wait(5)  # wait until the page is fully loaded.

browser.get('http://news.oilchem.net/login.shtml')

#print(browser.title)

userNameInput = browser.find_element_by_id('etuser_userLoginname')	
userNameInput.click()
userNameInput.send_keys('18815275529')

passwrdInput = browser.find_element_by_id('etuser_userPassword')
passwrdInput.click()
passwrdInput.send_keys('Cbnb12345')

verificationCode = browser.find_element_by_id('code')
verificationCode.click()


time.sleep(6)


submitBtn = browser.find_element_by_id('login')
submitBtn.click()

time.sleep(3)

cookie = {}
cookie_items = browser.get_cookies()
for cookie_item in cookie_items:
    cookie[cookie_item['name']] = cookie_item['value']
cookie_str = json.dumps(cookie)

print('----------------------')
print(cookie_str)

browser.close()
# prompt = frame.find_element_by_xpath('//body').find_element_by_xpath('//div[@id="logDiv"]')
# prompt = browser.find_element_by_xpath('//*[@id="logDiv"]/div[2]/div[2]/center/table[1]/tbody/tr[1]/td[1]')
# print(prompt.get_attribute('innerHTML'))

# userInputbox = browser.find_element_by_id('etuser_userLoginname') #browser.find_element_by_xpath('//*[@id="etuser_userLoginname"]')
# userInputbox.click()
# userInputbox.send_keys('18815275529 ')
#time.sleep(10)