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
import tkinter as tk
from tkinter import ttk

class Scrollable(ttk.Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame,
       call the update() method to refresh the scrollable area.
    """

    def __init__(self, frame, width=16):

        scrollbar = tk.Scrollbar(frame, width=width)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        tk.Frame.__init__(self, frame)

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tk.NW)


    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas width"

        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width = canvas_width)

    def update(self):
        "Update the canvas and the scrollregion"

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))


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

			remarks(connD)

	makeWin()

def remarks(connD):
	class device:
		def __init__(self):
			self.lastraport = ''
			self.requestdate = ''
			self.lastraportdate =''

	parent = 79
	querry = "SELECT dss.id, CASE WHEN dss.id ~E'^\\\d+$' THEN	(select name from devices where cast(devices.id as text)\
	  =  dss.id limit 1) ELSE (select id from ds_structure where id  =  dss.id limit 1) END as sortint, dss.sort FROM ds_structure\
	   as dss where dss.parent = " + str(parent)
	results = q_run(connD, querry)

	querry = "select name,id from main where parent = 1 order by name"
	resultr = q_run(connD, querry)





	def getships(evt):
		w = evt.widget
		index = int(w.curselection()[0])
		shipname = w.get(index)
		makeships(shipname)

	def makeships(shipname):
		querry = "select name from main where parent =(select id from main where name = '" + str(shipname) +"' limit 1) order by name"
		ships = q_run(connD,querry)
		Shiplistbox.delete(0,'end')

		for line in ships:
			Shiplistbox.insert(END, line[0])

	def getreports(evt):
		w = evt.widget
		index = int(w.curselection()[0])
		shipname = w.get(index)
		makereports(shipname)

	def makereports(shipname):
		querry = "select raport_number from measurements_low where parent = (select id from main where name = '" + str(shipname) +"' limit 1) group by raport_number order by raport_number DESC"
		reports = q_run(connD,querry)
		Reportlistbox.delete(0,'end')

		for line in reports:
			Reportlistbox.insert(END, line[0])

	def getdevices(evt):
		w = evt.widget
		index = int(w.curselection()[0])
		report = w.get(index)
		putdevices(report)

	class frame_reminder:
		def __init__(self, measCframe,dev,rn):
			self.rn = rn
			self.id = dev[1]
			self.name = dev[0]
			self.nameLabel = tk.Label(measCframe,text= self.name)
			self.nameLabel.pack(side = LEFT)
			self.textfield = tk.Text(measCframe, width=50, height=2)
			self.textfield.pack(side=LEFT)

			self.var = tk.IntVar(value=0)
			self.check = ttk.Checkbutton(measCframe, text='Sent', variable=self.var)
			self.check.pack(side=LEFT)
			self.var2 = tk.IntVar(value=0)
			self.check2 = ttk.Checkbutton(measCframe, text='Reminder', variable=self.var2)
			self.check2.pack(side=LEFT)
			measCframe.grid()
	def putdevices(report):
		querry = """select dev.name ,ml.id
			from measurements_low as ml 
			left join (select parent,sort, cast(id as int) as id from ds_structure where id ~E'^\\\d+$') as dss on ml.id =dss.id
			left join devices as dev on ml.id =dev.id
			where ml.raport_number = '""" + str(report) + """' 
				group by ml.id,dss.sort,dev.name
				order by dss.sort"""


		devices = q_run(connD, querry)

		try:
			for widget in measBframe.winfo_children():
				widget.destroy()
		except:
			pass

		MASTERmeasframe.pack(side=TOP, anchor=S)
		# measBframe.config(yscrollcommand=scrollbar.set)
		measBframe.pack(side=TOP)
		scrollable_body = Scrollable(measBframe, width=32)


		UploadButton = Button(MASTERmeasframe, text='Upload and refresh')#, command=upload)
		UploadButton.pack()
		remlist = list()
		for i in devices:
			measCframe = tk.Frame(measBframe, height=2, bd=1)
			X = frame_reminder(measCframe,i,report)
			remlist.append(X)

		scrollable_body.update()
	remarksWindow = tk.Tk()
	remarksWindow.title("Reminder")

	Ownerlistbox = Listbox(remarksWindow)
	Ownerlistbox.config(width=0)
	Ownerlistbox.bind('<Double-Button>', getships)
	Shiplistbox = Listbox(remarksWindow)
	Shiplistbox.config(width=0)
	Shiplistbox.bind('<Double-Button>', getreports)
	Reportlistbox = Listbox(remarksWindow)
	Reportlistbox.config(width=0)
	Reportlistbox.bind('<Double-Button>', getdevices)




	MASTERmeasframe = Frame(remarksWindow, width=300, height=300)
	measBframe = Canvas(MASTERmeasframe)  # ,yscrollcommand=rapmeasscrol.set,scrollregion=(0,0,500,500))





	p=0
	devlist = list()
	for line in resultr:
		Ownerlistbox.insert(END, line[0])
		p+=1



	Ownerlistbox.pack(side=LEFT, fill=BOTH)
	Shiplistbox.pack(side=LEFT, fill=BOTH)
	Reportlistbox.pack(side=LEFT, fill=BOTH)
	remarksWindow.mainloop()


# root = tk.Tk()
# root.title("Login")
# root.geometry("200x120")
# LogApplication(root)  # The frame is inside the widgit
remarks(connD)
#root.mainloop()
#remindershow()

