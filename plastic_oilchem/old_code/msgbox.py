# -*- coding: utf-8 -*-
from Tkinter import *
import time

# # import Tkinter
import tkMessageBox as mb

def center_window(root, w = 300, h = 200):
	ws = root.winfo_screenwidth()
	hs = root.winfo_screenheight()
	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2)
	root.geometry("%dx%d+%d+%d" % (w, h, x, y))

root = Tk()
center_window(root, 2, 2)

root.wm_attributes('-topmost', 1)

retCode = mb.askokcancel('登陆状态', '是否继续？')

print(retCode)

# root.mainloop()
# root.destory()
root.withdraw()  #hide the window
time.sleep(5)
