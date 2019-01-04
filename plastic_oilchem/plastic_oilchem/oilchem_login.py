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