import psycopg2
import csv

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox

host = '192.168.10.243'
username = 'testuser'
password = 'info'
connD = [username, password, host]


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


class reminder_monitor_window:

	def __init__(self):

		def getremarsrn(evt):
			w = evt.widget
			index = int(w.curselection()[0])
			raportno = w.get(index)
			reminder_remarks_details(raportno)

		def getfedrn(evt):
			w = evt.widget
			index = int(w.curselection()[0])
			raportno = w.get(index)
			reminder_feedbacks_details(raportno)

		def getreminderrn(evt):
			w = evt.widget
			index = int(w.curselection()[0])
			raportno = w.get(index)
			reminder_reminder_details(raportno)

		mainquerry = """
select ml.raport_number, remrn.raport_number as RemarksT, fdbrn.raport_number as FeedbacksT, remindrn.raport_number as ReminderT, remsend.raport_number as remsend,remrn.sended

from measurements_low as ml
left join (select rem1.raport_number,rem2.sended
			from remarks as rem1
			left join(select raport_number,sended from remarks 
						where raport_number <> ''
						group by raport_number,sended
						order by raport_number) as rem2 on rem1.raport_number = rem2.raport_number and rem2.sended = true

			where rem1.raport_number <> ''
			group by rem1.raport_number,rem2.sended) as remrn on ml.raport_number = remrn.raport_number
left join (select raport_number from feedbacks group by raport_number) as fdbrn on ml.raport_number = fdbrn.raport_number
left join (select raport_number from reminder group by raport_number) as remindrn on ml.raport_number = remindrn.raport_number
left join (select raport_number from reminder where status = 1 group by raport_number) as remsend on ml.raport_number = remsend.raport_number
left join (select lp,report_number from harmonogram) as har on ml.raport_number = har.report_number

where har.lp is not null

group by ml.raport_number, remrn.raport_number , fdbrn.raport_number , remindrn.raport_number , remsend.raport_number ,remrn.sended,har.lp
--order by ml.raport_number desc
order by har.lp desc

		"""
		self.rmwWindow = tk.Tk()
		self.rmwWindow.title("Reminder monitor")
		self.Lab1 = tk.Label(self.rmwWindow, text="Remarks")
		self.Lab2 = tk.Label(self.rmwWindow, text="Feedbacks")
		self.Lab3 = tk.Label(self.rmwWindow, text="Reminder")
		self.Lab4 = tk.Label(self.rmwWindow, text="Reminder sent")
		mainlist = q_run(connD, mainquerry)

		self.Lbox1 = tk.Listbox(self.rmwWindow)
		self.Lbox1.bind('<Double-Button>', getremarsrn)

		self.Lbox2 = tk.Listbox(self.rmwWindow)
		self.Lbox2.bind('<Double-Button>', getfedrn)

		self.Lbox3 = tk.Listbox(self.rmwWindow)
		self.Lbox3.bind('<Double-Button>', getreminderrn)
		self.Lbox4 = tk.Listbox(self.rmwWindow)

		for line in mainlist:

			self.Lbox1.insert(END, line[0])
			if str(line[1]) == 'None':
				self.Lbox1.itemconfig(END, bg='Red')
			else:
				self.Lbox1.itemconfig(END, bg='Green')

			self.Lbox2.insert(END, line[0])
			if str(line[1]) == 'None':
				self.Lbox2.itemconfig(END, bg='Grey')
			elif str(line[5]) == 'None':
				self.Lbox2.itemconfig(END, bg='Grey')
			else:
				if str(line[2]) == 'None':
					self.Lbox2.itemconfig(END, bg='Red')
				else:
					self.Lbox2.itemconfig(END, bg='Green')

			self.Lbox3.insert(END, line[0])
			if str(line[1]) == 'None':
				self.Lbox3.itemconfig(END, bg='Grey')
			else:
				if str(line[3]) == 'None':
					self.Lbox3.itemconfig(END, bg='Red')
				else:
					self.Lbox3.itemconfig(END, bg='Green')

			self.Lbox4.insert(END, line[0])
			if str(line[1]) == 'None':
				self.Lbox4.itemconfig(END, bg='Grey')
			else:
				if str(line[4]) == 'None':
					self.Lbox4.itemconfig(END, bg='Red')
				else:
					self.Lbox4.itemconfig(END, bg='Green')

		self.Lab1.pack(side=LEFT, anchor=N)
		self.Lbox1.pack(side=LEFT, anchor=S, fill=Y)

		self.Lab2.pack(side=LEFT, anchor=N)
		self.Lbox2.pack(side=LEFT, anchor=S, fill=Y)

		self.Lab3.pack(side=LEFT, anchor=N)
		self.Lbox3.pack(side=LEFT, anchor=S, fill=Y)

		self.Lab4.pack(side=LEFT, anchor=N)
		self.Lbox4.pack(side=LEFT, anchor=S, fill=Y)

		self.rmwWindow.mainloop()

	# self.remtextfield = tk.Text(self.rmwWindow, width=20, height=20)
	# self.remtextfield.insert(INSERT, str(devlist[index].remcom))
	# self.remtextfield.grid(column=0, row=7, columnspan=2)


class reminder_remarks_details:

	def __init__(self, raport_number):
		self.remdevlist = list()
		self.rn = raport_number
		self.remwin = tk.Tk()
		self.remwin.title("Remarks detail")

		querry = """
		
		select ml.id,dev.name,rem.remark
from measurements_low as ml
left join devices as dev on ml.id = dev.id
left join (select parent, sort, cast(id as integer) from ds_structure where id ~E'^\\\d+$') as dss on ml.id = dss.id
left join remarks as rem on ml.id = rem.id and rem.raport_number = '""" + str(raport_number) + """' 
where ml.raport_number = '""" + str(raport_number) + """' 
group by ml.id, dss.sort,rem.remark,dev.name
order by dss.sort
		
		"""
		c = 0
		self.devicelistbox = tk.Listbox(self.remwin, width=50)
		self.textfield = tk.Text(self.remwin, width=100)
		self.devicelistbox.bind('<<ListboxSelect>>', self.onselect)

		self.remdevlist = q_run(connD, querry)
		for line in self.remdevlist:
			self.devicelistbox.insert(END, line[1])
			if str(line[2]) != 'None':
				self.devicelistbox.itemconfig(END, bg='Green')

		self.devicelistbox.pack(side=LEFT, anchor=N, fill=Y)
		self.textfield.pack(side=LEFT, anchor=N, fill=Y)

	def onselect(self, evt):
		w = evt.widget
		index = int(w.curselection()[0])
		querry = 'select remark from remarks where id =' + str(
			self.remdevlist[index][0]) + " and raport_number = '" + str(self.rn) + "' limit 1"

		self.textfield.delete('1.0', END)
		self.textfield.insert(INSERT, q_run(connD, querry)[0][0])


class reminder_feedbacks_details:

	def __init__(self, raport_number):
		self.feddevlist = list()
		self.rn = raport_number
		self.remwin = tk.Tk()
		self.remwin.title("Remarks detail")

		querry = """
	select rem.id,dev.name,rem.remark,rem.sended,fdb.feedback
	from remarks as rem
	left join devices as dev on rem.id = dev.id
	left join (select parent, sort, cast(id as integer) from ds_structure where id ~E'^\\\d+$') as dss on rem.id = dss.id
	left join feedbacks as fdb on rem.id = fdb.id and rem.raport_number = fdb.raport_number
	where rem.raport_number = '""" + str(raport_number) + """' 
	group by rem.id, dss.sort,rem.remark,dev.name,rem.sended,fdb.feedback
	order by dss.sort

			"""
		c = 0
		self.devicelistbox = tk.Listbox(self.remwin, width=50)
		self.textfield = tk.Text(self.remwin, width=100)
		self.textfield2 = tk.Text(self.remwin, width=100)
		self.devicelistbox.bind('<<ListboxSelect>>', self.onselect)
		self.feddevlist = q_run(connD, querry)
		for line in self.feddevlist:
			self.devicelistbox.insert(END, line[1])
			if str(line[4]) != 'None':
				self.devicelistbox.itemconfig(END, bg='Green')

			if str(line[4]) == 'None' and str(line[3]) == 'True':
				self.devicelistbox.itemconfig(END, bg='Red')
		# if str(line[2]) != 'None':
		# 	self.devicelistbox.itemconfig(END, bg='Green')

		self.devicelistbox.pack(side=LEFT, anchor=N, fill=Y)
		self.textfield.pack(side=TOP, anchor=N)
		self.textfield2.pack(side=TOP, anchor=N)

	def onselect(self, evt):
		w = evt.widget
		index = int(w.curselection()[0])
		querry = 'select rem.remark, fdb.feedback from remarks as rem ' \
				 ' left join feedbacks as fdb on rem.raport_number = fdb.raport_number and rem.id = fdb.id' \
				 ' where rem.id =' + str(
			self.feddevlist[index][0]) + " and rem.raport_number = '" + str(self.rn) + "' limit 1"

		res = q_run(connD, querry)
		self.textfield.delete('1.0', END)
		self.textfield.insert(INSERT, res[0][0])
		self.textfield2.delete('1.0', END)
		self.textfield2.insert(INSERT, res[0][1])


class reminder_reminder_details:

	def __init__(self, raport_number):
		self.feddevlist = list()
		self.rn = raport_number
		self.remwin = tk.Tk()
		self.remwin.title("Remarks detail")

		querry = """
	select rem.id,dev.name,rem.remark, remi.send_date, remi.request_date
	from remarks as rem
	left join devices as dev on rem.id = dev.id
	left join (select parent, sort, cast(id as integer) from ds_structure where id ~E'^\\\d+$') as dss on rem.id = dss.id
	left join reminder as remi on rem.id = remi.id and rem.raport_number = remi.raport_number
	where rem.raport_number =  '""" + str(raport_number) + """' 
	group by rem.id, dss.sort,rem.remark,dev.name,rem.sended, remi.send_date, remi.request_date
	order by dss.sort
			"""
		c = 0
		self.devicelistbox = tk.Listbox(self.remwin, width=50)
		self.textfield = tk.Text(self.remwin, width=100)
		self.textfield2 = tk.Text(self.remwin, width=100)
		self.devicelistbox.bind('<<ListboxSelect>>', self.onselect)
		self.feddevlist = q_run(connD, querry)
		for line in self.feddevlist:
			self.devicelistbox.insert(END, line[1])
			if str(line[4]) != 'None':
				self.devicelistbox.itemconfig(END, bg='Green')

			if str(line[4]) == 'None' and str(line[3]) == 'True':
				self.devicelistbox.itemconfig(END, bg='Red')
		# if str(line[2]) != 'None':
		# 	self.devicelistbox.itemconfig(END, bg='Green')

		self.devicelistbox.pack(side=LEFT, anchor=N, fill=Y)
		self.textfield.pack(side=TOP, anchor=N)
		self.textfield2.pack(side=TOP, anchor=N)

	def onselect(self, evt):
		w = evt.widget
		index = int(w.curselection()[0])
		querry = 'select rem.remark, fdb.feedback from remarks as rem ' \
				 ' left join feedbacks as fdb on rem.raport_number = fdb.raport_number and rem.id = fdb.id' \
				 ' where rem.id =' + str(
			self.feddevlist[index][0]) + " and rem.raport_number = '" + str(self.rn) + "' limit 1"
		print(querry)
		res = q_run(connD, querry)
		self.textfield.delete('1.0', END)
		self.textfield.insert(INSERT, res[0][0])
		self.textfield2.delete('1.0', END)
		self.textfield2.insert(INSERT, res[0][1])


reminder_monitor_window()
