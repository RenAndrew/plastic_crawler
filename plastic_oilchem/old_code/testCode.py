# -*- coding: utf-8 -*-

from PIL import Image
import tesserocr
import locale
import os


os.chdir(r'C:\ProgramData\Anaconda2\envs\OCR\Lib\site-packages\tesserocr')

print('-' * 30)

im = Image.open(r'F:\git_repos\crawlers\plastic_price\code.jpg')

# print(tesserocr.tesseract_version())

result = tesserocr.image_to_text(im)

print(result)