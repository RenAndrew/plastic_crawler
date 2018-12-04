# -*- coding: utf-8 -*-

import urllib
import urllib2
import zlib  #for gzip decompression
import os,sys
import time, datetime
import json
import demjson
# import chardet

from .. import SpiderBase

class  PlasOilchemSpider(SpiderBase):
	"""docstring for  PlasOilchemSpider"""


	name = 'plas_spider'
	start_urls = [
        'http://price.oilchem.net/imPrice/listPrice.lz?id=3975&webFlag=2&hndz=1',
    ]

	def parse(self, response):
		print('-'*30)
		print (response.url)
    	
		