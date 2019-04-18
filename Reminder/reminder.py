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
            self.status =''

            self.name = ''
            self.id = ''
            self.lastraport = ''
            self.requestdate = ''
            self.lastraportdate =''

    def getships(evt):
        w = evt.widget
        index = int(w.curselection()[0])
        shipname = w.get(index)
        makeships(shipname)

    def makeships(shipname):
        querry = "select name from main where parent =(select id from main where name = '" + str(
            shipname) + "' limit 1) order by name"
        ships = q_run(connD, querry)
        Shiplistbox.delete(0, 'end')

        for line in ships:
            Shiplistbox.insert(END, line[0])

    def getdevs(evt):
        w = evt.widget
        index = int(w.curselection()[0])
        shipname = w.get(index)
        makedevs(shipname)

    def makedevs(shipname):
        def devremdet(evt):
            w = evt.widget
            index = int(w.curselection()[0])
            detWindow = tk.Tk()
            detWindow.title("Reminder details")

            LabName = tk.Label(detWindow,text =str(devlist[index].name)).pack()
            LabId   = tk.Label(detWindow,text =str(devlist[index].id)).pack()
            LabLastRN  = tk.Label(detWindow,text ="Last report: " + str(devlist[index].lastraport)).pack()
            LabLastRDate  = tk.Label(detWindow,text ="Last date: " + str(devlist[index].lastraportdate)).pack()




            detWindow.mainloop()
        devlistbox.delete(0, 'end')

        querry = "select id from main where name = '" + str(shipname)+ "'"
        parent = q_run(connD,querry)[0][0]

        ss = (q_run(connD, "select raport_number,min(date) from measurements_low where parent =" + str(
            parent) + " group by raport_number order by min desc limit 1"))[0]
        lastfullrn = ss[0]
        lastfulldate = ss[1]
        print(lastfullrn, lastfulldate)
        querry = "SELECT dss.id, CASE WHEN dss.id ~E'^\\\d+$' THEN	(select name from devices where cast(devices.id as text)\
             =  dss.id limit 1) ELSE (select id from ds_structure where id  =  dss.id limit 1) END as sortint, dss.sort FROM ds_structure\
              as dss where dss.parent = " + str(parent)
        results = q_run(connD, querry)

        querry = "select id,raport_number,min(date) from measurements_low where parent =" + str(
            parent) + "group by id,raport_number order by id,raport_number desc"
        resultr = q_run(connD, querry)

        querry ="select id,raport_number from reminder where status is null and parent = " + str(parent)
        remindertbl = q_run(connD, querry)

        print(querry)
        p = 0

        for line in results:
            for line2 in resultr:
                if str(line[0]) == str(line2[0]):
                    x = device()
                    x.name = str(line[1])
                    x.id = str(line2[0])
                    x.lastraport = str(line2[1])
                    x.lastraportdate = datetime.datetime.strptime(str(line2[2]), '%Y-%m-%d').date()
                    devlistbox.insert(END, results[p][1])

                    if x.lastraportdate >= lastfulldate:
                        devlistbox.itemconfig(END, bg='Green')
                        x.status = 'OK'
                        for line3 in remindertbl:   #SZUKANIE REMINDEROW


                            if str(line3[0]) ==  str(line2[0]) and str(line3[1]) ==  str(line2[1]):
                                print(line3[0])
                                devlistbox.itemconfig(END, bg='Yellow')

                    else:
                        devlistbox.itemconfig(END, bg='Red')
                        x.status = 'NOK'
                    devlist.append(x)
                    break

            p += 1
        devlistbox.bind('<Double-Button>',devremdet)
        makemessage()




    def makemessage():
        textfield.delete('1.0', END)
        headerstr = """
To: 

Attn: 

From: Info Marine

Subject:  

Our ref.: 

Good day Sirs,

Please be so kind and inform us whether taking vibration measurements is possible and - if yes, when we can expect data for following equipment:
 
        """
        textfield.insert(INSERT, headerstr)

        reminderstr = """
TUBEDZIELISTAURZADZEN
        """
        textfield.insert(INSERT, reminderstr)

        header2str = """
Could you also perform measurements of machinery missing from three months survey:
        """
        textfield.insert(INSERT, header2str)
        devstr = ''
        for line in devlist:
            if str(line.status) == 'NOK':
                devstr += chr(10) + str('-') + str(line.name)

        textfield.insert(INSERT, devstr)

        textfield.pack(side=LEFT)













    remWindow = tk.Tk()
    remWindow.title("Reminder")
    devlist = list()
    Ownerlistbox = Listbox(remWindow)
    Ownerlistbox.config(width=0)
    Ownerlistbox.bind('<Double-Button>', getships)
    Shiplistbox = Listbox(remWindow)
    Shiplistbox.config(width=0)
    Shiplistbox.bind('<Double-Button>', getdevs)

    devlistbox = Listbox(remWindow)
    devlistbox.config(width=0)


    textfield = tk.Text(remWindow, width=100, height=60)

    querry = "select name,id from main where parent = 1 order by name"
    resultrr = q_run(connD, querry)
    for line in resultrr:
        Ownerlistbox.insert(END, line[0])




    Ownerlistbox.pack(side=LEFT, fill=BOTH)
    Shiplistbox.pack(side=LEFT, fill=BOTH)
    devlistbox.pack(side=LEFT, fill=BOTH)

    remWindow.mainloop()

remindershow()

