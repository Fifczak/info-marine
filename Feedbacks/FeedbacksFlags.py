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
import pandas.io.sql as sqlio
import pandas as pd


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
			feedbackswindow(connD)

class feedbackswindow:
	def __init__(self,connD):
		self.connD = connD
		self. conn = psycopg2.connect(
			"host='{}' port={} dbname='{}' user={} password={}".format(connD[2], '5432', 'postgres', connD[0], connD[1]))
		self.getquerry()
		self.drawwindow()
	def getquerry(self):
		querry = """
		select dev.id,main.name as shipname, dev.name as devname,fdb.raport_number, rem.remark, rem.sended,
		fdb.feedback, fdb.fdbflag, fdb.costflag, fdb.price, fdb.low, fdb.high, dss.sort,
		 rem._id_ as remid, fdb._id_ as fdbid
		from feedbacks fdb
		left join remarks rem on fdb.id = rem.id and fdb.raport_number = rem.raport_number
		left join devices dev on fdb.id = dev.id
		left join ds_structure dss on cast(dev.id as text) = dss.id
		left join main on dev.parent = main.id
		order by fdb.raport_number
		"""
		self.fdbdFrame = sqlio.read_sql_query(querry, self.conn)
		self.fdbdFrame['fdbflag'] = pd.Series(self.fdbdFrame['fdbflag'], dtype='Int64').fillna(0)
		self.fdbdFrame['costflag'] = pd.Series(self.fdbdFrame['costflag'], dtype='Int64').fillna(0)
		self.presentfeedbacks = self.fdbdFrame

	def drawwindow(self):
		self.root = tk.Tk()
		self.root.title('Feedbacker')

		self.listframe = tk.Frame(self.root)
		self.fdbframe = tk.Frame(self.root)

		self.listfilterframe = tk.Frame(self.listframe)
		self.feedbacklist = tk.Listbox(self.listframe, width=0)
		self.makefilterwindow(self.listfilterframe)

		self.fillfdblist(self.presentfeedbacks)

		self.listframe.pack(side=LEFT, fill=Y)
		self.fdbframe.pack(side=LEFT, fill=Y)

		self.listfilterframe.pack(side=TOP)
		self.feedbacklist.pack(side=TOP, fill=Y, expand=1)

		self.root.mainloop()
	def fillfdblist(self, fdbdfr):
		self.feedbacklist.delete(0, 'end')
		dflisted = fdbdfr.values.tolist()
		for row in dflisted:
			liststring = (row[1], row[3], row[2])
			self.feedbacklist.insert(0, liststring)
	def makefilterwindow(self, frame):
		def boxtypechange(evt):
			getdetvalues(self.filterlisboxtype.get())

		def getdetvalues(filtertype):
			# print(str(filtertype))
			detlist = list()
			if str(filtertype) == 'None':
				detlist = ['All']
			elif str(filtertype) == 'Ship':
				querry = "select name from main where id in (select parent from feedbacks group by parent) order by name"
				detlist = column(list(q_run(self.connD, querry)), 0)
			elif str(filtertype) == 'Report':
				querry = "select raport_number from feedbacks group by raport_number order by raport_number desc"
				detlist = column(list(q_run(self.connD, querry)), 0)
			elif str(filtertype) == 'Fdb flag':
				querry = "select flagstr,lp from fdbflags order by lp"
				for item in list(q_run(self.connD, querry)):
					detlist.append('({}){}'.format(item[1], item[0]))

			elif str(filtertype) == 'Cost flag':
				querry = "select flagstr,lp from costflags order by lp"
				for item in list(q_run(self.connD, querry)):
					detlist.append('({}){}'.format(item[1], item[0]))
			elif str(filtertype) == 'Missing':
				detlist = ['no kW', 'no TYPE', 'NO COST CASE']
			self.filterlisboxdet.config(values=detlist)
			self.filterlisboxdet.current(0)

		def boxdetailchange(evt):
			filterdframe(self.filterlisboxtype.get(), self.filterlisboxdet.get())

		def filterdframe(filtertype, filterdet):
			if str(filtertype) == 'None':
				self.presentfeedbacks = self.fdbdFrame
			elif str(filtertype) == 'Ship':
				self.presentfeedbacks = self.fdbdFrame[self.fdbdFrame.shipname == str(filterdet)]
			elif str(filtertype) == 'Report':
				self.presentfeedbacks = self.fdbdFrame[self.fdbdFrame.raport_number == str(filterdet)]
			elif str(filtertype) == 'Fdb flag':
				filterby = str(filterdet)[filterdet.index('(') + 1:filterdet.index(')')]
				self.presentfeedbacks = self.fdbdFrame[self.fdbdFrame.fdbflag == int(filterby)]
			elif str(filtertype) == 'Cost flag':
				filterby = str(filterdet)[filterdet.index('(') + 1:filterdet.index(')')]
				self.presentfeedbacks = self.fdbdFrame[self.fdbdFrame.fdbflag == int(filterby)]
			elif str(filtertype) == 'Missing':
				self.presentfeedbacks = self.fdbdFrame[
					self.fdbdFrame['price'].astype(str).str.contains(filterdet) == True]

			self.fillfdblist(self.presentfeedbacks)

		def sortchange(evt):
			sortby(self.sortlist.get())

		def sortby(filterby):
			print(filterby)
			if filterby == 'Ship':
				filterby = 'shipname'
			elif filterby == 'Device':
				filterby = 'devname'
			elif filterby == 'Structure':
				filterby = 'sort'
			elif filterby == 'Report':
				filterby = 'raport_number'
			elif filterby == 'Fdb flag':
				filterby = 'fdbflag'
			elif filterby == 'Cost flag':
				filterby = 'costflag'
			print(filterby)
			self.presentfeedbacks = self.presentfeedbacks.sort_values(by=[filterby])
			self.fillfdblist(self.presentfeedbacks)

		self.label1 = tk.Label(frame, text='Filter by: ')
		self.filterlisboxtype = ttk.Combobox(frame, text="",
											 values=["None", "Ship", "Report", "Fdb flag", "Cost flag", "Missing"],
											 state="readonly")
		self.filterlisboxtype.bind('<<ComboboxSelected>>', boxtypechange)
		self.filterlisboxdet = ttk.Combobox(frame, text="", state="readonly")
		self.filterlisboxdet.bind('<<ComboboxSelected>>', boxdetailchange)

		self.label2 = tk.Label(frame, text='Sort by: ')
		self.sortlist = ttk.Combobox(frame, width=10,
									 values=['Ship', 'Device', 'Structure', 'Report', 'Fdb flag', 'Cost flag'],
									 state="readonly")
		self.sortlist.bind('<<ComboboxSelected>>', sortchange)

		self.label1.grid(row=0, column=0)
		self.filterlisboxtype.grid(row=0, column=1)
		self.filterlisboxdet.grid(row=0, column=2)
		self.label2.grid(row=1, column=0)
		self.sortlist.grid(row=1, column=1)


if __name__ == '__main__' :
	LogApplication()