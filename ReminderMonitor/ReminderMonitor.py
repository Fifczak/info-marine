import psycopg2
import csv

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox

host = '192.168.10.243'
username = 'testuser'
password =  'info'
connD = [username,password,host]

def q_run(connD, querry):
		username = connD[0]
		password = connD[1]
		host = connD[2]
		kport = "5432"
		kdb = "postgres"
		#cs = ' host="localhost",database="postgres", user= "postgres" , password="info" '
		cs = "dbname=%s user=%s password=%s host=%s port=%s"%(kdb,username,password,host,kport)
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
		mainquerry = """
select ml.raport_number, remrn.raport_number as RemarksT, fdbrn.raport_number as FeedbacksT, remindrn.raport_number as ReminderT, remsend.raport_number as remsend

from measurements_low as ml
left join (select raport_number from remarks group by raport_number) as remrn on ml.raport_number = remrn.raport_number
left join (select raport_number from feedbacks group by raport_number) as fdbrn on ml.raport_number = fdbrn.raport_number
left join (select raport_number from reminder group by raport_number) as remindrn on ml.raport_number = remindrn.raport_number
left join (select raport_number from reminder where status = 1 group by raport_number) as remsend on ml.raport_number = remsend.raport_number
left join (select lp,report_number from harmonogram) as har on ml.raport_number = har.report_number

where har.lp is not null

group by ml.raport_number, remrn.raport_number, fdbrn.raport_number, remindrn.raport_number,remsend.raport_number,har.lp

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
		self.Lbox2 = tk.Listbox(self.rmwWindow)
		self.Lbox3 = tk.Listbox(self.rmwWindow)
		self.Lbox4 = tk.Listbox(self.rmwWindow)

		for line in mainlist:

			self.Lbox1.insert(END, line[0])
			if str(line[1]) == 'None': self.Lbox1.itemconfig(END, bg='Red')
			else: self.Lbox1.itemconfig(END, bg='Green')


			self.Lbox2.insert(END, line[0])
			if str(line[1]) == 'None': self.Lbox2.itemconfig(END, bg='Grey')
			else:
				if str(line[2]) == 'None': self.Lbox2.itemconfig(END, bg='Red')
				else: self.Lbox2.itemconfig(END, bg='Green')


			self.Lbox3.insert(END, line[0])
			if str(line[1]) == 'None': self.Lbox3.itemconfig(END, bg='Grey')
			else:
				if str(line[3]) == 'None': self.Lbox3.itemconfig(END, bg='Red')
				else: self.Lbox3.itemconfig(END, bg='Green')


			self.Lbox4.insert(END, line[0])
			if str(line[1]) == 'None': self.Lbox4.itemconfig(END, bg='Grey')
			else:
				if str(line[4]) == 'None': self.Lbox4.itemconfig(END, bg='Red')
				else: self.Lbox4.itemconfig(END, bg='Green')




		self.Lab1.pack(side=LEFT,anchor = N)
		self.Lbox1.pack(side=LEFT, anchor = S, fill=Y)

		self.Lab2.pack(side=LEFT,anchor = N)
		self.Lbox2.pack(side=LEFT, anchor=S, fill=Y)

		self.Lab3.pack(side=LEFT,anchor = N)
		self.Lbox3.pack(side=LEFT, anchor=S, fill=Y)

		self.Lab4.pack(side=LEFT,anchor = N)
		self.Lbox4.pack(side=LEFT, anchor=S, fill=Y)





		self.rmwWindow.mainloop()


		#self.Reportlistbox.bind('<Double-Button>', setquaterly)

		# self.remtextfield = tk.Text(self.rmwWindow, width=20, height=20)
		# self.remtextfield.insert(INSERT, str(devlist[index].remcom))
		# self.remtextfield.grid(column=0, row=7, columnspan=2)

reminder_monitor_window()

