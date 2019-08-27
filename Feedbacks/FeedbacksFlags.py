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



#connD=['testuser','info','localhost']
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
			"host='{}' port={} dbname='{}' user={} password={}".format(self.connD[2], '5432', 'postgres', self.connD[0], self.connD[1]))
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

		querry = "select lp,flagstr from fdbflags"
		self.fdbflagz = list()
		self.fdbflagz.append(('0', 'No flag'))
		for item in (list(q_run(self.connD, querry))):
			self.fdbflagz.append(item)

		querry = "select lp,flagstr from costflags"
		self.costflagz = list()
		self.costflagz.append(['0', 'No flag'])
		for item in (list(q_run(self.connD, querry))):
			self.costflagz.append(item)

	def fillfdblist(self, fdbdfr):
		self.feedbacklist.delete(0, 'end')
		dflisted = fdbdfr.values.tolist()
		for row in dflisted:
			liststring = (row[1], row[3], row[2])
			self.feedbacklist.insert(END, liststring)

	def drawwindow(self):
		def changefeedbackwindow(evt):
			dflisted = self.presentfeedbacks.values.tolist()
			self.updatefeedbackwindows(dflisted[self.feedbacklist.curselection()[0]])

		self.root = tk.Tk()
		self.root.title('Feedbacker')

		self.listframe = tk.Frame(self.root)
		self.fdbframe = tk.Frame(self.root)

		self.listfilterframe = tk.Frame(self.listframe)
		self.feedbacklist = tk.Listbox(self.listframe, width=0, exportselection=False)
		self.feedbacklist.bind('<<ListboxSelect>>', changefeedbackwindow)
		self.makefilterwindow(self.listfilterframe)
		self.fillfdblist(self.presentfeedbacks)

		self.makefeedbackwindow(self.fdbframe)

		self.listframe.pack(side=LEFT, fill=Y)
		self.fdbframe.pack(side=LEFT, fill=Y)

		self.listfilterframe.pack(side=TOP)
		self.feedbacklist.pack(side=TOP, fill=Y, expand=1)

		self.root.mainloop()



	def filterdframe(self,filtertype, filterdet):
		if str(filtertype) == 'None':
			self.presentfeedbacks = self.fdbdFrame
		elif str(filtertype) == 'Ship':
			self.presentfeedbacks = self.fdbdFrame[self.fdbdFrame.shipname == str(filterdet)]
		elif str(filtertype) == 'Report':
			self.presentfeedbacks = self.fdbdFrame[self.fdbdFrame.raport_number == str(filterdet)]
		elif str(filtertype) == 'Fdb flag':
			filterby = str(filterdet)[filterdet.index('(') + 1:filterdet.index(')')]
			if int(filterby) == 0:
				self.presentfeedbacks = self.fdbdFrame.loc[ \
					(self.fdbdFrame.fdbflag == int(filterby)) | \
					(pd.isnull(self.fdbdFrame.fdbflag))]
			else:
				self.presentfeedbacks = self.fdbdFrame.loc[self.fdbdFrame.fdbflag == int(filterby)]

		elif str(filtertype) == 'Cost flag':
			filterby = str(filterdet)[filterdet.index('(') + 1:filterdet.index(')')]
			if int(filterby) == 0:
				self.presentfeedbacks = self.fdbdFrame.loc[ \
					(self.fdbdFrame.costflag == int(filterby)) | \
					(pd.isnull(self.fdbdFrame.costflag))]
			else:
				self.presentfeedbacks = self.fdbdFrame.loc[self.fdbdFrame.costflag == int(filterby)]
		elif str(filtertype) == 'Cost calc. missing':
			self.presentfeedbacks = self.fdbdFrame.loc[
				self.fdbdFrame['price'].astype(str).str.contains(filterdet) == True]

		self.fillfdblist(self.presentfeedbacks)

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
				detlist = (column(list(q_run(self.connD, querry)), 0))
			elif str(filtertype) == 'Fdb flag':
				querry = "select flagstr,lp from fdbflags order by lp"
				detlist.append("(0)None")
				for item in list(q_run(self.connD, querry)):
					detlist.append('({}){}'.format(item[1], item[0]))
			elif str(filtertype) == 'Cost flag':
				querry = "select flagstr,lp from costflags order by lp"
				detlist.append("(0)None")
				for item in list(q_run(self.connD, querry)):
					detlist.append('({}){}'.format(item[1], item[0]))
			elif str(filtertype) == 'Missing':
				detlist = ['no kW', 'no TYPE', 'NO COST CASE']
			self.filterlisboxdet.config(values=detlist)
			self.filterlisboxdet.current(0)
		def boxdetailchange(evt):
			self.filterdframe(self.filterlisboxtype.get(), self.filterlisboxdet.get())

		def sortchange(evt):
			sortby(self.sortlist.get())
		def sortby(filterby):
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

	def updatefeedbackwindows(self, fdbstrip):
		def updateheadlabel(fdbstrip):
			headtext = """
	Ship: {}
	Device: {}
	Report: {}
	        """.format(fdbstrip[1], fdbstrip[2], fdbstrip[3])
			self.labelhead.config(text=headtext)

			self.remarktext.configure(state='normal')
			self.fdbtext.configure(state='normal')

			self.remarktext.delete('1.0', END)
			try:
				self.remarktext.insert(END, fdbstrip[4])
			except:
				self.remarktext.insert(END, '#ERROR: MISSING REMARK IN DB')
			self.fdbtext.delete('1.0', END)
			self.fdbtext.insert(END, fdbstrip[6])
			self.fdbflagstring.current(fdbstrip[7])
			self.costflagstring.current(fdbstrip[8])

			self.remarktext.configure(state='disabled')
			self.fdbtext.configure(state='disabled')

			self.pricetext.delete('1.0', END)
			self.priceval.delete('1.0', END)
			if str(fdbstrip[9]) != 'None':
				self.pricetext.insert(END, fdbstrip[9][0])
				self.priceval.insert(END, fdbstrip[9][1])

			self.lowtext.delete('1.0', END)
			self.lowval.delete('1.0', END)
			if str(fdbstrip[10]) != 'None':
				self.lowtext.insert(END, fdbstrip[10][0])
				self.lowval.insert(END, fdbstrip[10][1])

			self.hightext.delete('1.0', END)
			self.highval.delete('1.0', END)
			if str(fdbstrip[11]) != 'None':
				self.hightext.insert(END, fdbstrip[11][0])
				self.highval.insert(END, fdbstrip[11][1])

		updateheadlabel(fdbstrip)

	def makefeedbackwindow(self, frame):
		def setflags():
			def loadcost():
				devid = (list(self.presentfeedbacks.loc[self.presentfeedbacks.fdbid == _id_, 'id'])[0])
				querry = 'select kw,type from devices where id = {}'.format(devid)
				devkw, devtype = list(q_run(self.connD, querry))[0]

				querry = "select costflag,typ, kwrange[1],kwrange[2], price[1],price[2], low[1],low[2] , high[1],high[2]from costcases"
				costcases = list(q_run(self.connD, querry))
				for case in costcases: #iteracja po costcase
					devcostflag = list(self.presentfeedbacks.loc[self.presentfeedbacks.fdbid == _id_,'costflag'])
					if costflag== 0:
						pricestr = ''
						priceval = ''
						lowstr = ''
						lowval = ''
						highstr = ''
						highval = ''
						querry = "update feedbacks set price = null, low = null, high = null where _id_ = {}".format(str(_id_))
						break
					elif len(devtype) == 0:
						pricestr = 'no TYPE'
						priceval = '?'
						lowstr = 'no TYPE'
						lowval = '?'
						highstr = 'no TYPE'
						highval = '?'
						querry = "update feedbacks set " \
								 "price[0] = '{}', price[1] = '{}', " \
								 "low[0] ='{}', low[1] = '{}', " \
								"high[0] = '{}', high[1] ='{}' " \
								"where _id_ ={}".format(pricestr,priceval,lowstr,lowval,highstr,highval,_id_)




					elif self.costflagstring.current() in column(costcases,0): #jest flaga w bazie
						if  str(self.costflagstring.current()) == str(case[0]): #flaga sie zgadza
							if str(devtype).strip() == str(case[1]).strip(): # tutaj typ
								#TODO: ZROBIC WSTAWIANIE NO TYPE ITP ITD
								kw = (re.findall(r'\d+\.*\d*', str(devkw))[0])
								if (float(kw) >= float(case[2]) and float(kw) <= float(case[3])) or (case[2] == 0 and case[3] == 0):
									pricestr = case[4]
									priceval = case[5]
									lowstr = case[6]
									lowval = case[7]
									highstr = case[8]
									highval = case[9]
									querry = "update feedbacks set " \
											 "price[0] = '{}', price[1] = '{}', " \
											 "low[0] ='{}', low[1] = '{}', " \
											 "high[0] = '{}', high[1] ='{}' " \
											 "where _id_ ={} ".format(pricestr, priceval, lowstr, lowval, highstr,
																	 highval, _id_)
									break
							else:
								pricestr = 'NO COST CASE'
								priceval = '?'
								lowstr = 'NO COST CASE'
								lowval = '?'
								highstr = 'NO COST CASE'
								highval = '?'
								querry = "update feedbacks set " \
										 "price[0] = '{}', price[1] = '{}', " \
										 "low[0] ='{}', low[1] = '{}', " \
										 "high[0] = '{}', high[1] ='{}' " \
										 "where _id_ ={}".format(pricestr, priceval, lowstr, lowval, highstr,
																 highval,_id_)


				q_run(self.connD, querry)
				self.getquerry()
				self.filterdframe(self.filterlisboxtype.get(), self.filterlisboxdet.get())
				self.fillfdblist(self.presentfeedbacks)
				dflisted = self.presentfeedbacks.values.tolist()
				self.updatefeedbackwindows(dflisted[index])
				self.feedbacklist.select_set(index)
				self.feedbacklist.see(index)
			index = self.feedbacklist.curselection()[0]
			fdbflag = self.fdbflagstring.current()
			costflag = self.costflagstring.current()
			_id_ = self.presentfeedbacks.iloc[index].loc['fdbid']
			if fdbflag == 0: fdbflag = 'Null'
			if costflag == 0: costflag = 'Null'
			querry = """UPDATE feedbacks set fdbflag = {},costflag = {}
	            where _id_ = {}""".format(fdbflag, costflag, _id_)
			q_run(self.connD, querry)
			if str(fdbflag) == 'Null': fdbflag = 0
			if str(costflag) == 'Null': costflag = 0
			self.presentfeedbacks.loc[self.presentfeedbacks.fdbid == _id_,'fdbflag'] = fdbflag
			self.fdbdFrame.loc[self.fdbdFrame.fdbid == _id_,'fdbflag'] = fdbflag
			self.presentfeedbacks.loc[self.presentfeedbacks.fdbid == _id_,'costflag'] = costflag
			self.fdbdFrame.loc[self.fdbdFrame.fdbid == _id_,'costflag'] = costflag
			self.filterdframe(self.filterlisboxtype.get(), self.filterlisboxdet.get())
			self.fillfdblist(self.presentfeedbacks)
			loadcost()


		def updatecosts():
			index = self.feedbacklist.curselection()[0]
			_id_ = self.presentfeedbacks.iloc[index].loc['fdbid']

			price0 = self.pricetext.get("1.0",END).strip()
			price1 = self.priceval.get("1.0",END).strip()
			low0 = self.lowtext.get("1.0",END).strip()
			low1 = self.lowval.get("1.0",END).strip()
			high0 =self.hightext.get("1.0",END).strip()
			high1 = self.highval.get("1.0",END).strip()


			querry = """UPDATE feedbacks set
							price[0] = '{}',price[1] = '{}',
				            low[0] = '{}',low[1] = '{}',
				            high[0] = '{}',high[1] = '{}'
				            where _id_ = {}""".format(
												price0, price1,
												low0, low1,
												high0, high1,
												_id_)

			q_run(self.connD, querry)
			#print(querry)
			self.getquerry()
			self.filterdframe(self.filterlisboxtype.get(), self.filterlisboxdet.get())
			self.fillfdblist(self.presentfeedbacks)
			self.feedbacklist.select_set(index)
			self.feedbacklist.see(index)


		## + FUNKCJA DO PRZELICZANIA COST FLAG
		## + ODWIEZANIE MAIN DATASETA + UWZGLEDNIENIE WYBRANYCH FILTRÓW
		headtext = """
	Ship: {}
	Device: {}
	Report: {}
	        """.format('SHIPNAME', 'DEVICENAME', 'REPORTNO')
		self.labelhead = tk.Label(frame, text=headtext)
		self.remarktext = tk.Text(frame, height=10, width=50, wrap=WORD)
		self.fdbtext = tk.Text(frame, height=10, width=50, wrap=WORD)
		self.fdbflagstring = ttk.Combobox(frame, width=40, values=column(self.fdbflagz, 1), state="readonly")
		self.costflagstring = ttk.Combobox(frame, width=40, values=column(self.costflagz, 1), state="readonly")
		self.remarktext.configure(state='disabled')
		self.fdbtext.configure(state='disabled')
		self.setflagbut = tk.Button(frame, text='Update flags', command=setflags)

		self.pricetext = tk.Text(frame, height=1, width=30, wrap=WORD)
		self.priceval = tk.Text(frame, height=1, width=30, wrap=WORD)

		self.lowtext = tk.Text(frame, height=1, width=30, wrap=WORD)
		self.lowval = tk.Text(frame, height=1, width=30, wrap=WORD)

		self.hightext = tk.Text(frame, height=1, width=30, wrap=WORD)
		self.highval = tk.Text(frame, height=1, width=30, wrap=WORD)

		self.setcostbut = tk.Button(frame, text='Update costs', command=updatecosts)

		# Grid manager
		self.labelhead.grid(row=0, column=0, columnspan=2)
		tk.Label(frame, text='Remark').grid(row=1, column=0, columnspan=2)
		self.remarktext.grid(row=2, column=0, columnspan=2)
		tk.Label(frame, text='Feedback').grid(row=1, column=2)
		self.fdbtext.grid(row=2, column=2)
		tk.Label(frame, text='FDB flag').grid(row=3, column=0)
		self.fdbflagstring.grid(row=3, column=1)
		self.fdbflagstring.current(0)
		tk.Label(frame, text='Cost flag').grid(row=4, column=0)
		self.costflagstring.grid(row=4, column=1)
		self.costflagstring.current(0)
		self.setflagbut.grid(row=3, column=2, columnspan=2, rowspan=2)

		tk.Label(frame, text='Price of work done').grid(row=6, column=0)
		self.pricetext.grid(row=6, column=1)
		self.priceval.grid(row=6, column=2)

		tk.Label(frame, text='Lowest cost of damage').grid(row=7, column=0)
		self.lowtext.grid(row=7, column=1)
		self.lowval.grid(row=7, column=2)

		tk.Label(frame, text='Highest cost of damage').grid(row=8, column=0)
		self.hightext.grid(row=8, column=1)
		self.highval.grid(row=8, column=2)

		self.setcostbut.grid(row=9, column=2)




if __name__ == '__main__' :
	LogApplication()
	#feedbackswindow(connD)