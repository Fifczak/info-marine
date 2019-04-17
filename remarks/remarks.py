import psycopg2
import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
import csv
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

def LogApplication(root):
    var = IntVar()

    def makeWin():
        title = tk.Label(root, text="Info Datasheet")  # TITLE
        title.grid(row=0, column=2)
        user_entry_label = tk.Label(root, text="Username: ")  # USERNAME LABEL
        user_entry_label.grid(row=1, column=1)
        user_entry = tk.Entry(root, text="Username: ")  # USERNAME ENTRY BOX
        user_entry.grid(row=1, column=2)
        pass_entry_label = tk.Label(root, text="Password: ")  # PASSWORD LABEL
        pass_entry_label.grid(row=2, column=1)
        pass_entry = tk.Entry(root, show="*")  # PASSWORD ENTRY BOX
        pass_entry.grid(row=2, column=2)

        with open('log.csv') as csvfile:
            openfile = csv.reader(csvfile, delimiter=' ')
            p = -1
            for lines in openfile:
                p += 1
                if p == 0:
                    user_entry.insert(0, str(lines[0]))
                if p == 1:
                    pass_entry.insert(0, str(lines[0]))

        var = IntVar()
        checksave = tk.Checkbutton(root, text="Remember", variable=var)
        checksave.grid(row=3, column=2)
        sign_in_butt = Button(root, text="Sign In", command=lambda ue=user_entry, pe=pass_entry: logging_in(ue, pe))
        sign_in_butt.grid(row=5, column=2)

    def logging_in(user_entry, pass_entry):
        user_get = user_entry.get()  # Retrieve Username
        pass_get = pass_entry.get()  # Retrieve Password
        if bool(var.get()) == True:
            config = Path('log.csv')
            with open('log.csv', 'w', newline='') as csvfile:
                filewriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                filewriter.writerow([user_get])
                filewriter.writerow([pass_get])
        connD[0] = user_get
        connD[1] = pass_get
        querry = "SELECT current_user"
        try:
            usercheck = q_run(connD, querry)  # PYINSTALLER ma problemy gdzies tu

        except:
            pass
        if usercheck:
            root.destroy()
            # print(usercheck[0])
            querry = "select name,id from main where parent =1 order by name"
            ownerlist = q_run(connD, querry)

            querry = "select name,id,parent from main where parent <> 1 order by name"
            shiplist = q_run(connD, querry)

            remarks()

    makeWin(connD)

def remarks(connD):
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


root = tk.Tk()
root.title("Login")
root.geometry("200x120")
LogApplication(root)  # The frame is inside the widgit

root.mainloop()
#remindershow()

