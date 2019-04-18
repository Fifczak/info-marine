import psycopg2
import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
import csv
from tkinter.filedialog import askopenfilename
from tkinter import Tk
from tkcalendar import Calendar, DateEntry
import matplotlib.pyplot as plt
import numpy as num
import tkinter as tkk
from tkinter import filedialog


connD=['testuser','info','192.168.8.125']

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

	querry = "select name,id from main where parent = 1 order by name"
	resultr = q_run(connD, querry)

	def datepick(ob):
		if str(ob.var2.get()) == '0':
				ob.dateLabel.configure(text='')
		if str(ob.var2.get()) == '1':
			def print_sel():
				ob.requestdate =  str(cal.selection_get())
				ob.dateLabel.configure(text=ob.requestdate)
				root.destroy()
			root = Tk()
			root.title("Calendar")
			#s = ttk.Style(root)
			#s.theme_use('clam')
			top = tk.Toplevel(root)

			cal = Calendar(top,
						   font="Arial 14", selectmode='day',
						   cursor="hand1", year=2019, month=4, day=15)
			cal.pack(fill="both", expand=True)
			ttk.Button(top, text="ok", command=print_sel).pack()
			root.mainloop()

	#


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
		querry = "(select id from main where name = '" + str(shipname) +"' limit 1)"
		parent = str(q_run(connD,querry)[0][0])
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
			self.parent =dev[2]
			self.nameLabel = tk.Label(measCframe,text= self.name)
			self.nameLabel.pack(side = LEFT)
			self.textfield = tk.Text(measCframe, width=50, height=2)
			self.textfield.pack(side=LEFT)

			self.var = tk.IntVar(value=0)
			self.check = ttk.Checkbutton(measCframe, text='Sent', variable=self.var)
			self.check.pack(side=LEFT)
			self.var2 = tk.IntVar(value=0)
			self.check2 = ttk.Checkbutton(measCframe, text='Reminder', variable=self.var2,command = lambda remO = self: datepick(remO))
			self.check2.pack(side=LEFT)
			measCframe.pack(side=TOP, fill=BOTH, expand=True)

			self.dateLabel = tk.Label(measCframe,text= "")
			self.dateLabel.pack(side = LEFT)

			self.requestdate = ''
			self.datevar = tk.StringVarVarvalue="2000-01-01"

			#command = lambda ue=user_entry, pe=pass_entry: logging_in(ue, pe)

	def putdevices(report):
		def upload():
			c=0
			for line in remlist:
				if line.textfield.get("1.0", END).strip() != '':
					querry = "select date from measurements_low where id = " + str(
						line.id) + " and raport_number = '" + str(line.rn) + "' limit 1"

					measdate = str(q_run(connD, querry)[0][0])

					if line.var.get() == 1: sendflag = 'True'
					else: sendflag = 'False'
					if line.var2.get() == 1: remflag = 'True'
					else: remflag = 'False'
					querry = "INSERT INTO REMARKS(id,raport_number,remark,parent,documentdate,sended,reminder) VALUES (" + str(
						line.id) + ",'" + str(line.rn) + "','" + str(
						(line.textfield.get("1.0", END)).strip()) + "'," + str(line.parent) + ",'" + str(
						measdate) +"'," + str(sendflag) + "," + str(remflag) + ")"
					q_run(connD, querry)


					if remflag == 'True':
						querry = "INSERT INTO REMINDER(parent,raport_number,request_date,remcom,id) VALUES (" + str(
							line.parent) + ",'" + str(line.rn) + "','" + str(
							line.requestdate) + "','" + str(line.textfield.get("1.0", END)).strip() + "'," + str(
							line.id) + ")"
						q_run(connD, querry)




					c+=1
			messagebox.showinfo("Title", 'Upload done: ' + str(c))

		querry = """select dev.name ,ml.id,ml.parent
			from measurements_low as ml 
			left join (select parent,sort, cast(id as int) as id from ds_structure where id ~E'^\\\d+$') as dss on ml.id =dss.id
			left join devices as dev on ml.id =dev.id
			where ml.raport_number = '""" + str(report) + """' 
				group by ml.id,dss.sort,dev.name,ml.parent
				order by dss.sort"""
		try:
			for widget in MASTERmeasframe.winfo_children():
				widget.destroy()
		except:
			pass

		MASTERmeasframe.pack(side=TOP, anchor=S, fill=BOTH)



		devices = q_run(connD, querry)
		header = ttk.Frame(MASTERmeasframe)
		body = ttk.Frame(MASTERmeasframe, width=1000,height = 1000)
		header.pack()
		body.pack(fill=BOTH)
		UploadButton = Button(header, text='Upload and refresh', command=upload)
		UploadButton.pack()
		GetReportButton = Button(header, text='Get report')#, command=upload)
		GetReportButton.pack()



		try:
			querry = "Select send_raport_koniec from harmonogram where report_number = '" + str(report) + "'"
			senddate = q_run(connD, querry)[0][0]
			senddate = str(senddate)[:10]
			if senddate == 'None':senddate = 'no date in harmonogram'
		except:
			senddate = 'no date in harmonogram'

		ttk.Label(header, text="Send date: " + str(senddate)).pack()
		scrollable_body = Scrollable(body, width=32)
		remlist = list()
		for i in devices:
			measCframe = tk.Frame(scrollable_body, height=2, width=32)
			X = frame_reminder(measCframe,i,report)
			remlist.append(X)
		scrollable_body.update()

	remarksWindow = tk.Tk()
	remarksWindow.title("Remarks")
	parent = 1
	MASTERmeasframe = Frame(remarksWindow, width=600,height = 600)
	Ownerlistbox = Listbox(remarksWindow)
	Ownerlistbox.config(width=0)
	Ownerlistbox.bind('<Double-Button>', getships)
	Shiplistbox = Listbox(remarksWindow)
	Shiplistbox.config(width=0)
	Shiplistbox.bind('<Double-Button>', getreports)
	Reportlistbox = Listbox(remarksWindow)
	Reportlistbox.config(width=0)
	Reportlistbox.bind('<Double-Button>', getdevices)





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

#remindershow()

