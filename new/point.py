from Tkinter import *
from PIL import ImageTk, Image
import tkFileDialog
import time
import threading
import random
import Queue
import re
import sys
import d2xx
import tkMessageBox
import os
import dataset
import winsound
import time
import tkSimpleDialog
import customtkSimpleDialog
import admin
import guardMultiListBox
import multiListBox

db = dataset.connect('sqlite:///mydatabase.db')

class Point:
    def __init__(self, table, canvas, coord, repeater,name, color='black'):

        (x,y) = coord
        self.item = canvas.create_oval(x-5, y-5, x+5, y+5,
                                outline=color, fill=color, tags="house")
        self.text = canvas.create_text(x+0, y-15, text=repeater)
        self.repeater = repeater
        self.canvas = canvas
        self.table = table
        self.isPanic = False

        self._drag_data = {"x": 0, "y": 0, "item": None}

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        canvas.tag_bind(self.item, "<ButtonPress-1>", self.OnTokenButtonPress)
        canvas.tag_bind(self.item, "<ButtonRelease-1>", self.OnTokenButtonRelease)
        canvas.tag_bind(self.item, "<B1-Motion>", self.OnTokenMotion)


    def OnTokenButtonPress(self, event):
        '''Being drag of an object'''
        # record the item and its location
        print event.x, event.y
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def OnTokenButtonRelease(self, event):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

        data = dict(repeater=self.repeater, coordx=event.x, coordy=event.y)
        self.table.update(data, ['repeater'])


    def OnTokenMotion(self, event):
        '''Handle dragging of an object'''
        # compute how much this object has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        self.canvas.move(self.text, delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y



class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        # self.scale("all",0,0,wscale,hscale)