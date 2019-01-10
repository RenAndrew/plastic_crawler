# -*- coding: utf-8 -*-

import urllib
import urllib2
import zlib  #for gzip decompression
import os,sys
import time, datetime
import json
import demjson
import random
# import chardet

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains  #鼠标操作
from selenium.webdriver.common.keys import Keys

from .. import plas_crawler
from .. import decode
from .. import oilchem_login
from .. import SpiderBase

class  PlasOilchemSpider(SpiderBase):
	"""爬取隆众价格网上塑料数据，直接调用数据API获取数据，自动登录并利用登录后的cookie获取权限"""

	userPassword = 'ax1010zq'
	userName = 'axzq1010'

	name = 'lldpe_usd'
	start_urls = [
		'http://news.oilchem.net/login.shtml'
	]

	price_name = 'LLDPE_east_china_USD' 		#LL华东价格usd
	# price_name = 'LDPE_USD'						#LD华东价格usd

	def parse(self, response ):
		print (response.url)
		# cookieAfterLogin = self.login_by_formsubmit(response)
		cookieAfterLogin = self.login_by_selenium(response)

		#real crawler start here
		print('Start crawl data!')
		plas_crawler.downloadData(self.price_name, cookieAfterLogin, self.getOutputPath(), self.getCrawlerConfigFile())

	#login by simulating form submit as the webpage does.
	def login_by_formsubmit(self, response):
		print(response.url)
		print('----------Try to login-------------')
		loginMachine = oilchem_login.AutoLogin(self.getWorkingDir())

		loginMachine.setAccount(self.userName, self.userPassword)
		cookieAfterLogin = loginMachine.formlogin(response)

		return cookieAfterLogin

	#login by selenium
	def login_by_selenium(self, response):
		print('----------Try to login-------------')
		loginMachine = oilchem_login.SeleniumLogin(self.getWorkingDir())

		loginMachine.setAccount(self.userName, self.userPassword)
		cookieAfterLogin = loginMachine.selelogin(response)

		# print (cookieAfterLogin)
		return cookieAfterLogin
		
		
	def getWorkingDir(self):
		if os.path.exists('./work_dir'):
			return os.getcwd() + '/work_dir'
		else:
			os.mkdir('work_dir')
			return os.getcwd() + '/work_dir'

	def getOutputPath(self):
		if os.path.exists('./output'):
			return os.getcwd() + '/output'
		else:
			os.mkdir('output')
			return os.getcwd() + '/output'

	def getCrawlerConfigFile(self):
		if os.path.exists('./all_crawlers.json'):
			return os.path.abspath('./all_crawlers.json')
		elif os.path.exists('./plastic_oilchem/all_crawlers.json'):
			return os.path.abspath('./plastic_oilchem/all_crawlers.json')
		else:
			raise Exception('ERROR: Can not find all_crawlers.json!')


	#######################################################################
	# The following code it not used now, just work as a backup solution #
	# which is login by selenium
	# def autologin(self):
	# 	browser = webdriver.Chrome()
	# 	browser.implicitly_wait(5)  # wait until the page is fully loaded.

	# 	browser.get('http://news.oilchem.net/login.shtml')

	# 	userNameInput = browser.find_element_by_id('etuser_userLoginname')	
	# 	userNameInput.click()
	# 	userNameInput.send_keys(self.userName)

	# 	passwrdInput = browser.find_element_by_id('etuser_userPassword')
	# 	passwrdInput.click()
	# 	passwrdInput.send_keys(self.userPassword)

	# 	# time.sleep(5)
	# 	# verificationCodeImg = browser.find_element_by_id('rCode')
	# 	# srcLink = verificationCodeImg.get_attribute('src')
		# srcLink = 'http://news.oilchem.net/getcode/api/?' + str(random.random()) + str(random.random())[2:6]   #18 digits random number
		
	# 	print(srcLink)

	# 	cookie_items = browser.get_cookies()

	# 	# print(cookie_items)
	# 	workDir = self.getWorkingDir()
	# 	timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
	# 	codeImgFilePath = workDir + '/code_' + timestamp + '.jpg'

	# 	if (srcLink is not None):
	# 		req = urllib2.Request(srcLink)
	# 		#when getting verification code image, must add cookie to the request,
	# 		#or the server will not bond the verification code with your session.
	# 		#and the verification will failed.
	# 		req.add_header('cookie', self.cookieToStr(cookie_items)) 
	# 		response = urllib2.urlopen(req)
	# 		imgData = response.read()
			
	# 		codeImgFile = open(codeImgFilePath, 'wb')
	# 		codeImgFile.write(imgData)  
	# 		codeImgFile.close()

	# 	else:
	# 		raise Exception('Can not get the verification code image!')

	# 	codeValue = decode.decodePicuture(codeImgFilePath)
	# 	print('Code value: %d' %(codeValue))
	# 	if (codeValue < 0 or codeValue > 9999):
	# 		browser.close()
	# 		raise Exception('Can not parse the verification code, please retry!')

	# 	verificationCode = browser.find_element_by_id('code')
	# 	verificationCode.click()
	# 	verificationCode.send_keys(codeValue)

	# 	time.sleep(1)

	# 	submitBtn = browser.find_element_by_id('login')
	# 	submitBtn.click()
	# 	time.sleep(3)

	# 	#get the data page for updating cookie
	# 	browser.get('http://price.oilchem.net/imPrice/listPrice.lz?id=3975&webFlag=2&hndz=1')
	# 	time.sleep(30)
	# 	cookie_items = browser.get_cookies()

	# 	#test if really login by checking cookie
	# 	if (not self.testLoginOK(cookie_items)):
	# 		browser.close()
	# 		raise Exception('Can not login successfully!')

	# 	# print(cookie_items)
	# 	# configFilePath = self.writeCookieConfig(cookie_items)
	# 	configFilePath = self.getWorkingDir() + '/cookie_config.dat'
	# 	with open(configFilePath, 'w+') as outfile:
	# 		outfile.write(self.cookieToStr(cookie_items))

	# 	browser.close()

	# 	return configFilePath

	# def testLoginOK(self, cookie_items):
	# 	for cookie_item in cookie_items:
	# 		if cookie_item['name'] == 'userid':
	# 			return True
	# 	return False

	# def cookieToStr(self, cookie_items):
	# 	cookie_str = ''
	# 	for cookie_item in cookie_items:
	# 		cookie_str += ( cookie_item['name'] + '=' + cookie_item['value'] + ';' )

	# 	return cookie_str;

	# def writeCookieConfig(self,cookie_items):
	# 	# print('Current work directory:')
	# 	# os.system('pwd')
	# 	configFilePath = self.getWorkingDir() + '/_cookie_config.dat'
	# 	outfile = open(configFilePath, 'w+')
	# 	cookie_str = '';

	# 	cookie_dict = {}
	# 	for cookie_item in cookie_items:
	# 	    cookie_dict[cookie_item['name']] = cookie_item['value']

	# 	if (cookie_dict['Hm_lpvt_47f485baba18aaaa71d17def87b5f7ec'] is not None):
	# 		cookie_str += ('Hm_lpvt_47f485baba18aaaa71d17def87b5f7ec=' + cookie_dict['Hm_lpvt_47f485baba18aaaa71d17def87b5f7ec'] + '; ')

	# 	if (cookie_dict['parentid'] is not None):
	# 		cookie_str += ('parentid=' + cookie_dict['parentid'] + '; ' )

	# 	if (cookie_dict['username'] is not None):
	# 		cookie_str += ('username=' + cookie_dict['username'] + '; ' )

	# 	cookie_str += ('etuser_userLoginname=' + cookie_dict['username'])
	# 	cookie_str += ('auto=1; ' ) #different from cookie? in cookie it is 0

	# 	if (cookie_dict['LZ_730960_UN'] is not None):
	# 		cookie_str += ('LZ_730960_UN=' + cookie_dict['LZ_730960_UN'] + '; ' )

	# 	if (cookie_dict['lz_usermember'] is not None):
	# 		cookie_str += ('lz_usermember=' + cookie_dict['lz_usermember'] + '; ' )

	# 	if (cookie_dict['password'] is not None):
	# 		cookie_str += ('password=' + cookie_dict['password'] + '; ' )

	# 	if (cookie_dict['userid'] is not None):
	# 		cookie_str += ('userid=' + cookie_dict['userid'] + '; ' )

	# 	if (cookie_dict['sidid'] is not None):
	# 		cookie_str += ('sidid=' + cookie_dict['sidid'] + '; ' )

	# 	if (cookie_dict['userNo'] is not None):
	# 		cookie_str += ('userNo=' + cookie_dict['userNo'] + '; ' )

	# 	if (cookie_dict['refcheck'] is not None):
	# 		cookie_str += ('refcheck=' + cookie_dict['refcheck'] + '; ' )

	# 	if (cookie_dict['refpay'] is not None):
	# 		cookie_str += ('refpay=' + cookie_dict['refpay'] + '; ' )

	# 	if (cookie_dict['refsite'] is not None):
	# 		cookie_str += ('refsite=' + cookie_dict['refsite'] + '; ' )  # refsite need to be the data called page?  http%3A%2F%2Fprice.oilchem.net%2FimPrice%2FlistPrice.lz%3Fid%3D3975%26webFlag%3D2%26hndz%3D1

	# 	if (cookie_dict['Hm_lvt_47f485baba18aaaa71d17def87b5f7ec'] is not None):
	# 		cookie_str += ('Hm_lvt_47f485baba18aaaa71d17def87b5f7ec=' + cookie_dict['Hm_lvt_47f485baba18aaaa71d17def87b5f7ec'] + '; ' )

	# 	if (cookie_dict['AccessToken'] is not None):
	# 		cookie_str += ('AccessToken=' + cookie_dict['AccessToken'] + '; ' )

	# 	if (cookie_dict['JSESSIONID'] is not None):
	# 		cookie_str += ('JSESSIONID=' + cookie_dict['JSESSIONID'] + '' )

	# 	print(cookie_str)

	# 	outfile.write(cookie_str)
	# 	outfile.close()
	# 	return configFilePath

	