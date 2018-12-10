# -*- coding: utf-8 -*-

from PIL import Image
import decode
import tesserocr

print('----------------')

picpath = '/home/renxb/pypy/code/001.jpg'

img = Image.open(picpath)
# img.show()

img = decode.pictureTransform(img)
size = img.size
img = img.crop((0,0, 360, 100))
# img.show()
print ('%f , %f' % (360.0/float(size[0]), 100.0/float(size[1])) )



codeText = tesserocr.image_to_text(img)
print(codeText)

img = decode.thresholdFilterImg(img, 140)
img.show()

codeText = tesserocr.image_to_text(img)
print(codeText)
# decode.