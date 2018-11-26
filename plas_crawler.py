# -*- coding: utf-8 -*-

import urllib
import urllib2

def  formulateUrl(productName, productModel, id=3975, webflag=2):
	baseUrl = 'http://price.oilchem.net/imPrice/getPrice.lz?'

	paramDict = {
		'id' : id,
		'priceDate' : '',
		'priceDate1' : '',
		'pName' : productName,
		'productModel' : productModel,
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

	return headers;

if __name__ == "__main__":
	print('-------------------------')

	reqUrl = formulateUrl('LLDPE', '丁烯基', 3975, 2)
