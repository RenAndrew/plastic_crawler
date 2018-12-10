# -*- coding: utf-8 -*-

from PIL import Image
import tesserocr
import locale
import os
import time

def pictureTransform(img):
	size = img.size
	img = img.resize( (size[0]*5, size[1]*5), Image.ANTIALIAS)  #放大5倍

	img = img.convert('L')		#转为灰度图片（黑白）
	#还可以进行二值化门限处理降低背景噪音增加精度
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

	print('(%s %s %s)'%(left, op, right))

	left = int(left)
	right = int(right)

	if op == '+':
		return left + right
	else:
		return left + right

def decodePicuture(picpath):
	im = Image.open(picpath)
	reenforcedIm = pictureTransform(im)

	codeText = tesserocr.image_to_text(reenforcedIm)

	# print(codeText)

	retNumber = calculate(codeText)

	return retNumber

if __name__ == '__main__':
	for i in range(1,6):
		picpath = './code/00' + str(i) + '.jpg'
		
		finalCode = decodePicuture(picpath)
		print(finalCode)
		# print('-----------------------')
