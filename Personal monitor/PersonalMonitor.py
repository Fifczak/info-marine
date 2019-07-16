
#FIFCZAK BASICS
import psycopg2
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
###


import pandas as pd
from tkinter import *
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import re
import csv
connD=['testuser','info','192.168.10.243']
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
			DayflowFrame(connD)




class DayflowFrame():


	def createwindow(self,connD):
		def showMonthTasks():
			querry = "select ini from users where full_name = '{}'".format(self.e1.get())
			ini = list(q_run(connD,querry))[0][0]


			datec = datetime.strptime(self.e2.get(),'%Y-%m-%d')


			tasks = ['pomiar', 'struct', 'datasheet', 'report', 'analysis', 'accept', 'send_raport', 'remarks',
					 'feedbacks']
			monthtaskframe = pd.DataFrame(columns={'pomiar', 'struct', 'datasheet', 'report', 'analysis', 'accept', 'send_raport', 'remarks',
					 'feedbacks'})
			for item in tasks:
				querry = "select count(lp) from harmonogram where {}_kto = '{}' and date_part('month',{}_koniec) = {} ".format(item,ini,item,datec.month)

				monthtaskframe.loc[0, '{}'.format(item)] = list(q_run(connD,querry))[0][0]

			print('{}_{}.xlsx'.format(ini,datec.month))
			monthtaskframe.to_excel('{}_{}.xlsx'.format(ini,datec.month))


		def showDayChart():
			def tasklogbymin(taskloglist):
				checklist = list()
				checklist.clear()
				tasklog = pd.DataFrame(columns={'minute', 'active'})
				datestart = datetime.strptime(str(self.e2.get())[:10], '%Y-%m-%d').date()

				timelist = (pd.DataFrame(columns=['NULL'],
								  index=pd.date_range('{}T08:00:00Z'.format(datestart), '{}T16:00:00Z'.format(datestart),
													  freq='15T'))
					 .between_time('08:00', '16:00')
					 .index.strftime('%Y-%m-%d %H:%M')
					 .tolist()
					 )

				tasklogdf = pd.DataFrame(columns={'minute','pomiar', 'struct', 'datasheet', 'report', 'analysis', 'accept', 'send_raport', 'remarks',
						 'feedbacks'})
				cc=-1
				for tt in timelist:
					cc += 1
					tasklogdf.loc[cc, 'minute'] = tt


				for item in taskloglist:
					for index, row in item.iterrows():
						tl = item.columns[0].rfind('_')
						taskstr = item.columns[0][0:tl]
						colstr = '{}_start'.format(taskstr)
						minutemin = (str(row['{}_start'.format(taskstr)]))
						minutemax = (str(row['{}_koniec'.format(taskstr)]))
						if str(minutemin) == 'NaT':
							print('yesterday')

						elif str(minutemax) == 'NaT':
							print('tomorow')
							taskchartdata = list()
							taskchartdata.clear()
							cc = -1
							for tt in timelist:
								cc += 1
								if tt >= minutemin:
									tasklogdf.loc[cc, taskstr] =1
								else:
									tasklogdf.loc[cc, taskstr] =0
						else:
							taskchartdata = list()
							taskchartdata.clear()
							cc = -1
							for tt in timelist:
								cc += 1
								if tt >= minutemin and tt <= minutemax:
									tasklogdf.loc[cc, taskstr] =1
								else:
									tasklogdf.loc[cc, taskstr] =0

				return(tasklogdf)

			def chlogbymin(chlog):
				checklist = list()
				checklist.clear()
				fchlog = pd.DataFrame(columns={'minute', 'actions'})
				datestart = datetime.strptime(str(self.e2.get())[:10], '%Y-%m-%d').date()

				timelist = (pd.DataFrame(columns=['NULL'],
								  index=pd.date_range('{}T08:00:00Z'.format(datestart), '{}T16:00:00Z'.format(datestart),
													  freq='15T'))
					 .between_time('08:00', '16:00')
					 .index.strftime('%Y-%m-%d %H:%M')
					 .tolist()
					 )
				tic = -1
				for item in timelist:
					tic += 1
					fchlog.loc[tic, 'minute'] = item
					count = 0
					for index, row in chlog.iterrows():
						minute = (str(row['tstamp'])[:16])
						if minute > timelist[tic] and minute < timelist[tic+1]:
							count +=1
					fchlog.loc[tic, 'actions'] = count
				return(fchlog)
			def preparetask():

				tasklogframesslist = list()
				tasks = ['pomiar', 'struct', 'datasheet', 'report', 'analysis', 'accept', 'send_raport', 'remarks',
						 'feedbacks']
				for item in tasks:
					login = column(self.nameslist, 1)[self.e1.current()]
					date = datetime.strptime(self.e2.get(), "%Y-%m-%d")
					self.modified_date = date + timedelta(days=1)
					datetime.strftime(self.modified_date, "%Y-%m-%d")
					querry = """
						select {}_start,{}_koniec from harmonogram where {}_kto =
						 (select ini from users where login = '{}') and(({}_start >=   timestamp '{} 00:00:00'
						  and {}_start < timestamp '{}')or ({}_koniec >=   timestamp '{} 00:00:00'
						  and {}_koniec < timestamp '{}'))order by analysis_start

						""".format(item,item,item,login,item,self.e2.get(),item,self.modified_date,item,self.e2.get()\
								   ,item,self.modified_date)
					tasklog = list(q_run(connD, querry))

					if len(tasklog) != 0:
						tasklogframe = pd.DataFrame(columns={'{}_start'.format(item), '{}_koniec'.format(item)})
						tasklogframesslist.append(tasklogframe)
						tic = -1
						for stamp in tasklog:
							tic +=1
							tasklogframe.loc[tic, '{}_start'.format(item)] = stamp[0]
							tasklogframe.loc[tic, '{}_koniec'.format(item)] =stamp[1]
				return tasklogframesslist

			def preparechlog():
				login = column(self.nameslist,1)[self.e1.current()]
				date = datetime.strptime(self.e2.get(), "%Y-%m-%d")
				self.modified_date = date + timedelta(days=1)
				datetime.strftime(self.modified_date, "%Y-%m-%d")
				querry = "select tstamp,tabname from logging.t_history where who = '{}' and tstamp >= timestamp '{} 00:00:00'"\
	  "and tstamp < timestamp '{}' order by tstamp ".format(login,self.e2.get(),self.modified_date)
				changelog = q_run(connD,querry)
				return changelog

			fig, (ax1, ax2) = plt.subplots(2, 1, sharex='col')
			plt.yscale('log')
			fig.suptitle('Day work flow {} in {}'.format(str(self.e1.get()).strip(),str(self.e2.get())  , fontsize=16))
			taskflow = tasklogbymin(preparetask())

			x1 = taskflow['minute']
			y1 = taskflow['pomiar']
			y2 = taskflow['struct']
			y3 = taskflow['datasheet']
			y4 = taskflow['report']
			y5 = taskflow['analysis']
			y6 = taskflow['accept']
			y7 = taskflow['send_raport']
			y8 = taskflow['remarks']
			y9 = taskflow['feedbacks']
			ax1.plot(x1,y1, label="pomiar")
			ax1.plot(x1,y2, label="struct")
			ax1.plot(x1,y3, label="datasheet")
			ax1.plot(x1,y4, label="report")
			ax1.plot(x1,y5, label="analysis")
			ax1.plot(x1,y6, label="accept")
			ax1.plot(x1,y7, label="send_raport")
			ax1.plot(x1,y8, label="remarks")
			ax1.plot(x1,y9, label="feedbacks")
			ax1.set_yticklabels([])
			ax1.legend()

			ax1.xaxis.set_visible(False)


			chlgDframe = pd.DataFrame(preparechlog())
			try:
				chlgDframe.columns=['tstamp','tabname']
				xy = chlogbymin(chlgDframe)
				x = xy['minute']
				y = xy['actions']
				ax2.bar(x,y)
			except:
				pass

			fig.autofmt_xdate()
			plt.show()

		self.remWindow = tk.Tk()
		tk.Label(self.remWindow,
				 text="Person").grid(row=0, sticky=tk.W)
		tk.Label(self.remWindow,
				 text="Date").grid(row=1, sticky=tk.W)
		querry = "select full_name,login from users where role_id = '{1}' order by full_name"
		self.nameslist = list(q_run(connD,querry))

		self.e1 = ttk.Combobox(self.remWindow, state="readonly")

		self.e1['values'] = column(self.nameslist,0)
		self.e2 = tk.Entry(self.remWindow)

		self.e2.insert(0, datetime.now().date())
		self.e1.grid(row=0, column=1, sticky=tk.W)
		self.e2.grid(row=1, column=1, sticky=tk.W)
		tk.Button(self.remWindow,command = showDayChart, text="Show day flow").grid(row=3,
															 column=0,
															 sticky=tk.W,

															 pady=4)
		tk.Button(self.remWindow,command = showMonthTasks, text="Show Month stats").grid(row=3,
															 column=1,
															 sticky=tk.W,

															 pady=4)


		self.remWindow.mainloop()
	def __init__(self,connD):
		self.createwindow(connD)

LogApplication()
