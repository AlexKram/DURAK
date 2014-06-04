#!/usr/bin/python

from Tkinter import *
from functools import partial
import time

root = Tk()

def fu(*args,**kwargs):
	print args
	print kwargs
	if len(args)>0:
		args[0].destroy()

w = Button(root, text="Hello, world!",command=fu)
w.pack()



for x in xrange(1,10000000000000):
	root.update()
	time.sleep(1.0/50.0/2.0)
	if (x%50)==0:
		m=Button(root, text="Hello-"+str(x))
		m['command']=partial(fu,m)
		m.pack()

