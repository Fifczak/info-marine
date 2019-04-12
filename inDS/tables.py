from tkinter import *
import csv


def createStandardTable(f,window):
    
    length = len(f)

    sizes = [0] * length
    for i in f:
                
    f.seek(0)
    trow = 0
    table = Frame(window)
    for i in f:
        for w,column in enumerate(i):
            Label(table,text=column,width=sizes[w],borderwidth=2,relief="groove",justify=LEFT,anchor=W, background='white').grid(column=w,row=trow,sticky=W)
        
        trow+=1
        
    return table