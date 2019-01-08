# -*- coding: utf-8 -*-

from PIL import Image
import decode
import tesserocr
import os

# print('----------------')

# picpath = '/home/renxb/pypy/code/001.jpg'

# img = Image.open(picpath)
# # img.show()

# img = decode.pictureTransform(img)
# size = img.size
# img = img.crop((0,0, 360, 100))
# # img.show()
# print ('%f , %f' % (360.0/float(size[0]), 100.0/float(size[1])) )



# codeText = tesserocr.image_to_text(img)
# print(codeText)

# img = decode.thresholdFilterImg(img, 140)
# img.show()

# codeText = tesserocr.image_to_text(img)
# print(codeText)
# decode.

if __name__ == '__main__':
	print('----------------')
	imgDir = '/home/renxb/git_repos/plastic_crawler/plastic_oilchem/work_dir/'
	for fileName in os.listdir(imgDir):
		if fileName.find('.jpg') > 0 :
			print(fileName)
			picpath = imgDir + fileName
		else:
			continue
		img = Image.open(picpath)
		img = decode.pictureTransform(img)
		size = img.size
		img = img.crop((0,0, 360, 100))
		# codeText = tesserocr.image_to_text(img)
		# print(codeText)

		img = decode.thresholdFilterImg(img, 140)
		# img.show()

		codeText = tesserocr.image_to_text(img)
		print(codeText)

		# print(fileName)