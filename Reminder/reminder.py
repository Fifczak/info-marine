import psycopg2
import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
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
            self.lastfullnumber = ''
            self.lastraportdate =''
            self.senddate = ''
            self.remcom = ''

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
            def datepick(ob):
                def print_sel():
                    ob.requestdate = str(cal.selection_get())
                    ob.dateLabel.configure(text=ob.requestdate)
                    root.destroy()
                root = Tk()
                root.title("Calendar")
                s = ttk.Style(root)
                s.theme_use('clam')
                top = tk.Toplevel(root)
                cal = Calendar(top,
                               font="Arial 14", selectmode='day',
                               cursor="hand1", year=2019, month=4, day=15)
                cal.pack(fill="both", expand=True)
                ttk.Button(top, text="ok", command=print_sel).pack()
                root.mainloop()


            w = evt.widget
            index = int(w.curselection()[0])
            detWindow = tk.Tk()
            detWindow.title("Reminder details")

            LabName = tk.Label(detWindow,text =str(devlist[index].name)).grid(column = 0, row = 0)
            LabId   = tk.Label(detWindow,text =str(devlist[index].id)).grid(column = 1, row = 0)
            LabLastRNL  = tk.Label(detWindow,text ="Last report:").grid(column = 0, row = 2)
            LabLastRN = tk.Label(detWindow, text= str(devlist[index].lastraport)).grid(column = 1, row = 2)

            LabLastRDateL  = tk.Label(detWindow,text ="Last date:" ).grid(column = 0, row = 3)
            LabLastRDate = tk.Label(detWindow,text = str(devlist[index].lastraportdate)).grid(column = 1, row = 3)

            SendDateL = tk.Label(detWindow, text="Send date:").grid(column = 0, row = 4)
            SendDate = tk.Label(detWindow, text=str(devlist[index].senddate))
            SendDate.bind('<Double-Button-1>', datepick)
            SendDate.grid(column=1, row=4)
            RequestDateL = tk.Label(detWindow, text="Request date:").grid(column = 0, row = 5)
            RequestDate = tk.Label(detWindow, text= str(devlist[index].requestdate)).grid(column = 1, row = 5)

            remtextfield = tk.Text(detWindow, width=20, height=20)
            remtextfield.insert(INSERT, str(devlist[index].remcom))
            remtextfield.grid(column=0, row=6, columnspan=2)





            detWindow.mainloop()



        devlistbox.delete(0, 'end')
        querry = "select id from main where name = '" + str(shipname)+ "'"
        parent = q_run(connD,querry)[0][0]

        ss = (q_run(connD, "select raport_number,min(date),max(date) from measurements_low where parent =" + str(
            parent) + " group by raport_number order by min desc"))

        for rep in ss:
            if len(rep[0]) == 9:
                lastfulldate = rep[1]
                lastfulldatemax = rep[2]
                break

        querry = "SELECT dss.id, CASE WHEN dss.id ~E'^\\\d+$' THEN	(select name from devices where cast(devices.id as text)\
             =  dss.id limit 1) ELSE (select id from ds_structure where id  =  dss.id limit 1) END as sortint, dss.sort FROM ds_structure\
              as dss where dss.parent = " + str(parent)
        results = q_run(connD, querry)


        querry = """
        
            select ml.id,ml.raport_number,min(ml.date),har.send_raport_koniec,rem.request_date, rem.remcom, rem.status
            from measurements_low as ml
            left join reminder as rem on ml.id = rem.id and ml.raport_number = rem.raport_number 
            left join harmonogram as har on ml.raport_number = har.report_number  
            where ml.parent = """ + str(parent) + """ 
            group by ml.id,ml.raport_number,rem.request_date,har.send_raport_koniec, rem.remcom, rem.status order by ml.id,ml.raport_number desc
                    
                    """

        resultr = q_run(connD, querry)


        ###################CROSSOWANIE TABELI REMINDER Z MEASUREMENTS_LOW
        querry =  """select rem.id, rem.raport_number, cast(har.send_raport_koniec as date)

            from reminder as rem
            left join harmonogram as har on rem.raport_number = har.report_number and rem.parent = har.shipid
            
            where parent = """ + str(parent) + """ and status is null"""
        remindertbl1 = q_run(connD, querry)


        querry = "Select id from measurements_low where parent = " + str(parent) + " and date > '" + str(lastfulldatemax) + "' group by id"
        newmeaslist = q_run(connD, querry)

        for item in remindertbl1:
            for item2 in newmeaslist:
                if item[0] == item2[0]:
                    querry = "UPDATE reminder set status = 2 where id = " + str(item[0]) + " and raport_number = '" + str(item[1]) + " '"
                    q_run(connD, querry)
                    print(querry)
                    break
        ######## ######## ######## ######## ######## ######## ########




        querry ="select id,raport_number from reminder where status is distinct from 2 and parent = " + str(parent)
        remindertbl = q_run(connD, querry)


        p = 0
        devlist.clear()
        for line in results:
            for line2 in resultr:
                fullrn = line2[1][:4] + '-' + line2[1][4:]
                if str(line[0]) == str(line2[0]):
                    x = device()
                    x.name = str(line[1])
                    x.id = str(line2[0])
                    x.lastraport = str(line2[1])
                    x.remcom = str(line2[5])
                    x.lastraportdate = datetime.datetime.strptime(str(line2[2]), '%Y-%m-%d').date()
                    sdate = str(line2[3])[:10]
                    if str(line2[3]) == "None":pass
                    else: x.senddate = datetime.datetime.strptime(str(sdate), '%Y-%m-%d').date()
                    if str(line2[4]) == "None": pass
                    else:x.requestdate = datetime.datetime.strptime(str(line2[4]), '%Y-%m-%d').date()
                    devlistbox.insert(END, results[p][1])



                    if x.lastraportdate >= lastfulldate:
                        devlistbox.itemconfig(END, bg='Green')
                        x.status = 'OK'
                        for line3 in remindertbl:   #SZUKANIE REMINDEROW
                            if str(line3[0]) ==  str(line2[0]) and str(line3[1]) ==  str(line2[1]):
                                x.status = 'REM'
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

        devstr = ''
        for line in devlist:
            if str(line.status) == 'REM':
                devstr += chr(10) + str('-') + str(line.name)
                ## UZUPEŁNIANIE REMCOM DO PRZEMYSLENIA
                # if str(line.remcom) != 'None':
                #     devstr += "(" + str(line.remcom) + ")"

        textfield.insert(INSERT, devstr)

        header2str = chr(10) + chr(10) + "Which was recommended to be controlled in our reports. "
        textfield.insert(INSERT, header2str)

        devlistnok = list()
        for line in devlist:
            if str(line.status) == 'NOK':
                devlistnok.append(line)
        print(len(devlistnok))
        if len(devlistnok) == 0:
            pass
        else:
            devstr = "Could you also perform measurements of machinery missing from three months survey:" + chr(10)
            for line in devlistnok:
                if str(line.status) == 'NOK':
                    devstr += chr(10) + str('-') + str(line.name)

        devstr += chr(10) + chr(10)
        textfield.insert(INSERT, devstr)


        header3str ="We hope to receive your response soon, thank you in advance. "
        textfield.insert(INSERT, header3str)

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

