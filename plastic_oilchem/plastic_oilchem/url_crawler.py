# -*- coding: utf-8 -*-

import urllib
import urllib2
import zlib  #for gzip decompression
import os,sys
import time, datetime
import json
import demjson


class UrlCrawlerConfig:
	
	def __init__(self, cookie, crawler_name, crawler_config_file, outputpath, pagesize=200):
		self.cookie = cookie
		self.crawlerName = crawler_name
		self.crawlerConfigFile = crawler_config_file
		self.outputpath = outputpath
		self.pageSize = pagesize

		self.configDetails()

	def setCookieInHeader(self, cookie):
		headers = {
			'Accept':'application/json, text/plain, */*',
		    'Accept-Encoding':'gzip, deflate',
		    'Accept-Language':'zh-CN,zh;q=0.8',
		    'Connection':'keep-alive',
		    'Content-Type':'application/x-www-form-urlencoded',
		    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36',
		    'cookie' : cookie
		}

		return headers

	def configDetails(self):
		self.apiHeaders = self.setCookieInHeader(self.cookie)

		#get the config json object of current crawler
		with open(self.crawlerConfigFile, 'r') as configFile:  #BAD here!!!
			config = configFile.read()
			# print (config)
			crawler_configs = json.loads(config)

		for crawler_config in crawler_configs:
			if (crawler_config['crawler_name'] == self.crawlerName):
				self.config = crawler_config

		if self.config is None:
			raise Exception('Can not find the crawler configuration!')

		if not self.config.has_key('data_api_url'):
			raise Exception('Can not find the data api url!')

		self.dataUrl = self.config['data_api_url']

		if self.config.has_key('column_header'):
			self.csvHead = (self.config['column_header'] + '\n')
		else:
			self.csvHead = u'ID,报价日期,产品名称,规格型号,地区,价格类型,低端价,高端价,中间价,单位,涨跌幅,人民币价,--,备注\n'#default header

class UrlCrawler:

	# crawlerConfig : UrlCrawlerConfig
	def __init__(self, crawlerConfig):
		
		self.config = crawlerConfig

		print(self)

	def postParameter(self, page, pageSize=40):
		postdata = {
			'page' : page,
			'rp' : pageSize,
			'sortname' : 'id',
			'sortorder' : 'asc',
			'query' : None,
			'qtype' : None
		}
		return urllib.urlencode(postdata)

	def getDataPage(self, reqUrl, headers, pageSize, pageIdx):
		if (pageIdx < 1 or pageIdx > pageSize):
			raise "Incorrect page number " + str(pageIdx)

		data = self.postParameter(pageIdx, pageSize)

		req = urllib2.Request(reqUrl, headers=headers, data=data)
		#customization opener to add cookies
		#opener = urllib2.build_opener()
		response = urllib2.urlopen(req)
		retdata = response.read()    #返回的数据是经过压缩的
		#用gzip解压缩
		jsonData = zlib.decompress(retdata, 16+zlib.MAX_WBITS)

		return demjson.decode(jsonData) #the data is in raw javascript format, not json, convert it to json (python object).


	def getDataApiUrl(self):
		return self.config.dataUrl

	def downloadData(self):
		print('-------------- Start crawling -----------------------')
		
		startTime = time.time()
		config = self.config
		outputpath = config.outputpath
		pageSize = config.pageSize
		reqUrl = config.dataUrl
		headers = config.apiHeaders
		csvHead = config.csvHead

		jsonData = self.getDataPage(reqUrl, headers, pageSize, 1)  # get the first page of data

		totalItemCount = jsonData['total']
		maxPage = (totalItemCount + pageSize - 1) / pageSize  	#整数除法向上取整
		print('====> Total item count: ' + str(totalItemCount) + ', number of pages: ' + str(maxPage))
		print('')

		timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
		outputFileName = outputpath + '/' + config.crawlerName +'_out_' + timestamp + '.csv'
		print('==== output to:')
		print(outputFileName)
		outputFile = open(outputFileName, 'w+')

		for i in range(1,maxPage):
			if (i == 1):
				outputFile.write(csvHead.encode('utf-8'))
			jsonData = self.getDataPage(reqUrl, headers, pageSize, i)
			for j in range(0, len(jsonData['rows']) ):
				priceItem = jsonData['rows'][j]
				id = priceItem['id']
				cell = priceItem['cell']
				# line = id + ',' + ','.join(cell) + '\n'
				line = ','.join(cell) + '\n'
				
				line = line.encode('utf-8')
				# print(line)
				outputFile.write(line)

		outputFile.close()

		endTime = time.time()
		print('Compelete the job in ' + str(endTime - startTime) + ' seconds.')
		print('------------ End -------------')
		return 0

	# def downloadData(crawlerName, cookieValue, outputpath, configFile):
	# 	print('-------------- Start crawling -----------------------')
	# 	# os.system('pwd')
	# 	startTime = time.time()
	# 	pageSize = 200 #define the page size

	# 	global CRAWLER_CONFIG_FILE
	# 	CRAWLER_CONFIG_FILE = configFile
	# 	reqUrl = getDataApiUrl(crawlerName)

	# 	headers = setCookieInHeader(cookieValue)

	# 	jsonData = getDataPage(reqUrl, headers, pageSize, 1)  # get the first page of data

	# 	totalItemCount = jsonData['total']
	# 	maxPage = (totalItemCount + pageSize - 1) / pageSize  #整数除法向上取整
	# 	print('====> Total item count: ' + str(totalItemCount) + ', number of pages: ' + str(maxPage))
	# 	print('')

	# 	timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
	# 	outputFileName = outputpath + '/' + crawlerName +'_out_' + timestamp + '.csv'
	# 	print('==== output to:')
	# 	print(outputFileName)
	# 	outputFile = open(outputFileName, 'w+')

	# 	for i in range(1,maxPage):
	# 		if (i == 1):
	# 			csvHead = u'ID,报价日期,产品名称,规格型号,地区,价格类型,低端价,高端价,中间价,单位,涨跌幅,人民币价,--,备注\n'
	# 			# print(csvHead)
	# 			outputFile.write(csvHead.encode('utf-8'))
				
	# 		jsonData = getDataPage(reqUrl, headers, pageSize, i)
	# 		for j in range(0, len(jsonData['rows']) ):
	# 			priceItem = jsonData['rows'][j]
	# 			id = priceItem['id']
	# 			cell = priceItem['cell']
	# 			# line = id + ',' + ','.join(cell) + '\n'
	# 			line = ','.join(cell) + '\n'
				
	# 			line = line.encode('utf-8')
	# 			# print(line)
	# 			outputFile.write(line)

	# 	outputFile.close()

	# 	endTime = time.time()
	# 	print('Compelete the job in ' + str(endTime - startTime) + ' seconds.')
	# 	print('------------ End -------------')
	# 	return 0