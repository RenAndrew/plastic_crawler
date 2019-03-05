# -*- coding: utf-8 -*-

import urllib
import urllib2
import zlib  #for gzip decompression
import os,sys
import time, datetime
import json
import demjson
# import chardet

#global varibles
CRAWLER_CONFIG_FILE = './all_crawlers.json'

def  formulateUrl(productName, productModel, id=3975, webflag=2):
	baseUrl = 'http://price.oilchem.net/imPrice/getPrice.lz?'

	paramDict = {
		'id' : id,
		'priceDate' : '',
		'priceDate1' : '',
		'pName1' : productName,
		'productModel1' : productModel,
		'pArea1' : '',
		'pType1' : '',
		'keyword' : '',
		'orderType' : '',
		'webFlag' : webflag
	}

	parameter = urllib.urlencode(paramDict)
	#parameter = 'id=%s&priceDate=&priceDate1=&pName=%s&pModel1=%spArea1=&pType1=&keyword=&orderType=&webFlag=%s' % (id, productName, productModel, webflag)

	print(baseUrl + parameter)

	return baseUrl + parameter

def setCookieInHeader(cookie):
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

def postParameter(page, pageSize=40):
	postdata = {
		'page' : page,
		'rp' : pageSize,
		'sortname' : 'id',
		'sortorder' : 'asc',
		'query' : None,
		'qtype' : None
	}
	return urllib.urlencode(postdata)

def getDataPage(reqUrl, headers, pageSize, pageIdx):
	if (pageIdx < 1 or pageIdx > pageSize):
		raise "Incorrect page number " + str(pageIdx)

	data = postParameter(pageIdx, pageSize)

	req = urllib2.Request(reqUrl, headers=headers, data=data)
	#customization opener to add cookies
	#opener = urllib2.build_opener()
	response = urllib2.urlopen(req)
	retdata = response.read()    #返回的数据是经过压缩的
	#用gzip解压缩
	jsonData = zlib.decompress(retdata, 16+zlib.MAX_WBITS)

	return demjson.decode(jsonData) #the data is in raw javascript format, not json, convert it to json (python object).

def main(configFilePath):
	print('-------------- Start crawling -----------------------')
	# os.system('pwd')
	startTime = time.time()
	pageSize = 200 #define the page size

	reqUrl = formulateUrl('LLDPE', '丁烯基', 3975, 2)

	cookieConfigFile = open(configFilePath, 'r')
	cookieContent = cookieConfigFile.read()
	headers = setCookieInHeader(cookieContent)
	#print(cookieContent);
	cookieConfigFile.close()

	jsonData = getDataPage(reqUrl, headers, pageSize, 1)  # get the first page of data

	totalItemCount = jsonData['total']
	maxPage = (totalItemCount + pageSize - 1) / pageSize  #整数除法向上取整
	print('====> Total item count: ' + str(totalItemCount) + ', number of pages: ' + str(maxPage))
	print('')

	timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
	outputFileName= 'plas_out_' + timestamp + '.csv'
	print(outputFileName)
	outputFile = open(outputFileName, 'w+')

	for i in range(1,maxPage):
		if (i == 1):
			csvHead = u'ID,报价日期,产品名称,规格型号,地区,价格类型,低端价,高端价,中间价,单位,涨跌幅,人民币价,备注\n'
			# print(csvHead)
			outputFile.write(csvHead.encode('utf-8'))
			continue  #skip the first page because it has been already fetched
		else:
			jsonData = getDataPage(reqUrl, headers, pageSize, i)
		for j in range(0, len(jsonData['rows']) ):
			priceItem = jsonData['rows'][j]
			id = priceItem['id']
			cell = priceItem['cell']
			line = id + ',' + ','.join(cell) + '\n'
			# line = line.decode('ascii')
			line = line.encode('utf-8')
			# print(line)
			outputFile.write(line)

	outputFile.close()

	endTime = time.time()
	print('Compelete the job in ' + str(endTime - startTime) + ' seconds.')
	print('------------ End -------------')
	return 0

def getDataApiUrl(crawler_name):
	with open(CRAWLER_CONFIG_FILE, 'r') as configFile:
		config = configFile.read()
		# print (config)
		crawler_configs = json.loads(config)

	for crawler_config in crawler_configs:
		if (crawler_config['crawler_name'] == crawler_name):
			return crawler_config['data_api_url']

	return None

#same as main, but get the cookie from parameter
def downloadData(crawlerName, cookieValue, outputpath, configFile):
	print('-------------- Start crawling -----------------------')
	# os.system('pwd')
	startTime = time.time()
	pageSize = 200 #define the page size

	global CRAWLER_CONFIG_FILE
	CRAWLER_CONFIG_FILE = configFile
	reqUrl = getDataApiUrl(crawlerName)

	headers = setCookieInHeader(cookieValue)

	jsonData = getDataPage(reqUrl, headers, pageSize, 1)  # get the first page of data

	totalItemCount = jsonData['total']
	maxPage = (totalItemCount + pageSize - 1) / pageSize  #整数除法向上取整
	print('====> Total item count: ' + str(totalItemCount) + ', number of pages: ' + str(maxPage))
	print('')

	timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
	outputFileName = outputpath + '/' + crawlerName +'_out_' + timestamp + '.csv'
	print('==== output to:')
	print(outputFileName)
	outputFile = open(outputFileName, 'w+')

	for i in range(1,maxPage):
		if (i == 1):
			csvHead = u'ID,报价日期,产品名称,规格型号,地区,价格类型,低端价,高端价,中间价,单位,涨跌幅,人民币价,--,备注\n'
			# print(csvHead)
			outputFile.write(csvHead.encode('utf-8'))
			
		jsonData = getDataPage(reqUrl, headers, pageSize, i)
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

if __name__ == "__main__":
	main('./work_dir/cookie_config.dat')

	# #get the total number of items
	# nstart = jsonData.index('total:')
	# totalStr = jsonData[nstart + 6 : nstart+20]
	
	# nend = totalStr.index(',')
	# totalStr = totalStr[0:nend].strip()
	# totalItemCount = int(totalStr)
	# maxPage = (totalItemCount + pageSize - 1) / pageSize  #整数除法向上取整

	# print('====> Total item count: ' + str(totalItemCount) + ', number of pages: ' + str(maxPage))
	# print('')

	# tmpfilename = 'tmp.js'
	# outfile = open(tmpfilename, 'w+')
	# outfile.write('exports.data = ')
	# outfile.write(jsonData)
	# outfile.close()

	# os.system('node process.js')

	# for i in range(2, maxPage):
	# 	jsonData = getDataPage(reqUrl, headers, pageSize, i)
	# 	tmpfilename = 'tmp.js'
	# 	outfile = open(tmpfilename, 'w+')
	# 	outfile.write('exports.data = ')
	# 	outfile.write(jsonData)
	# 	outfile.close()

	# 	os.system('node process.js')
	
	