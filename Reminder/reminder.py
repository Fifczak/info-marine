import psycopg2
import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox

from tkinter.filedialog import askopenfilename
from tkinter import Tk

import matplotlib.pyplot as plt
import numpy as num
import tkinter as tkk
from tkinter import filedialog


connD=['testuser','info','localhost']
def q_run(connD, querry):
    username = connD[0]
    password = connD[1]
    host = connD[2]
    kport = "5432"
    kdb = "postgres"
    # cs = ' host="localhost",database="postgres", user= "postgres" , password="info" '
    cs = "dbname=%s user=%s password=%s host=%s port=%s" % (kdb, username, password, host, kport)
    conn = None
    conn = psycopg2.connect(str(cs))
    cur = conn.cursor()
    cur.execute(querry)
    try:
        result = cur.fetchall()
        return result
    except:
        pass
    conn.commit()
    cur.close()





def remindershow():
    class device:
        def __init__(self):
            self.lastraport = ''
            self.requestdate = ''
            self.lastraportdate =''



    parent = 79
    ss = (q_run(connD,"select raport_number,min(date) from measurements_low where parent ="+str(parent)+" group by raport_number order by min desc limit 1"))[0]
    lastfullrn = ss[0]
    lastfulldate= ss[1]
    print(lastfullrn,lastfulldate)
    querry = "SELECT dss.id, CASE WHEN dss.id ~E'^\\\d+$' THEN	(select name from devices where cast(devices.id as text)\
      =  dss.id limit 1) ELSE (select id from ds_structure where id  =  dss.id limit 1) END as sortint, dss.sort FROM ds_structure\
       as dss where dss.parent = " + str(parent)
    results = q_run(connD, querry)

    querry = "select id,raport_number,min(date) from measurements_low where parent =" + str(parent)+ "group by id,raport_number order by id,raport_number desc"
    resultr = q_run(connD, querry)


    remWindow = tk.Tk()
    remWindow.title("Reminder")

    devlistbox = Listbox(remWindow)
    devlistbox.config(width=0)
    #pointslist.bind('<Double-Button>', pointselect)
    p=0
    devlist = list()
    for line in results:
        for line2 in resultr:
            if str(line[0]) == str(line2[0]):
                x = device()
                x.lastraport = str(line2[1])
                x.lastraportdate = datetime.datetime.strptime(str(line2[2]), '%Y-%m-%d').date()
                devlistbox.insert(END, results[p][1])

                if x.lastraportdate >=  lastfulldate:
                    devlistbox.itemconfig(END, bg='Green')
                else:
                    devlistbox.itemconfig(END, bg='Red')
                devlist.append(x)
                break

        p+=1
    devlistbox.pack(side=LEFT, fill=BOTH)
    remWindow.mainloop()

remindershow()

