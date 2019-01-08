# -*- coding: utf-8 -*-

from PIL import Image
import tesserocr
import locale
import os
import time

def thresholdFilterImg(img, threshold=140):
	table=[]
	for i in range(256):
		if i < threshold:
			table.append(0)
		else:
			table.append(1)
	img = img.point(table, '1') #所有低于门限值的全部为0
	return img

def pictureTransform(img):
	size = img.size
	img = img.resize( (size[0]*5, size[1]*5), Image.ANTIALIAS)  #放大5倍

	size = img.size
	cutSizeX = int(size[0] * 0.87)		#magic number here
	cutSizeY = int(size[1] * 0.8)		
	img = img.crop((0,0, cutSizeX, cutSizeY))

	img = img.convert('L')		#转为灰度图片（黑白）

	#还可以进行二值化门限处理降低背景噪音增加精度 thresholdFilterImg
	return img

def calculate(decodedExp):
	tokens = decodedExp.split('+')
	op = '+'
	if (len(tokens) == 1):   # not plus operator
		tokens = decodedExp.split('-')
		if (len(tokens) == 1):		#neither plus nor minus, bad recoginization
			return -1
		op = '-'

	if len(tokens) != 2:
		return -1 #unknown condition

	left = tokens[0].encode('ascii').strip()
	right = tokens[1].encode('ascii').strip()

	# print('(%s %s %s)'%(left, op, right))

	left = int(left)
	right = int(right)

	if op == '+':
		return left + right
	else:
		return left - right

def decodePicuture(picpath):
	im = Image.open(picpath)
	reenforcedIm = pictureTransform(im)

	# im.show()

	codeText = tesserocr.image_to_text(reenforcedIm)

	print(codeText)

	try:
		retNumber = calculate(codeText)
	except:
		# reenforcedIm.show()
		return -1
	return retNumber



if __name__ == '__main__':
	for i in range(1,9):
		picpath = './code/00' + str(i) + '.jpg'
		
		finalCode = decodePicuture(picpath)
		print(finalCode)
		print('-----------------------')
