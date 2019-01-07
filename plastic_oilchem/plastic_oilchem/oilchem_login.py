# -*- coding: utf-8 -*-

import urllib
import urllib2
import zlib  #for gzip decompression
import os,sys
import time, datetime
import json
import demjson
import random

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains  #鼠标操作
from selenium.webdriver.common.keys import Keys

from . import decode

# from Tkinter import *
# import tkMessageBox as mb

#center the root frame window
# def center_window(root, w = 300, h = 200):
# 	ws = root.winfo_screenwidth()
# 	hs = root.winfo_screenheight()
# 	x = (ws/2) - (w/2)
# 	y = (hs/2) - (h/2)
# 	root.geometry("%dx%d+%d+%d" % (w, h, x, y))

class AutoLogin:
	"""隆众网自动登录"""

	def getWorkingDir(self):
		return self.workingDir

	def __init__(self, workingDir):
		self.workingDir = workingDir

	def setAccount(self, accountName, password):
		self.accountName = accountName
		self.password = password

	def tryDecodeTimes(self, cookie, count):
		while( count > 0):
			count = count -1
			codeValue = self.refreshVerfCode(cookie)
			if (codeValue >1000 and codeValue < 10000):
				break;
			print('verification code error!')

		if count == 0:
			print('Tried 5 times to decode the verification code and failed, quit...')
			return None
		return codeValue

	def tryLoginByCode(self, submitUrl, codeValue, cookie):
		formData = dict()

		formData['username'] = self.accountName
		formData['password'] = self.password
		formData['code'] = str(codeValue)

		headers = {
			'Accept':'application/json, text/plain, */*',
			'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36',
			'Origin': 'http://news.oilchem.net',
			'Referer': 'http://news.oilchem.net/login.shtml',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
			'cookie' : cookie
		}

		req = urllib2.Request(submitUrl, headers=headers, data=urllib.urlencode(formData))

		response = urllib2.urlopen(req)
		retdata = response.read()
		#用gzip解压缩
		retMsg = zlib.decompress(retdata, 16+zlib.MAX_WBITS)
		print(retMsg)

		retMessage = demjson.decode(retMsg)

		if (retMessage['data'] == None or retMessage['data'] == '' or retMessage['data']['login'] != '1'):
			print('Login failed!')
			raise Exception('failed login.')

		cookie = response.headers['Set-Cookie']
		# print('-' * 30)
		# print(cookie)
		loginedCookie = self.generateCookie(retMessage['data'], cookie)

		return loginedCookie

	#用模拟表单提交的方式登录
	def formlogin(self, response):
		submitUrl = "http://news.oilchem.net/user/userLogin.do?ajax=1&chkbdwx=0&closewindow=&rnd=" + str(random.random()) + str(random.random())[2:6]
		cookie = response.headers['Set-Cookie']
		# print(cookie)

		countTriedMax = 3
		while (countTriedMax > 0):
			countTriedMax = countTriedMax - 1
			#Try to get and parse the verification code, try 5 times at most
			codeValue = self.tryDecodeTimes(cookie, 5)
			if codeValue is None:
				raise Exception('Program quit exception.') # this will quit the program

			try:
				loginedCookie = self.tryLoginByCode(submitUrl, codeValue, cookie)
				print('-'*30)
				print('Login successfully!')
				print('-'*30)
				return loginedCookie
			except:
				pass #do nothing but try again

		print('Login failed more than 3 times, sorry we have to quit program.')
		raise Exception('Program quit exception.')

	#generate a valid cookie for getting data, from login return information and setcookie info in the response
	def generateCookie(self, retData, setedCookie):
		cookieItems = setedCookie.split(';')
		cookieDict = {}
		for cookieItem in cookieItems:
			idx = cookieItem.find(',')
			if (idx > 0):
				cookieItem = cookieItem.split(',')[1]
			pair = cookieItem.split('=')
			valueset = (pair[0].strip(), pair[1].strip())
			cookieDict[valueset[0]] = valueset[1] 
			# print (valueset)

		# print (cookieDict)
		cookie = 'parentid=0; userid=' + str(retData['userNo']) + '; '
		cookie += ('password=' + cookieDict['password'] + '; ')
		cookie += ('AccessToken=' + cookieDict['AccessToken'] + ';' )
		cookie += ('username=' + cookieDict['username'] + ';' )
		cookie += ('sidid=' + cookieDict['sidid'] + ';' )
		cookie += ('userNo=' + str(retData['userNo']) + ';' )
		cookie += ('LZ_' + str(retData['userNo']) + '_UN=' + urllib.quote('安信证券股份有限公司') + '(axzq1010);')
		cookie += ('lz_usermember=' + urllib.quote(retData['userMember']) + ';' )
		cookie += 'lz_usermember=0%2C2; auto=0; refcheck=ok; refpay=0; refsite=http%3A%2F%2Fnews.oilchem.net%2Flogin.shtml; '
		cookie += 'Hm_lvt_47f485baba18aaaa71d17def87b5f7ec=1546486194; Hm_lpvt_47f485baba18aaaa71d17def87b5f7ec=1546486194'
		
		print('-' * 40)
		print (cookie)

		return cookie

	#Get the verification code picture and OCR it to get the code
	def refreshVerfCode(self, cookie):
		codeApiUrl = 'http://news.oilchem.net/getcode/api/?' + str(random.random()) + str(random.random())[2:6]   #18 digits random number
		
		# print(codeApiUrl)

		workDir = self.getWorkingDir()
		timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
		codeImgFilePath = workDir + '/code_' + timestamp + '.jpg'

		req = urllib2.Request(codeApiUrl)
		req.add_header('cookie', cookie)
		response = urllib2.urlopen(req)
		imgData = response.read()
			
		codeImgFile = open(codeImgFilePath, 'wb')
		codeImgFile.write(imgData)  
		codeImgFile.close()
		
		codeValue = decode.decodePicuture(codeImgFilePath)
		# print('Code value: %d' %(codeValue))
		# if (codeValue < 0 or codeValue > 9999):
		# 	raise Exception('Can not parse the verification code, please retry!')

		return codeValue

#login by selenium operations, extends AutoLogin
class SeleniumLogin(AutoLogin):

	def selelogin(self, response):
		browser = webdriver.Chrome()
		browser.implicitly_wait(5)  # wait until the page is fully loaded.

		countTriedMax = 3
		while (countTriedMax > 0):
			countTriedMax = countTriedMax - 1

			browser.get(response.url)

			userNameInput = browser.find_element_by_id('etuser_userLoginname')	
			userNameInput.click()
			userNameInput.send_keys(self.userName)

			passwrdInput = browser.find_element_by_id('etuser_userPassword')
			passwrdInput.click()
			passwrdInput.send_keys(self.userPassword)

			cookie_items = browser.get_cookies()
			cookie = self.cookieToStr(cookie_item)
			#Try to get and parse the verification code, try 5 times at most
			codeValue = self.tryDecodeTimes(cookie, 5)
			if codeValue is None:
				raise Exception('Program quit exception.') # this will quit the program

			try:
				# loginedCookie = self.tryLoginByCode(submitUrl, codeValue, cookie)
				verificationCode = browser.find_element_by_id('code')
				verificationCode.click()
				verificationCode.send_keys(codeValue)

				time.sleep(1)

				submitBtn = browser.find_element_by_id('login')
				submitBtn.click()
				time.sleep(3)

				#get the data page for updating cookie
				browser.get('http://price.oilchem.net/imPrice/listPrice.lz?id=3975&webFlag=2&hndz=1')
				time.sleep(3)
				cookie_items = browser.get_cookies()

				#test if really login by checking cookie
				if (not self.testLoginOK(cookie_items)):
					continue	#break the while loop and try again

				loginedCookie = self.cookieToStr(cookie_items)

				print ('-'*30)
				print ('Login successfully!')
				print (loginedCookie)
				print ('-'*30)
				browser.close()
				return loginedCookie
			except:
				pass #do nothing but try again

		browser.close()
		print('Login failed more than 3 times, sorry we have to quit program.')
		raise Exception('Program quit exception.')

	# def autologin(self):
	# 	browser = webdriver.Chrome()
	# 	browser.implicitly_wait(5)  # wait until the page is fully loaded.

	# 	browser.get(response.url)

	# 	userNameInput = browser.find_element_by_id('etuser_userLoginname')	
	# 	userNameInput.click()
	# 	userNameInput.send_keys(self.userName)

	# 	passwrdInput = browser.find_element_by_id('etuser_userPassword')
	# 	passwrdInput.click()
	# 	passwrdInput.send_keys(self.userPassword)

	# 	# time.sleep(5)
	# 	# verificationCodeImg = browser.find_element_by_id('rCode')
	# 	# srcLink = verificationCodeImg.get_attribute('src')
	# 	srcLink = 'http://news.oilchem.net/getcode/api/?' + str(random.random()) + str(random.random())[2:6]   #18 digits random number
		
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

	def testLoginOK(self, cookie_items):
		for cookie_item in cookie_items:
			if cookie_item['name'] == 'userid':
				return True
		return False

	def cookieToStr(self, cookie_items):
		cookie_str = ''
		for cookie_item in cookie_items:
			cookie_str += ( cookie_item['name'] + '=' + cookie_item['value'] + ';' )

		return cookie_str;

	# write the cookie to file, not use now
	def writeCookieConfig(self,cookie_items):
		# print('Current work directory:')
		# os.system('pwd')
		configFilePath = self.getWorkingDir() + '/_cookie_config.dat'
		outfile = open(configFilePath, 'w+')
		cookie_str = '';

		cookie_dict = {}
		for cookie_item in cookie_items:
		    cookie_dict[cookie_item['name']] = cookie_item['value']

		if (cookie_dict['Hm_lpvt_47f485baba18aaaa71d17def87b5f7ec'] is not None):
			cookie_str += ('Hm_lpvt_47f485baba18aaaa71d17def87b5f7ec=' + cookie_dict['Hm_lpvt_47f485baba18aaaa71d17def87b5f7ec'] + '; ')

		if (cookie_dict['parentid'] is not None):
			cookie_str += ('parentid=' + cookie_dict['parentid'] + '; ' )

		if (cookie_dict['username'] is not None):
			cookie_str += ('username=' + cookie_dict['username'] + '; ' )

		cookie_str += ('etuser_userLoginname=' + cookie_dict['username'])
		cookie_str += ('auto=1; ' ) #different from cookie? in cookie it is 0

		if (cookie_dict['LZ_730960_UN'] is not None):
			cookie_str += ('LZ_730960_UN=' + cookie_dict['LZ_730960_UN'] + '; ' )

		if (cookie_dict['lz_usermember'] is not None):
			cookie_str += ('lz_usermember=' + cookie_dict['lz_usermember'] + '; ' )

		if (cookie_dict['password'] is not None):
			cookie_str += ('password=' + cookie_dict['password'] + '; ' )

		if (cookie_dict['userid'] is not None):
			cookie_str += ('userid=' + cookie_dict['userid'] + '; ' )

		if (cookie_dict['sidid'] is not None):
			cookie_str += ('sidid=' + cookie_dict['sidid'] + '; ' )

		if (cookie_dict['userNo'] is not None):
			cookie_str += ('userNo=' + cookie_dict['userNo'] + '; ' )

		if (cookie_dict['refcheck'] is not None):
			cookie_str += ('refcheck=' + cookie_dict['refcheck'] + '; ' )

		if (cookie_dict['refpay'] is not None):
			cookie_str += ('refpay=' + cookie_dict['refpay'] + '; ' )

		if (cookie_dict['refsite'] is not None):
			cookie_str += ('refsite=' + cookie_dict['refsite'] + '; ' )  # refsite need to be the data called page?  http%3A%2F%2Fprice.oilchem.net%2FimPrice%2FlistPrice.lz%3Fid%3D3975%26webFlag%3D2%26hndz%3D1

		if (cookie_dict['Hm_lvt_47f485baba18aaaa71d17def87b5f7ec'] is not None):
			cookie_str += ('Hm_lvt_47f485baba18aaaa71d17def87b5f7ec=' + cookie_dict['Hm_lvt_47f485baba18aaaa71d17def87b5f7ec'] + '; ' )

		if (cookie_dict['AccessToken'] is not None):
			cookie_str += ('AccessToken=' + cookie_dict['AccessToken'] + '; ' )

		if (cookie_dict['JSESSIONID'] is not None):
			cookie_str += ('JSESSIONID=' + cookie_dict['JSESSIONID'] + '' )

		print(cookie_str)

		outfile.write(cookie_str)
		outfile.close()
		return configFilePath
