import tesserocr
from PIL import Image
image=Image.open('test.png')
image=image.convert("L") #转为灰度图
threshold=80  #门限值
table=[]
for i in range(256):
    if i <threshold:
        table.append(0)
    else:
        table.append(1)
image=image.point(table,'1')  #所有低于门限值的全部为0
image.show()
print(tesserocr.image_to_text(image))