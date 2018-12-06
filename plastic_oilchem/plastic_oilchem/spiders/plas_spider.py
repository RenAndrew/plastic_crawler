# -*- coding: utf-8 -*-

import urllib
import urllib2
import zlib  #for gzip decompression
import os,sys
import time, datetime
import json
import demjson
# import chardet
from .. import plas_crawler

from .. import SpiderBase

class  PlasOilchemSpider(SpiderBase):
	"""爬取隆众价格网上塑料数据，直接调用数据API获取数据，Selenium登陆后自动填入cookie信息"""


	name = 'plas_spider'
	start_urls = [
        'http://price.oilchem.net/imPrice/listPrice.lz?id=3975&webFlag=2&hndz=1',
    ]

	def parse(self, response):
		plas_crawler.main()
		print('-'*30)
		# print (response.url)
    	
		