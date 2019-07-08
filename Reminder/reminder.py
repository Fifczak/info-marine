import psycopg2
import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from tkinter.filedialog import askopenfilename
from tkinter import Tk
import csv
import matplotlib.pyplot as plt
import numpy as num
import tkinter as tkk
from tkinter import filedialog
from tqdm import tqdm



#connD=['testuser','info','192.168.10.243']
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
def column(matrix, i):
    return [row[i] for row in matrix]

class LogApplication:
	def __init__(self):
		self.root = Tk()
		self.root.title("Log In")
		self.title = tk.Label(self.root, text="Info Datasheet")  # TITLE
		self.title.grid(row=0, column=2)
		self.user_entry_label = tk.Label(self.root, text="Username: ")  # USERNAME LABEL
		self.user_entry_label.grid(row=1, column=1)
		self.user_entry = tk.Entry(self.root, text="Username: ")  # USERNAME ENTRY BOX
		self.user_entry.grid(row=1, column=2)
		self.pass_entry_label = tk.Label(self.root, text="Password: ")  # PASSWORD LABEL
		self.pass_entry_label.grid(row=2, column=1)
		self.pass_entry = tk.Entry(self.root, show="*")  # PASSWORD ENTRY BOX
		self.pass_entry.grid(row=2, column=2)
		try:
			with open('C:\overmind\\temp\log.csv') as csvfile:
				openfile = csv.reader(csvfile, delimiter=' ')
				p = -1
				for lines in openfile:
					p += 1
					if p == 0:
						self.user_entry.insert(0, str(lines[0]))
					if p == 1:
						self.pass_entry.insert(0, str(lines[0]))
		except:
			pass
		self.var = IntVar()
		self.checksave = tk.Checkbutton(self.root, text="Remember", variable=self.var)
		self.checksave.grid(row=3, column=2)
		self.sign_in_butt = Button(self.root, text="Sign In", command=lambda ue=self.user_entry, pe=self.pass_entry: self.logging_in(ue, pe))
		self.sign_in_butt.grid(row=5, column=2)
		self.root.mainloop()

	def logging_in(self,user_entry, pass_entry):
		user_get = user_entry.get()  # Retrieve Username
		pass_get = pass_entry.get()  # Retrieve Password
		if bool(self.var.get()) == True:
		   # config = Path('C:\overmind\\temp\log.csv')
			with open('C:\overmind\\temp\log.csv', 'w+' ,newline='') as csvfile:
				filewriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
				filewriter.writerow([user_get])
				filewriter.writerow([pass_get])
		connD = [user_get, pass_get, '192.168.10.243']


		querry = "SELECT current_user"
		usercheck = ''

		usercheck = q_run(connD, querry)  # PYINSTALLER ma problemy gdzies tu
		if usercheck != '':
			self.root.destroy()
			remindershow(connD)



def remindershow(connD):
    devlist = list()
    class device:
        def __init__(self):
            self.status =''
            self.remstatus = ''
            self.name = ''
            self.id = ''
            self.lastraport = ''
            self.lastfullnumber = ''
            self.lastraportdate =''
            self.senddate = ''
            self.requestdate =''
            self.remcom = ''

    class reminderwindow:
        def __init__(self):
            self.name =''
            self.lastfulldatemin = ''
            self.lastfulldatemax = ''
            self.parent = ''
            self.results = []
            self.resultr = []
            self.reminderharmo = list()
            def lastfulldate():
                ss = (
                    q_run(connD,
                          "select raport_number,min(date),max(date) from measurements_low where parent =" + str(
                              self.parent) + " group by raport_number order by min desc"))

                for rep in ss:
                    if len(rep[0]) == 9:
                        self.lastfulldatemin = rep[1]
                        self.lastfulldatemax = rep[2]
                        break

                lfd = [self.lastfulldatemin, self.lastfulldatemax]


                return lfd
            def preQuerrys():

                querry = "select id from main where name = '" + str(self.name) + "'"

                self.parent = q_run(connD, querry)[0][0]

                querry = "SELECT dss.id, CASE WHEN dss.id ~E'^\\\d+$' THEN	(select name from devices where cast(devices.id as text)\
                         =  dss.id limit 1) ELSE (select id from ds_structure where id  =  dss.id limit 1) END as sortint, dss.sort FROM ds_structure\
                          as dss where dss.parent = " + str(self.parent)
                self.results = q_run(connD, querry)

                querry = """

                        select ml.id,ml.raport_number,min(ml.date),har.send_raport_koniec,rem.request_date, rem.remcom, rem.status
                        from measurements_low as ml
                        left join reminder as rem on ml.id = rem.id and ml.raport_number = rem.raport_number 
                        left join harmonogram as har on ml.raport_number = har.report_number  
                        where ml.parent = """ + str(self.parent) + """ 
                        group by ml.id,ml.raport_number,rem.request_date,har.send_raport_koniec, rem.remcom, rem.status order by ml.id,ml.raport_number desc

                                """

                self.resultr = q_run(connD, querry)

                # answerQuerrys = [parent, results, resultr]
                # return answerQuerrys
            def dontsend(ID):
                def builddevlistlocal():
                    self.devlistbox.delete(0, 'end')
                    for item in devlist:
                        self.devlistbox.insert(END,str(item.name))

                        if str(item.id) == str(ID):
                            self.devlistbox.itemconfig(END, bg='Blue')
                            item.status = "W8"
                        elif str(item.status) == "OK":
                            self.devlistbox.itemconfig(END, bg='Green')
                        elif str(item.status) == "REM":
                            if str(item.remstatus) == '1':
                                self.devlistbox.itemconfig(END, bg='Orange')
                            else:
                                self.devlistbox.itemconfig(END, bg='Yellow')
                        elif str(item.status) == "NOK":
                            self.devlistbox.itemconfig(END, bg='Red')
                        elif str(item.status) == "W8":
                            self.devlistbox.itemconfig(END, bg='Blue')
                        elif str(item.status) == "UNDREM":
                            self.devlistbox.itemconfig(END, bg='Grey')

                builddevlistlocal()

                makemessage()
            def marksend():
                for item in devlist:
                    if item.status == 'REM':
                        teraz = str(datetime.datetime.now() )[:10]
                        querry = "UPDATE REMINDER SET STATUS = 1, send_date = '{}'" \
                                 " WHERE ID = '{}' AND raport_number = '{}'".format(teraz,str(item.id),str(item.lastraport) )

                        q_run(connD,querry)
            def getships(evt):
                w = evt.widget
                index = int(w.curselection()[0])
                shipname = w.get(index)
                makeships(shipname)
            def makeships(shnm):

                ColorShips(self.Shiplistbox, shnm)
            def getparent(shipname):
                self.parent = q_run(connD,"select id from main where name ='" + str(shipname) + "'" )[0][0]
            def getdevs(evt):
                w = evt.widget
                index = int(w.curselection()[0])

                self.name = w.get(index)
                getparent(str(self.name))
                makedevs("Y")
            def makedevs(check1):
                self.devlistbox.delete(0, 'end')
                if check1 == "Y":
                    last = lastfulldate()
                    self.lastfulldatemin = last[0]
                    self.lastfulldatemax = last[1]
                #     check_new_measurements() ### sprawdzanie przeniesione do wgrywania pomiarow
                querry = "select id,raport_number,status from reminder where status is distinct from 2 and parent = " + str(
                    self.parent)
                remindertbl = q_run(connD, querry)
                builddevlist(remindertbl)
                buildreportlist()
                makemessage()
            def setquaterly(evt):
                w = evt.widget
                index = int(w.curselection()[0])
                raportno = w.get(index)
                querry = "select raport_number,min(date),max(date) from measurements_low where raport_number ='" + str(
                    raportno) + "' group by raport_number order by min desc"
                dates = q_run(connD, querry)

                self.lastfulldatemin = dates[0][1]
                self.lastfulldatemax = dates[0][2]
                makedevs("N")
            def devremdet(evt):
                class details_window():
                    def __init__(self):
                        self.detWindow = tk.Tk()
                        self.detWindow.title("Reminder details")
                        self.LabName = tk.Label(self.detWindow, text=str(devlist[index].name)).grid(column=0, row=0)
                        self.LabId = tk.Label(self.detWindow, text=str(devlist[index].id)).grid(column=1, row=0)
                        self.id = str(devlist[index].id)
                        self.LabLastRNL = tk.Label(self.detWindow, text="Last report:").grid(column=0, row=2)
                        self.LabLastRN = tk.Label(self.detWindow, text=str(devlist[index].lastraport)).grid(
                            column=1,
                            row=2)
                        self.rn = str(devlist[index].lastraport)
                        self.LabLastRDateL = tk.Label(self.detWindow, text="Last date:").grid(column=0, row=3)
                        self.LabLastRDate = tk.Label(self.detWindow, text=str(devlist[index].lastraportdate)).grid(
                            column=1, row=3)

                        self.SendDateL = tk.Label(self.detWindow, text="Send date:").grid(column=0, row=4)
                        self.SendDate = tk.Label(self.detWindow, text=str(devlist[index].senddate))

                        self.SendDate.grid(column=1, row=4)
                        self.RequestDateL = tk.Label(self.detWindow, text="Request date:").grid(column=0, row=5)
                        self.RequestDate = tk.Label(self.detWindow, text=str(devlist[index].requestdate))
                        self.RequestDate.bind('<Double-Button-1>', lambda ID=str(devlist[index].id): self.datepick(ID))
                        self.RequestDate.grid(column=1,row=5)
                        self.var = IntVar()


                        self.sendbutton = tk.Button(self.detWindow, text='Dont Send',
                                                    command=lambda ID=str(devlist[index].id): dontsend(ID))
                        self.sendbutton.grid(column=0, row=6, columnspan=2)

                        self.remtextfield = tk.Text(self.detWindow, width=20, height=20)
                        self.remtextfield.insert(INSERT, str(devlist[index].remcom))
                        self.remtextfield.grid(column=0, row=7, columnspan=2)

                    def datepick(self,ob):
                        def print_sel():
                            ob.requestdate = str(cal.selection_get())
                            self.RequestDate.configure(text=ob.requestdate)
                            root.destroy()
                            querry = "UPDATE reminder set request_date = '" + str(ob.requestdate) + "' " \
                            "where raport_number = '" + str(self.rn) + "' and id = " + str(self.id)
                            q_run(connD,querry)
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
                W = details_window()
                W.detWindow.mainloop()
            def check_new_measurements():
                #przeniesione do wgrywania pomiarow

                ###################CROSSOWANIE TABELI REMINDER Z MEASUREMENTS_LOW
                querry = """select rem.id, rem.raport_number, cast(har.send_raport_koniec as date)

                         from reminder as rem
                         left join harmonogram as har on rem.raport_number = har.report_number and rem.parent = har.shipid

                         where parent = """ + str(self.parent) + """ and status is null"""
                remindertbl1 = q_run(connD, querry)

                querry = "Select id from measurements_low where parent = " + str(self.parent) + " and date > '" + str(
                    self.lastfulldatemax) + "' group by id"
                newmeaslist = q_run(connD, querry)

                for item in remindertbl1:
                    for item2 in newmeaslist:
                        if item[0] == item2[0]:
                            querry = "UPDATE reminder set status = 2 where id = " + str(
                                item[0]) + " and raport_number = '" + str(item[1]) + "'"
                            q_run(connD, querry)
                            break
                ######## ######## ######## ######## ######## ######## ########
            def buildreportlist():
                querry = "select raport_number from measurements_low where parent =(select id from main where name = '" + str(
                    self.name) + "' limit 1) group by raport_number order by raport_number desc"
                reportlist = q_run(connD, querry)
                self.Reportlistbox.delete(0, 'end')

                for line in reportlist:
                    self.Reportlistbox.insert(END, line[0])
            def builddevlist(remindertbl):

                preQuerrys()
                p = 0
                devlist.clear()
                for line in self.results:
                    for line2 in self.resultr:
                        fullrn = line2[1][:4] + '-' + line2[1][4:]
                        if str(line[0]) == str(line2[0]):
                            x = device()
                            x.name = str(line[1])
                            x.id = str(line2[0])
                            x.lastraport = str(line2[1])
                            x.remcom = str(line2[5])
                            x.lastraportdate = datetime.datetime.strptime(str(line2[2]), '%Y-%m-%d').date()
                            sdate = str(line2[3])[:10]
                            if str(line2[3]) == "None":
                                pass
                            else:
                                x.senddate = datetime.datetime.strptime(str(sdate), '%Y-%m-%d').date()
                            if str(line2[4]) == "None":
                                pass
                            else:
                                x.requestdate = datetime.datetime.strptime(str(line2[4]), '%Y-%m-%d').date()
                            self.devlistbox.insert(END, self.results[p][1])
                            if x.lastraportdate >= self.lastfulldatemin:
                                self.devlistbox.itemconfig(END, bg='Green')
                                x.status = 'OK'
                                for line3 in remindertbl:  # SZUKANIE REMINDEROW
                                    if str(line3[0]) == str(line2[0]) and str(line3[1]) == str(line2[1]):
                                        x.status = 'UNDREM'
                                        date = str(datetime.datetime.now() + datetime.timedelta(days=14))[:10]

                                        if x.requestdate < datetime.datetime.strptime(str(date), '%Y-%m-%d').date():
                                            x.status = 'REM'
                                            if str(line3[2]) == '1':
                                                x.remstatus = '1'
                                                self.devlistbox.itemconfig(END, bg='Orange')
                                            else:
                                                self.devlistbox.itemconfig(END, bg='Yellow')

                                        else:
                                            self.devlistbox.itemconfig(END, bg='Grey')

                            else:

                                self.devlistbox.itemconfig(END, bg='Red')
                                x.status = 'NOK'
                            devlist.append(x)
                            break

                    p += 1
                self.devlistbox.bind('<Double-Button>', devremdet)
            def makemessage():
                nextfull = self.lastfulldatemax + datetime.timedelta(days=90)
                teraz = datetime.datetime.now().date()
                delay = datetime.timedelta(days=14)
                request = teraz + delay
                print(nextfull,'<',request)


                if nextfull < request:
                    self.textfield.delete('1.0', END)
                    headerstr = """
To: 

Attn: 

From: Info Marine

Subject:  

Our ref.: 

Dear Sirs,
In accordance to three month measurement period time, please be so kind and inform us whether taking vibration measurements of whole machinery is possible and - if yes, when we can expect data?
We hope to receive your response soon, thank you in advance.
                                        """
                    self.textfield.insert(INSERT, headerstr)
                else:
                    self.textfield.delete('1.0', END)
                    headerstr = """
To: 

Attn: 

From: Info Marine

Subject:  

Our ref.: 

Good day Sirs,

Please be so kind and inform us whether taking vibration measurements is possible and - if yes, when we can expect data for following equipment:
    
                        """
                    self.textfield.insert(INSERT, headerstr)
                    devstr = ''

                    for line in devlist:

                        if str(line.status) == 'REM':

                            devstr += chr(10) + str('-') + str(line.name)
                            ## UZUPEŁNIANIE REMCOM DO PRZEMYSLENIA
                            # if str(line.remcom) != 'None':
                            #     devstr += "(" + str(line.remcom) + ")"
                    self.textfield.insert(INSERT, devstr)
                    devstr = ""
                    header2str = chr(10) + chr(10) + "Which was recommended to be controlled in our reports. "
                    self.textfield.insert(INSERT, header2str)
                    devlistnok = list()
                    for line in devlist:
                        if str(line.status) == 'NOK':
                            devlistnok.append(line)
                    if len(devlistnok) == 0:
                        pass
                    else:
                        devstr = "Could you also perform measurements of machinery missing from three months survey:" + chr(
                            10)
                        for line in devlistnok:
                            if str(line.status) == 'NOK':
                                devstr += chr(10) + str('-') + str(line.name)
                    devstr += chr(10) + chr(10)
                    self.textfield.insert(INSERT, devstr)
                    header3str = "We hope to receive your response soon, thank you in advance. "
                    self.textfield.insert(INSERT, header3str)
                self.sendbutton.pack(side=TOP)
                self.textfield.pack(side=LEFT)
            def ReminderQuerrys():
                querry = """select main2.name, main.name,remi.parent,max(remi.send_date)as send,min(remi.request_date) as request
                            from reminder remi
                            left join main on remi.parent = main.id
                            left join main main2 on main.parent = main2.id
                            where remi.status is distinct from 2 and remi.send_date is not null
                            group by main2.name,  main.name,remi.parent"""
                self.reminderharmo = q_run(connD, querry)
                querry = """select main2.name, max(remi.send_date)as send,min(remi.request_date) as request,remi.parent 
                            from reminder remi
                            left join main on remi.parent = main.id
                            left join main main2 on main.parent = main2.id
                            where remi.status is distinct from 2 and remi.send_date is not null
                            group by main2.name,remi.parent 
							order by main2.name"""
                self.reminderownerharmo = q_run(connD, querry)
                querry = "select name,id from main where parent = 1 order by name"
                self.resultrr = q_run(connD, querry)
            def ColorOwners(object):
                ReminderQuerrys()
                try:
                    print(self.lastfulldatemax)
                    nextfull = datetime.datetime.strptime(str(self.lastfulldatemax), '%y-%m-%d').date() + datetime.timedelta(days=90)
                except:
                    nextfull =datetime.datetime.now().date()
                teraz = datetime.datetime.now().date()
                delay = datetime.timedelta(days=14)
                request = teraz + delay
                delay2 = datetime.timedelta(days=7)
                lastsend = teraz - delay2

                for line in tqdm(self.resultrr):
                    object.insert(END, line[0])
                    for line2 in self.reminderownerharmo:
                        if line[0] == line2[0]:
                            object.itemconfig(END, bg='grey')
                            self.parent = line2[3]
                            #print(self.parent)
                            self.lastfulldatemax = lastfulldate()[0]
                            nextfull = self.lastfulldatemax + datetime.timedelta(days=90)

                            if nextfull < request:
                                    object.itemconfig(END, bg='red')
                                    continue
                            if line2[2] < request: #jeśli jest request_date mniejsza niz dzis + 2 tygodnie
                                object.itemconfig(END, bg='yellow')

                                if line2[1] > lastsend: #jeśli wysłano w przeciągu zeszłego tygodnia
                                    object.itemconfig(END, bg='orange')
                                    break

            def ColorShips(object,shnm):


                teraz = datetime.datetime.now().date()
                delay = datetime.timedelta(days=14)
                request = teraz + delay
                delay2 = datetime.timedelta(days=7)
                lastsend = teraz - delay2
                querry = "select name from main where parent =(select id from main where name = '" + str(
                    shnm) + "' limit 1) order by name"
                ships = q_run(connD, querry)
                object.delete(0, 'end')
                for line in ships:
                    object.insert(END, line[0])
                    for line2 in self.reminderharmo:
                        if line[0] == line2[1]:
                            object.itemconfig(END, bg='grey')
                            self.parent = line2[2]
                            self.lastfulldatemax= lastfulldate()[0]
                            nextfull = self.lastfulldatemax + datetime.timedelta(days=90)
                            if line2[4] < request: #jeśli jest request_date mniejsza niz dzis + 2 tygodnie
                                object.itemconfig(END, bg='yellow')
                                if nextfull < request:
                                    object.itemconfig(END, bg='red')
                                if line2[3] > lastsend: #jeśli wysłano w przeciągu zeszłego tygodnia
                                    object.itemconfig(END, bg='orange')
                                    break
            self.remWindow = tk.Tk()
            self.remWindow.title("Reminder")
            self.Ownerlistbox = Listbox(self.remWindow, exportselection=False)
            self.Ownerlistbox.config(width=0)
            self.Ownerlistbox.bind('<Double-Button>', getships)
            self.Shiplistbox = Listbox(self.remWindow, exportselection=False)
            self.Shiplistbox.config(width=0)
            self.Shiplistbox.bind('<Double-Button>', getdevs)
            self.Reportlistbox = Listbox(self.remWindow, exportselection=False)
            self.Reportlistbox.config(width=0)
            self.Reportlistbox.bind('<Double-Button>', setquaterly)
            self.devlistbox = Listbox(self.remWindow)
            self.devlistbox.config(width=0)
            self.sendbutton = tk.Button(text='Send', command = marksend)
            self.textfield = tk.Text(self.remWindow, width=100, height=60)


            ColorOwners(self.Ownerlistbox)


            self.Ownerlistbox.pack(side=LEFT, fill=BOTH)
            self.Shiplistbox.pack(side=LEFT, fill=BOTH)
            self.devlistbox.pack(side=LEFT, fill=BOTH)
            self.Reportlistbox.pack(side=LEFT, fill=BOTH)
            self.remWindow.mainloop()



    reminderwindow()


LogApplication()

