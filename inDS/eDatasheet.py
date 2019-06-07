from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
import psycopg2
from tkinter import messagebox
import csv

host = 'localhost'
ownerlist = []


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
		self.sign_in_butt = Button(self.root, text="Sign In",
								   command=lambda ue=self.user_entry, pe=self.pass_entry: self.logging_in(ue, pe))
		self.sign_in_butt.grid(row=5, column=2)
		self.root.mainloop()
	def logging_in(self, user_entry, pass_entry):
		user_get = user_entry.get()  # Retrieve Username
		pass_get = pass_entry.get()  # Retrieve Password
		if bool(self.var.get()) == True:
			# config = Path('C:\overmind\\temp\log.csv')
			with open('C:\overmind\\temp\log.csv', 'w+', newline='') as csvfile:
				filewriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
				filewriter.writerow([user_get])
				filewriter.writerow([pass_get])
		connD = [user_get, pass_get, '192.168.10.243']
		querry = "SELECT current_user"
		usercheck = ''
		usercheck = q_run(connD, querry)  # PYINSTALLER ma problemy gdzies tu
		if usercheck != '':
			querry = "select name,id from main where parent =1 order by name"
			ownerlist = q_run(connD, querry)
			querry = "select name,id,parent from main where parent <> 1 order by name"
			shiplist = q_run(connD, querry)
			self.root.destroy()
			ShipsApplication(ownerlist, shiplist, connD)

class ShipsApplication():
	def __init__(self,ownerlist, shiplist, connD):
		def onselect(evt):
			shipid = self.tree.item(self.tree.selection()[0]).get('values')[0]
			Datasheet(connD, shipid)
		self.root2 = tk.Tk()
		self.root2.title("Chose ship")
		self.tree = ttk.Treeview(self.root2)
		i = -1
		for row in ownerlist:
			i += 1
			parent = self.tree.insert('', 'end', text=str(row[0]))
			j = -1
			for row2 in shiplist:
				j += 1
				if str(row[1]) == str(row2[2]):
					self.tree.insert(parent, 'end', text=str(row2[0]), values=(shiplist[j][1]))
		self.tree.bind('<Double-Button>', onselect)
		self.tree.pack(fill=BOTH, expand=1)



class Datasheet():
	def make_frame_meas(self, measframe, reportno, id, connD,parent):

		try:
			for widget in measframe.winfo_children():
				widget.destroy()
		except:
			pass

		rButton = tk.Button(measframe)
		xcord = 0
		pointlist = tk.Listbox(measframe)
		pointlist.config(width=5)
		rmslist = tk.Listbox(measframe)
		rmslist.config(width=7)
		envlist = tk.Listbox(measframe)
		envlist.config(width=7)
		mcremark = tk.Text(measframe, width=20)
		remark = tk.Text(measframe, width=20)
		feedback = tk.Text(measframe, width=20)

		for x in self.resultm:
			if x[1] == reportno:
				rButton.configure(text=reportno)
				if (str(x[0])).strip() == (str(id)).strip():
					# try:
					pointlist.insert(END, str(x[2]))
					rmslist.insert(END, round(float(x[3]), 3))
					rmslist.bind('<Double-Button>', lambda event, id=x[0], rn=x[1]: self.onselect2(event, id, rn, connD,parent))
					# print(str(x[5]))
					limStr = self.countLimit(str(x[5]), x[3])
					# print((str(limStr)).strip())
					if (str(limStr)).strip() == 'Cl. D' or (str(limStr)).strip() == 'V. III' or (
							str(limStr)).strip() == 'V.III' or (str(limStr)).strip() == 'Out of limit':
						rmslist.itemconfig(END, bg='Red')
					elif (str(limStr)).strip() == 'Cl. C' or (str(limStr)).strip() == 'V. II':
						rmslist.itemconfig(END, bg='Yellow')
					elif (str(limStr)).strip() == 'Cl. B' or (str(limStr)).strip() == 'Cl. A' or (
							str(limStr)).strip() == 'V. I' or (str(limStr)).strip() == 'V.I' or (
							str(limStr)).strip() == 'In limit':
						rmslist.itemconfig(END, bg='Green')

					# except:
					# rmslist.insert(END,'-')
					try:
						envlist.insert(END, round(float(x[4]), 3))
						envlist.bind('<Double-Button>',
									 lambda event, id=x[0], rn=x[1]: self.onselect3(event, id, rn, connD, parent))

					except:
						envlist.insert(END, '-')
					mcremark.bind('<Double-Button>',
								  lambda event, id=x[0], rn=x[1]: self.onselectmcard(event, id, rn, connD, parent))
					remark.bind('<Double-Button>',
								  lambda event, id=x[0], rn=x[1]: self.onselectremark(event, id, rn, connD, parent))
					feedback.bind('<Double-Button>',
								  lambda event, id=x[0], rn=x[1]: self.onselectfeedback(event, id, rn, connD, parent))



		#lambda event, id = x[0], rn = x[1]: self.onselect2(event, id, rn, connD, parent)

		# for x in self.resultmc:
		# if (str(x[0])).strip() == (str(id)).strip():
		# if (str(x[1])).strip() == (str(reportno[0])).strip():
		# mcremark.insert(INSERT, x[2])
		# break

		for mcx in self.resultmc:
			if (str(mcx[0])).strip() == (str(id)).strip():
				if (str(mcx[1])).strip() == (str(reportno)).strip():
					mcremark.insert(INSERT, mcx[2])
					break
		for x in self.resultrem:
			if (str(x[0])).strip() == (str(id)).strip():
				if (str(x[1])).strip() == (str(reportno)).strip():
					remark.insert(INSERT, x[2])
					break
		for fdx in self.resultfed:
			if (str(fdx[0])).strip() == (str(id)).strip():
				if (str(fdx[1])).strip() == (str(reportno)).strip():
					feedback.insert(INSERT, fdx[2])
					break

		rButton.pack()
		pointlist.pack(side=LEFT, fill=Y)
		rmslist.pack(side=LEFT, fill=Y)
		envlist.pack(side=LEFT, fill=Y)
		mcremark.pack(side=LEFT, fill=Y)
		remark.pack(side=LEFT, fill=Y)
		feedback.pack(side=LEFT, fill=Y)

		measframe.pack(side=LEFT, fill=tk.BOTH, expand=True)
	def countLimit(self,standard, value):
		value = float(value)

		for limNo in self.limits:
			if str(limNo[0]) == standard:
				if value <= float(limNo[3]):  # IF LIM1
					limStr = str(limNo[2])
					break
				else:
					if value <= float(limNo[5]):  # IF LIM2
						limStr = str(limNo[4])
						break
					else:
						if value <= float(limNo[7]):  # IF LIM3
							limStr = str(limNo[6])
							break
						else:
							limStr = str(limNo[8])
							break
		try:
			return limStr
		except:
			print('Limit count error')
	def onselect(self, evt,connD):
		w = evt.widget
		index = int(w.curselection()[0])
		value = w.get(index)
		id_ = self.results[index][0]
		self.update_device_parameters(connD,id_)
		replistc = list()
		replistc.clear()
		try:
			for widget in self.MASTERmeasframe.winfo_children():
				widget.destroy()
		except:
			print('no MASTERmeasframe')
		self.meascanv = Canvas(self.MASTERmeasframe, bg='#FFFFFF')
		if id_.isdigit() == True:
			querry = "select raport_number from measurements_low where id = " + id_ + " group by raport_number order by raport_number DESC"
			replistc = q_run(connD, querry)

		self.raportlist.delete(0, 'end')
		for i in replistc:
			self.raportlist.insert(END, str(i[0]))
		# make_frame_meas(Frame(self.meascanv, height=2, bd=1), i, id_)
		# rapmeasscrol = Scrollbar(self.MASTERmeasframe, orient=HORIZONTAL)
		# rapmeasscrol.pack(side=BOTTOM, fill=X)
		# rapmeasscrol.config(command=self.meascanv.xview)
		self.meascanv.config(width=300, height=300)
		# self.meascanv.config(xscrollcommand=rapmeasscrol.set)
		self.meascanv.pack(side=LEFT, fill=tk.BOTH, expand=True)
	def onselect2(self, evt, id, rn, connD,parent):
		w = evt.widget
		index = int(w.curselection()[0])
		value = w.get(index)
		querry = "select point from points where id = " + str(id) + " and sort = " + str(index +1)
		point = q_run(connD, querry)[0][0]
		self.ValRMSwindow(connD, self, value, id, rn, point,parent)
	def onselect3(self, evt, id, rn, connD,parent):
		w = evt.widget
		index = int(w.curselection()[0])
		value = w.get(index)
		querry = "select point from points where id = " + str(id) + " and sort = " + str(index +1)
		point = q_run(connD, querry)[0][0]
		self.ValENVwindow(connD, self, value, id, rn, point,parent)
	def onselectmcard(self, evt, id, rn, connD,parent):
		self.MCARDwindow(connD, self, id, rn, parent)
	def onselectremark(self, evt, id, rn, connD,parent):
		self.REMARKwindow(connD, self, id, rn, parent)
	def onselectfeedback(self, evt, id, rn, connD,parent):
		self.FEEDBACKwindow(connD, self, id, rn, parent)
	def loadquerrys(self,parent,connD):
		querry1 = "select raport_number from measurements_low where parent = " + str(
			parent) + " group by raport_number order by raport_number DESC "
		self.resultr = q_run(connD, querry1)
		querry2 = "SELECT dss.id, CASE WHEN dss.id ~E'^\\\d+$' THEN	(select name from devices where cast(devices.id as text)  =  dss.id limit 1) ELSE (select id from ds_structure where id  =  dss.id limit 1) END as sortint, dss.sort FROM ds_structure as dss where dss.parent = " + str(
			parent) + " ORDER BY DSS.SORT"
		self.results = q_run(connD, querry2)
		querry3 = """select ml.id, ml.raport_number, ml.point,  ml.value, ml2.value, dev.norm
						from measurements_low as ml 
						left join points as pts on ml.id = pts.id and ml.point = pts.point
						left join (select id,raport_number, point, value 
												from measurements_low where parent = '""" + str(parent) + """' and type = 'envelope P-K') as ml2 
												on ml.id=ml2.id and ml.raport_number = ml2.raport_number
												and ml.point = ml2.point 
						left join devices as dev on ml.id = dev.id
						where ml.parent =  """ + str(
			parent) + """ and ml.type = 'RMS' and ml.id <> 0 order by id, raport_number, sort"""
		self.resultm = q_run(connD, querry3)
		querry = "select id, raport_number, mcremark from mcdata where raport_number is not null and id is not null"
		self.resultmc = q_run(connD, querry)
		querry = "select id, raport_number, remark from remarks where raport_number is not null and id is not null"
		self.resultrem = q_run(connD, querry)
		querry = "select id, raport_number, feedback from feedbacks where raport_number is not null and id is not null"
		self.resultfed = q_run(connD, querry)
		querry = """select standard,
								limit_1_value,limit_1_name,
								limit_2_value,limit_2_name, 
								limit_3_value,limit_3_name,
								limit_4_value,limit_4_name,
							envflag
						from standards"""
		self.limits = q_run(connD, querry)
		# self.resultr = inputdata[0]
		# self.results = inputdata[1]
		# self.resultm = inputdata[2]
		# self.resultmc = inputdata[3]
		# self.resultrem = inputdata[4]
		# self.resultfed = inputdata[5]
		# self.limits = inputdata[6]
		return ([self.resultr, self.results, self.resultm, self.resultmc, self.resultrem, self.resultfed, self.limits])
	def RAPonselect(self, evt, connD,parent):
		w = evt.widget
		index = int(w.curselection()[0])
		value = w.get(index)
		try:
			for widget in self.meascanv.winfo_children():
				widget.destroy()
		except:
			print('no MASTERmeasframe')
		self.make_frame_meas(Frame(self.meascanv, height=2, bd=1), value, self.deviceid['text'], connD,parent)
	def update_device_parameters(self,connD,id_):
		querry = "select name, type, model from devices where id = " + str(id_)
		devparams = q_run(connD, querry)
		self.devicename.configure(text=devparams[0][0])
		self.deviceid.configure(text=str(id_))
		self.devicetype.configure(text=devparams[0][1])
		self.devicemodel.configure(text=devparams[0][2])
	def deviceslist(self, connD, mylist,parent):
		def lastrn(line0):
			for line3 in self.resultrS:
				for line2 in self.resultm:
					if str(line2[0]) == str(line0):
						if str(line3[0]).strip() == line2[1]:
							return line2[1]

		ycord = 0
		querry = "select raport_number from measurements_low where parent = " + str(
			parent) + " group by raport_number order by raport_number DESC"
		self.resultrS = q_run(connD, querry)
		xcord = 0

		for line in self.results:
			self.limitstr = ''
			maxValList = list()
			lrn = lastrn(line[0])
			if line[0].isnumeric() == True:
				tempval = 0
				tempval2 = 0
				limStr = 'ERR'
				for x in self.resultm:
					if str(x[1]) == str(lrn):
						if (str(x[0])).strip() == (str(line[0])).strip():
							if tempval < float(x[3]):
								tempval = float(x[3])
								limStr = self.countLimit(str(x[5]), x[3])
							try:
								if tempval2 < float(x[4]):
									tempval2 = float(x[4])
							except:
								pass

				mylist.insert(END, self.results[xcord][1] + '(' + str(lrn) + ':' + str(limStr) + ')')


			else:
				mylist.insert(END, self.results[xcord][1])
				mylist.itemconfig(END, bg='blue')
			xcord += 1
			#lambda event, id=x[0], rn=x[1]: onselect2(event, id, rn))
		mylist.bind('<<ListboxSelect>>',lambda event : self.onselect(event, connD))
					#self.onselect)
		cs = mylist.curselection()
		self.devicesscrollbar.config(command=mylist.yview)
		mylist.pack(side=LEFT, fill=BOTH)
	class ValRMSwindow():
		def __init__(self,connD, parentclass, value,id,rn,point,parent):
			def updateRMS():
				try:
					querry = "UPDATE measurements_low set value = "+str(self.Val.get("1.0",END))+",date = '"+str(self.ValDate.get("1.0",END))+"' where raport_number = '"+str(rn)+ "' and id = "+str(id)+" and type = 'RMS' and point = '"+str(point) + "'"
					q_run(connD,querry)
					for widget in parentclass.meascanv.winfo_children():
						widget.destroy()
					parentclass.loadquerrys(parent, connD)
					parentclass.make_frame_meas(Frame(parentclass.meascanv, height=2, bd=1), rn, id, connD,parent)
					self.window.destroy()
				except:
					messagebox.showinfo("Error", str('UPDATE FAILED'))

			self.window = tk.Tk()
			self.window.title("CHANGE RMS")
			self.Val = tk.Text(self.window, height=1, width=12)
			self.Val.insert(END, value)

			self.ValDate = tk.Text(self.window, height=1, width=12)
			querry = "select date from measurements_low where raport_number = '"+str(rn)+ \
						 "' and id = "+str(id)+" and type = 'RMS' and point = '"+str(point)+"' limit 1"
			dat = q_run(connD,querry)
			self.ValDate.insert(END, dat)
			self.okbut = tk.Button(self.window,text = 'Change',command=updateRMS, width=12)
			self.Val.pack(side=TOP)
			self.ValDate.pack(side=TOP)
			self.okbut.pack(side=TOP)
			self.window.mainloop()
	class ValENVwindow():
		def __init__(self,connD, parentclass, value,id,rn,point,parent):
			def updateENV():
				try:
					querry = "UPDATE measurements_low set value = "+str(self.Val.get("1.0",END))+",date = '"+str(self.ValDate.get("1.0",END))+"' where raport_number = '"+str(rn)+ "' and id = "+str(id)+" and type = 'envelope P-K' and point = '"+str(point) + "'"
					q_run(connD,querry)
					for widget in parentclass.meascanv.winfo_children():
						widget.destroy()
					parentclass.loadquerrys(parent, connD)
					parentclass.make_frame_meas(Frame(parentclass.meascanv, height=2, bd=1), rn, id, connD,parent)
					self.window.destroy()
				except:
					messagebox.showinfo("Error", str('UPDATE FAILED'))

			self.window = tk.Tk()
			self.window.title("CHANGE ENVELOPE")
			self.Val = tk.Text(self.window, height=1, width=12)
			self.Val.insert(END, value)

			self.ValDate = tk.Text(self.window, height=1, width=12)
			querry = "select date from measurements_low where raport_number = '"+str(rn)+ \
						 "' and id = "+str(id)+" and type = 'envelope P-K' and point = '"+str(point)+"' limit 1"
			dat = q_run(connD,querry)
			self.ValDate.insert(END, dat)
			self.okbut = tk.Button(self.window,text = 'Change',command=updateENV, width=12)
			self.Val.pack(side=TOP)
			self.ValDate.pack(side=TOP)
			self.okbut.pack(side=TOP)
			self.window.mainloop()
	class MCARDwindow():
		def __init__(self,connD, parentclass, id, rn, parent):#,connD, parentclass, value,id,rn,point,parent):
			def updateMCARD():
				try:
					querry = "UPDATE mcdata set mcremark = '"+str(self.MCREM.get("1.0",END))+"'," \
					"documentdate = '"+str(self.DocDate.get("1.0",END))+"' " \
					"where raport_number = '"+str(rn)+ "' and id = "+str(id)
					print(querry)
					q_run(connD,querry)
					for widget in parentclass.meascanv.winfo_children():
						widget.destroy()
					parentclass.loadquerrys(parent, connD)
					parentclass.make_frame_meas(Frame(parentclass.meascanv, height=2, bd=1), rn, id, connD,parent)
					self.window.destroy()
				except:
					messagebox.showinfo("Error", str('UPDATE FAILED'))

			self.window = tk.Tk()
			self.window.title("CHANGE MCARD")
			self.DocDate = tk.Text(self.window, height=1, width=12)
			querry = "select mcremark, documentdate from mcdata where " \
					 "raport_number = '" + str(rn) + "' and id = " + str(id) + " limit 1"
			resmc = q_run(connD,querry)

			self.MCREM = tk.Text(self.window, height=10, width=60)
			try:
				self.DocDate.insert(END, resmc[0][1])
				self.MCREM.insert(END, resmc[0][0])
			except:
				pass
			self.okbut = tk.Button(self.window,text = 'Change',command=updateMCARD, width=12)
			self.DocDate.pack(side=TOP)
			self.MCREM.pack(side=TOP)
			self.okbut.pack(side=TOP)

			self.window.mainloop()
	class REMARKwindow():
		def __init__(self,connD, parentclass, id, rn, parent):#,connD, parentclass, value,id,rn,point,parent):
			def updateREM():
				try:
					if self.var1.get() == 1:
						sendflag = 'True'
					else:
						sendflag = 'False'

					querry = "UPDATE remarks set remark = '"+str(self.REM.get("1.0",END))+"'," \
					"documentdate = '"+str(self.DocDate.get("1.0",END))+"', sended = " + str(sendflag) +  \
					" where raport_number = '"+str(rn)+ "' and id = "+str(id)

					q_run(connD,querry)
					for widget in parentclass.meascanv.winfo_children():
						widget.destroy()
					parentclass.loadquerrys(parent, connD)
					parentclass.make_frame_meas(Frame(parentclass.meascanv, height=2, bd=1), rn, id, connD,parent)
					self.window.destroy()
				except:
					messagebox.showinfo("Error", str('UPDATE FAILED'))
			self.window = tk.Tk()
			self.window.title("CHANGE REMARK")
			self.DocDate = tk.Text(self.window, height=1, width=12)

			querry = "select remark, documentdate,sended from remarks where " \
					 "raport_number = '" + str(rn) + "' and id = " + str(id) + " limit 1"

			resmc = q_run(connD,querry)

			self.REM = tk.Text(self.window, height=10, width=60)

			self.var1 = IntVar(self.window )
			self.var1.set(0)
			print(str(resmc[0][2]))
			if str(resmc[0][2]) == 'True':self.var1.set(1)

			self.sended = tk.Checkbutton(self.window, text='Sent', variable=self.var1, onvalue=1, offvalue=0)



			try:
				self.DocDate.insert(END, resmc[0][1])
				self.REM.insert(END, resmc[0][0])
			except:
				pass
			self.okbut = tk.Button(self.window,text = 'Change',command=updateREM, width=12)
			self.DocDate.pack(side=TOP)
			self.REM.pack(side=TOP)
			self.sended.pack(side=TOP)

			self.okbut.pack(side=TOP)

			self.window.mainloop()
	class FEEDBACKwindow():
		def __init__(self,connD, parentclass, id, rn, parent):#,connD, parentclass, value,id,rn,point,parent):
			def updateFDB():
				try:
					querry = "UPDATE feedbacks set feedback = '"+str(self.FDB.get("1.0",END))+"'," \
					"documentdate = '"+str(self.DocDate.get("1.0",END))+"' " \
					"where raport_number = '"+str(rn)+ "' and id = "+str(id)
					q_run(connD,querry)
					for widget in parentclass.meascanv.winfo_children():
						widget.destroy()
					parentclass.loadquerrys(parent, connD)
					parentclass.make_frame_meas(Frame(parentclass.meascanv, height=2, bd=1), rn, id, connD,parent)
					self.window.destroy()
				except:
					messagebox.showinfo("Error", str('UPDATE FAILED'))

			self.window = tk.Tk()
			self.window.title("CHANGE FEEDBACK")
			self.DocDate = tk.Text(self.window, height=1, width=12)
			querry = "select feedback, documentdate from feedbacks where " \
					 "raport_number = '" + str(rn) + "' and id = " + str(id) + " limit 1"
			resmc = q_run(connD,querry)

			self.FDB = tk.Text(self.window, height=10, width=60)
			try:
				self.DocDate.insert(END, resmc[0][1])
				self.FDB.insert(END, resmc[0][0])
			except:
				pass
			self.okbut = tk.Button(self.window,text = 'Change',command=updateFDB, width=12)
			self.DocDate.pack(side=TOP)
			self.FDB.pack(side=TOP)
			self.okbut.pack(side=TOP)

			self.window.mainloop()



	limits = list()

	def __init__(self,connD,parent):

		self.loadquerrys(parent,connD)
		self.Fwindow = tk.Tk()
		self.Fwindow.title("Info Datasheet")
		self.devicesscrollbar = Scrollbar(self.Fwindow)
		self.devicesscrollbar.pack(side=LEFT, fill=Y)
		devicesscrollbarX = Scrollbar(self.Fwindow, orient=HORIZONTAL)
		devicesscrollbarX.pack( side=BOTTOM, fill=X )
		self.mylist = Listbox(self.Fwindow, yscrollcommand=self.devicesscrollbar.set)
		self.mylist.config(width=0)
		self.deviceslist(connD,self.mylist, parent)

		self.deviceframe = Frame(self.Fwindow)
		self.devicename = tk.Label(self.deviceframe, text="Name")
		self.deviceid = tk.Label(self.deviceframe, text="id")
		self.devicetype = tk.Label(self.deviceframe, text="TYPE: ")
		self.devicemodel = tk.Label(self.deviceframe, text="MODEL: ")
		self.raportlist = Listbox(self.deviceframe)
		self.raportlist.config(width=0)
		self.raportlist.bind('<<ListboxSelect>>', lambda event : self.RAPonselect(event, connD,parent))
							 #self.RAPonselect)
		# lambda event : self.onselect(event, connD)
		self.deviceframe.pack(side=LEFT)
		self.deviceid.pack(side=TOP)
		self.devicename.pack(side=TOP)
		self.devicetype.pack(side=TOP)
		self.devicemodel.pack(side=TOP)
		self.raportlist.pack(side=TOP)
		self.MASTERmeasframe = Canvas(self.Fwindow,width=300, xscrollcommand=devicesscrollbarX.set)
		devicesscrollbarX.config(command=self.MASTERmeasframe.xview)
		self.MASTERmeasframe.pack(side=LEFT, fill=Y)
		self.Fwindow.mainloop()


# Keeps the window open/running


#LogApplication()
Datasheet(['testuser','info','localhost'],79)