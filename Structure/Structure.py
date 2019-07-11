import psycopg2
import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
import csv
from tkinter.filedialog import askopenfilename
import tkinter as tkk
from tkinter import filedialog
from tqdm import tqdm
from tkinter import messagebox
from tkinter import simpledialog

host = '192.168.10.243'
#host = 'localhost'
devlist = list()
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
		connD = [user_get, pass_get, host]


		querry = "SELECT current_user"
		usercheck = ''

		usercheck = q_run(connD, querry)  # PYINSTALLER ma problemy gdzies tu
		if usercheck != '':
			self.root.destroy()
			StructWindow(connD)
class device:
	def __init__(self):
		self.id = ''
		self.name = ''
		self.model = ''
		self.type = ''
		self.kw = ''
		self.rpm = ''
		self.pms = ''
		self.info = ''
		self.norm = ''
		self.drivenby = ''
		self.meas_condition = ''
		self.interval_type = ''
		self.interval_length = ''
		self.points = list()
class PointComboboxObject:
	def callback(self, event=None):
		self.changecapt(self.showvalue,self.var.get(),self.sort)
		self.showvalue = self.var.get()
	def changecapt(self,oldval,newval,oR):
		clickBearing = (self.parentclass.CombBearingList[oR].showvalue)  ## MOJE AKTUALNE
		clickSealBearing = (self.parentclass.CombBearingSealList[oR].showvalue)
		clickAddBearing = (self.parentclass.CombBearingAddList[oR].showvalue)
		clickVisibleBearing = (self.parentclass.CombVisibleList[oR].showvalue)
		nR = -1
		for line in self.parentclass.CombPointList:
			nR+=1
			if line.showvalue == newval:
				line.cbox.delete(0, END)
				line.cbox.insert(0, oldval)
				line.showvalue = oldval
				clickRingBearing = (self.parentclass.CombBearingList[nR].showvalue)  ## bearing w tym ktory ma ten sam point
				clickRingBearingSeal = (self.parentclass.CombBearingSealList[nR].showvalue)
				clickRingBearingAdd = (self.parentclass.CombBearingAddList[nR].showvalue)
				clickRingVisibleBearing = (self.parentclass.CombVisibleList[nR].showvalue)
				self.parentclass.CombBearingList[nR].cbox.delete(0, END) #delete w tym ktory ma ten sam point
				self.parentclass.CombBearingList[nR].cbox.insert(0, clickBearing)
				self.parentclass.CombBearingList[nR].showvalue = clickBearing
				self.parentclass.CombBearingSealList[nR].cbox.delete(0, END)
				self.parentclass.CombBearingSealList[nR].cbox.insert(0, clickSealBearing)
				self.parentclass.CombBearingSealList[nR].showvalue = clickSealBearing
				self.parentclass.CombBearingAddList[nR].cbox.delete(0, END)
				self.parentclass.CombBearingAddList[nR].cbox.insert(0, clickAddBearing)
				self.parentclass.CombBearingAddList[nR].showvalue = clickAddBearing
				self.parentclass.CombVisibleList[nR].cbox.delete(0, END)
				self.parentclass.CombVisibleList[nR].cbox.insert(0, clickVisibleBearing)
				self.parentclass.CombVisibleList[nR].showvalue = clickVisibleBearing
				self.parentclass.CombBearingList[oR].cbox.delete(0, END)  # delete w wybranym
				self.parentclass.CombBearingList[oR].cbox.insert(0, clickRingBearing)
				self.parentclass.CombBearingList[oR].showvalue = clickRingBearing
				self.parentclass.CombBearingSealList[oR].cbox.delete(0, END)
				self.parentclass.CombBearingSealList[oR].cbox.insert(0, clickRingBearingSeal)
				self.parentclass.CombBearingSealList[oR].showvalue = clickRingBearingSeal
				self.parentclass.CombBearingAddList[oR].cbox.delete(0, END)
				self.parentclass.CombBearingAddList[oR].cbox.insert(0, clickRingBearingAdd)
				self.parentclass.CombBearingAddList[oR].showvalue = clickRingBearingAdd
				self.parentclass.CombVisibleList[oR].cbox.delete(0, END)
				self.parentclass.CombVisibleList[oR].cbox.insert(0, clickRingVisibleBearing)
				self.parentclass.CombVisibleList[oR].showvalue = clickRingVisibleBearing
	def __init__(self,parentframe,inlist,c,parentClass):
		self.parentclass = parentClass
		self.sort = c-1
		self.showvalue = str(inlist[c-1])
		self.valueslist = list()
		self.var = tk.StringVar()
		self.cbox = ttk.Combobox(parentframe, textvariable=self.var, values=inlist)
		self.cbox.grid(row=c, column=1)
		self.cbox.bind('<<ComboboxSelected>>',self.callback)
		self.cbox.insert(0, inlist[c-1])
		self.cbox.configure(values=inlist)
class BearingComboboxObject:
	def callback(self, event=None):
		self.showvalue = self.var.get()
	def __init__(self,parentframe,bearing,c,col,inlist2):
		self.showvalue = str(bearing)
		self.valueslist = list()
		self.var = tk.StringVar()
		self.cbox = ttk.Combobox(parentframe, textvariable=self.var)
		self.cbox.grid(row=c, column=col)
		self.cbox.bind('<<ComboboxSelected>>', self.callback)
		self.cbox.insert(0, str(bearing))
		self.cbox.configure(values=inlist2)
class DragDropListbox(tk.Listbox):
	""" A Tkinter listbox with drag'n'drop reordering of entries. """
	def __init__(self, master, **kw):
		kw['selectmode'] = tk.SINGLE
		tk.Listbox.__init__(self, master, kw)
		self.bind('<Button-1>', self.setCurrent)
		self.bind('<B1-Motion>', self.shiftSelection)
		self.curIndex = None

	def setCurrent(self, event):
		self.curIndex = self.nearest(event.y)


	def shiftSelection(self, event):
		i = self.nearest(event.y)
		if i < self.curIndex:
			x = self.get(i)
			color = self.itemcget(i, "background")
			color2 = self.itemcget(i, "fg")
			self.delete(i)
			self.insert(i+1, x)
			self.itemconfig(i + 1, background=color, fg = color2)

			self.curIndex = i

		if i > self.curIndex:
			x = self.get(i)
			color = self.itemcget(i, "background")
			color2 = self.itemcget(i, "fg")
			self.delete(i)
			self.insert(i-1, x)
			self.itemconfig(i-1, background=color, fg = color2)
			self.curIndex = i
class chosedevicewindow():
	def __init__(self,connD,shipid,listbox):
		def insertdevice():
			name = ships[cbox.current()]
			id = ids[cbox.current()]
			try:
				idx = listbox.curselection()[0]
			except:
				idx = 0
			listbox.insert(idx+1,'{}@{}'.format(name,id)  )

		self.devwindow = tk.Tk()
		self.devwindow.title("Structure")

		label = tk.Label(self.devwindow,text = 'Chose device')
		label.grid(row=0, column = 0)

		querry = "select name,id from devices where parent = {} order by name".format(shipid)
		ans = list(q_run(connD,querry))
		ships = column(ans,0)
		ids = column(ans, 1)
		self.var = tk.StringVar()
		cbox = ttk.Combobox(self.devwindow, textvariable=self.var, values=ships,state="readonly",width = 50)
		cbox.grid(row = 0, column = 1)


		addbut = tk.Button(self.devwindow,text = 'Add device', command = insertdevice).grid(row = 1, column = 0)


		self.devwindow.mainloop()


class ModelMakerWindow():
	def maker_change(self,event):
		idx = self.cbox.current()
		querry = "select id,name,type from main_models where parent = {} order by name".format(self.makersids[idx])
		ans = list(q_run(self.connD, querry))
		models = column(ans, 1)
		modelsids = column(ans, 0)
		self.types = column(ans, 2)
		self.cbox2.config(values=models)
		try:
			self.cbox2.current(0)
			self.typelabel.config(text = self.types[0])
		except:
			self.cbox2.config(text = ' ')
			self.typelabel.config(text=' ')

	def model_change(self,event):
		idx = self.cbox2.current()
		self.typelabel.config(text = self.types[idx])

	def addmaker(self):
		maker = simpledialog.askstring("Add maker", "Enter maker name:")
		querry = "INSERT INTO main_models (name) VALUES ('{}')".format(maker)
		q_run(connD, querry)
		querry = "select id,name from main_models where parent is null and name <> '' and name <> ' ' order by name"
		ans = list(q_run(connD, querry))
		self.makers = column(ans, 1)
		self.makersids = column(ans, 0)
		self.configures

	def addmodel(self):
		idx = self.cbox.current()

		querry = "INSERT INTO main_models (parent,name) VALUES (EMPTY,'{}')".format(self.makersids[idx])
		print(querry)

	def __init__(self,connD):
		self.connD = connD
		self.devwindow = tk.Tk()
		self.devwindow.title("Structure")
		label = tk.Label(self.devwindow, text='Maker')
		label.grid(row=0, column=0)
		querry = "select id,name from main_models where parent is null and name <> '' and name <> ' ' order by name"
		ans = list(q_run(connD, querry))
		self.makers = column(ans, 1)
		self.makersids = column(ans, 0)
		self.var = tk.StringVar()
		self.cbox = ttk.Combobox(self.devwindow, textvariable=self.var, values=self.makers, state="readonly", width=50)
		self.cbox.bind('<<ComboboxSelected>>', self.maker_change)
		self.cbox.grid(row=0, column=1)
		label = tk.Label(self.devwindow, text='Model')
		label.grid(row=1, column=0)
		self.var2 = tk.StringVar()
		self.cbox2 = ttk.Combobox(self.devwindow, textvariable=self.var2, state="readonly", width=50)
		self.cbox2.grid(row=1, column=1)
		self.cbox2.bind('<<ComboboxSelected>>', self.model_change)
		label2 = tk.Label(self.devwindow, text = 'Type: ')
		label2.grid(row = 2, column = 0)
		self.typelabel= tk.Label(self.devwindow, text = '-')
		self.typelabel.grid(row = 2, column =1 )

		#addbut = tk.Button(self.devwindow, text='Add device', command=insertdevice).grid(row=2, column=0)
		addmakerbut = tk.Button(self.devwindow, text='Add maker', command = self.addmaker)
		addmakerbut.grid(row=0, column=2)
		addmakerbut = tk.Button(self.devwindow, text='Add model', command = self.addmodel)
		addmakerbut.grid(row=1, column=2)


		self.devwindow.mainloop()

class StructWindow:
	class DevicesFrame:
		def reloadquerry(self,structuresort,shipid,connD):
			if structuresort == True:
				querry = """select dev.id, dev.name,mm.name,dev.type,kw,rpm,pms,info,st.standard,drivenby, meas_condition,cm,interval_type,interval_length
							from devices dev
							left join ds_structure dss on cast(dev.id as text) = dss.id
							left join main_models mm on dev.model_fkey = mm.id
							left join standards st on dev.standard_fkey = st.id
							where dev.parent ={}
							order by dss.sort""".format(str(shipid))
				ans = q_run(connD, querry)
				self.structuresort = False
			else:
				querry = """select dev.id, dev.name,mm.name,dev.type,kw,rpm,pms,info,st.standard,drivenby, meas_condition,cm,interval_type,interval_length
							from devices dev
							left join ds_structure dss on cast(dev.id as text) = dss.id
							left join main_models mm on dev.model_fkey = mm.id
							left join standards st on dev.standard_fkey = st.id
							where dev.parent = {}
							order by dev.name""".format(str(shipid))
				ans= q_run(connD, querry)
				self.structuresort = True
			self.devdata = list()
			self.devdata = list()
			self.devdata.clear()
			for item in ans:
				self.devdata.append(item)
			self.loaddevices()
		def loaddevices(self):
			self.deviceslistbox.delete(0, END)
			devlist.clear()
			for line in self.devdata:
				dev = device()
				self.deviceslistbox.insert(END, '{} @ {}'.format(line[1],line[0]))
				dev.id = str(line[0])
				dev.name = str(line[1])
				dev.model = str(line[2])
				dev.type = str(line[3])
				dev.kw = str(line[4])
				dev.rpm = str(line[5])
				dev.pms = str(line[6])
				dev.info = str(line[7])
				dev.norm = str(line[8])
				dev.drivenby = str(line[9])
				dev.meas_condition = str(line[10])
				dev.cm = str(line[11])

				if str(line[12]) == '1': dev.interval_type = "Day"
				elif str(line[12]) == '2': dev.interval_type = "Week"
				elif str(line[12]) == '3': dev.interval_type = "Month"
				dev.interval_length = str(line[13])
				devlist.append(dev)
			self.deviceslistbox.pack(fill=BOTH, expand = 1)
		def showmodelframe(self):
			ModelMakerWindow(self.connD)
		def __init__(self,parent,shipid,connD):
			def updatedevice():
				print('Update')
			def getdetails(evt):
				w = evt.widget
				index = int(w.curselection()[0])
				devname = w.get(index)
				for widget in self.detailframe.winfo_children():
					widget.destroy()
				for line in devlist:
					at = devname.find('@')
					dev = devname[:at-1]
					if str(line.name) == str(dev):
						self.title = tk.Label(self.detailframe, text='Id: '+str(line.id))
						self.title.grid(row=0, column=2)
						self.lab_name_l = tk.Label(self.detailframe, text="Name").grid(row=2, column=1)
						self.lab_name_e = tk.Entry(self.detailframe, width = 50)
						self.lab_name_e.grid(row=2, column=2)
						self.lab_name_e.insert(0, str(line.name))
						self.lab_model_l = tk.Label(self.detailframe, text="Model").grid(row=3, column=1)
						self.lab_model_e = tk.Button(self.detailframe, width = 40, command = self.showmodelframe)
						self.lab_model_e.grid(row=3, column=2)
						self.lab_model_e.configure(text =  str(line.model))
						self.lab_type_l = tk.Label(self.detailframe, text="Type").grid(row=4, column=1)
						self.lab_type_e = tk.Entry(self.detailframe, text="", width = 50)
						self.lab_type_e.grid(row=4, column=2)
						self.lab_type_e.insert(0, str(line.type))
						self.lab_kw_l = tk.Label(self.detailframe, text="kW").grid(row=5, column=1)
						self.lab_kw_e = tk.Entry(self.detailframe, text="", width = 50)
						self.lab_kw_e.grid(row=5, column=2)
						self.lab_kw_e.insert(0, str(line.kw))
						self.lab_rpm_l = tk.Label(self.detailframe, text="rpm").grid(row=6, column=1)
						self.lab_rpm_e = tk.Entry(self.detailframe, text="", width = 50)
						self.lab_rpm_e.grid(row=6, column=2)
						self.lab_rpm_e.insert(0, str(line.rpm))
						self.lab_pms_l = tk.Label(self.detailframe, text="PMS").grid(row=7, column=1)
						self.lab_pms_e = tk.Entry(self.detailframe, text="", width = 50)
						self.lab_pms_e.grid(row=7, column=2)
						self.lab_pms_e.insert(0, str(line.pms))
						self.lab_info_l = tk.Label(self.detailframe, text="Info").grid(row=8, column=1)
						self.lab_info_e = tk.Entry(self.detailframe, text="", width = 50)
						self.lab_info_e.grid(row=8, column=2)
						self.lab_info_e.insert(0, str(line.info))
						self.lab_norm_l = tk.Label(self.detailframe, text="Norm").grid(row=9, column=1)

						self.standardlist = list(q_run(connD,"select standard,id from standards order by standard"))
						standards = column(self.standardlist,0)

						self.lab_norm_e = ttk.Combobox(self.detailframe, text="", values=standards, width = 45)
						self.lab_norm_e.grid(row=9, column=2)
						self.lab_norm_e.insert(0, str(line.norm))
						self.lab_drivenby_l = tk.Label(self.detailframe, text="Drivenby").grid(row=10, column=1)
						self.lab_drivenby_e = tk.Entry(self.detailframe, text="", width = 50)
						self.lab_drivenby_e.grid(row=10, column=2)
						self.lab_drivenby_e.insert(0, str(line.drivenby))
						self.lab_meas_condition_l = tk.Label(self.detailframe, text="Meas condition").grid(row=11, column=1)
						self.lab_meas_condition_e = tk.Entry(self.detailframe, text="", width = 50)
						self.lab_meas_condition_e.grid(row=11, column=2)
						self.lab_meas_condition_e.insert(0, str(line.meas_condition))
						self.lab_cm_l = tk.Label(self.detailframe, text="CM").grid(row=12, column=1)
						self.lab_cm_e = ttk.Combobox(self.detailframe, text="", values=["True","False"], width = 45)
						self.lab_cm_e.grid(row=12, column=2)
						self.lab_cm_e.insert(0, str(line.cm))
						self.lab_interval_type_l = tk.Label(self.detailframe, text="Interval type").grid(row=13, column=1)
						self.lab_interval_type_e = ttk.Combobox(self.detailframe, text="", values=["Day","Week","Month"], width = 45)
						self.lab_interval_type_e.grid(row=13, column=2)
						self.lab_interval_type_e.insert(0, str(line.interval_type))
						self.lab_interval_length_l = tk.Label(self.detailframe, text="Interval_length").grid(row=14, column=1)
						self.lab_interval_length_e = tk.Entry(self.detailframe, text="", width = 50)
						self.lab_interval_length_e.grid(row=14, column=2)
						self.lab_interval_length_e.insert(0, str(line.interval_length))
						self.updatebut = tk.Button(self.detailframe,text = "Update device data",command = updatedevice)
						self.updatebut.grid(row=15, column=2)

			self.connD = connD
			self.structuresort = True
			self.sortbutton = Button(parent,text = 'Change sort', command = lambda: self.reloadquerry(self.structuresort,shipid,connD))
			self.sortbutton.pack(side = TOP, anchor = W)
			self.deviceslistbox = Listbox(parent, exportselection=False)
			self.deviceslistbox.config(width=0)
			self.detailframe = Frame(parent)
			self.detailframe.pack(side=RIGHT, anchor=W, fill=BOTH, expand = 1)
			self.reloadquerry(self.structuresort,shipid,connD)
			self.deviceslistbox.bind('<Double-Button>', getdetails)
			parent.pack(side=LEFT)
	class PointsFrame:
		def AddPoint(self):
			querry = "select max(sort) from points where id = {}".format(self.devid)
			maxsort = list(q_run(self.connD, querry))[0][0]

			querry = "insert into points(id,point,sort,visible) values ({},(select max(_id_)+1 from points),{}, True)".format(self.devid,maxsort+1)
			print(querry)
			q_run(self.connD, querry)
			self.reloadquerry(self.structuresort, self.shipid, self.connD, False)
			self.makecontrols(self.devname, self.connD)
		def UploadPoints(self):
			testlist = list()
			testlist.clear()
			for i in self.CombPointList:
				testlist.append(i.cbox.get())
			if (any(testlist.count(x) > 1 for x in testlist)) == True:
				messagebox.showinfo("Brak", 'Uplooad aborted. Duplicate point names')
			else:
				counter = -1
				for i in tqdm(self.CombPointList):
					counter +=1
					point = i.cbox.get()
					bearing = self.CombBearingList[counter].showvalue
					if str(bearing) == 'None': bearing = 'Null'
					else:bearing = "'{}'".format(bearing)
					seal = self.CombBearingSealList[counter].showvalue
					if str(seal) == 'None': seal = 'Null'
					else:seal = "'{}'".format(seal)
					add = self.CombBearingAddList[counter].showvalue
					if str(add) == 'None': add = 'Null'
					else:add = "'{}'".format(add)
					visible = self.CombVisibleList[counter].showvalue
					if self.CombVisibleList[counter].showvalue == 'None':self.CombVisibleList[counter].showvalue = 'False'

					try:
						querry = "select point from points where sort = {} and id = {}".format( counter+1,self.devid)
						temppoint = list(q_run(self.connD, querry))[0][0]
					except:
						temppoint = 'NONE'

					if temppoint != 'NONE':
						querry = "update points set point = 'TEMPCHANGE' where point = '{}' and id = {}".format(point,self.devid)
						q_run(self.connD, querry)





					querry = "update points set point = '{}',visible = '{}' where sort = {} and id = {}".format(point,self.CombVisibleList[counter].showvalue, counter+1,self.devid)
					q_run(self.connD, querry)







					if temppoint != 'NONE':
						querry = "update points set point = '{}' where point = 'TEMPCHANGE' and id = {}".format(temppoint,self.devid)
						q_run(self.connD, querry)



					if point != i.showvalue:
						querry = "update measurements_low set point = '{}' where point = '{}' and id = {}".format(point,i.showvalue,self.devid)
						q_run(self.connD, querry)
					querry1 = "update bearings set bearing ={}, seal = {}, additional = {} where id = {} and point = '{}' " \
							 "returning bearing,seal,additional ".format(bearing,seal,add,self.devid,point)
					updates = q_run(self.connD,querry1)
					if len(updates) == 0:
						querry = "INSERT INTO bearings (id,point,bearing,seal,additional)" \
								 " VALUES ({},'{}',{},{},{}) ".format(self.devid,point,bearing,seal,add)
						q_run(self.connD, querry)

					else:
						querry = "update bearings set bearing ={}, seal = {}, additional = {} where id = {} and point = '{}' " \
								  .format(bearing, seal, add, self.devid, point)
						q_run(self.connD, querry)

				self.reloadquerry(self.structuresort, self.shipid, self.connD,False)
				self.makecontrols(self.devname, self.connD)
		def DeletePoint(self):

			point = (self.CombPointList[len(self.CombPointList)-1].showvalue)
			querry = "select * from measurements_low where id = {} and point = '{}' ".format(self.devid,point)
			if len(q_run(self.connD,querry)) == 0:
				querry = "delete from points where id ={} and point = '{}'".format(self.devid,point)
				q_run(self.connD,querry)
				self.reloadquerry(self.structuresort, self.shipid, self.connD, False)
				self.makecontrols(self.devname, self.connD)
			else:
				messagebox.showinfo("Brak", 'Delete not aviable, there are measurements for point {}'.format(point))
		def reloadquerry(self, structuresort, shipid, connD,chagesort):
			if chagesort == False:
				if structuresort == True: structuresort = False
				else: structuresort = True
			if structuresort == True:
				querry = """select dev.id, name, pts.point, bea.bearing,bea.seal,bea.additional, pts.sort,pts.visible
						from points pts
						left join bearings bea on pts.id = bea.id and pts.point = bea.point
						left join devices dev on pts.id = dev.id
						left join ds_structure dss on cast(dev.id as text) = dss.id
						
						where pts.id IN (select id from devices where parent = {})
						order by dev.name,pts.sort""".format(str(shipid))
				ans = q_run(connD, querry)

				self.structuresort = False
			else:
				querry = """select dev.id, name, pts.point, bea.bearing,bea.seal,bea.additional, pts.sort,pts.visible
							from points pts
							left join bearings bea on pts.id = bea.id and pts.point = bea.point
							left join devices dev on pts.id = dev.id
							left join ds_structure dss on cast(dev.id as text) = dss.id
							where pts.id IN (select id from devices where parent = {})
							order by dss.sort,pts.sort""".format(str(shipid))
				ans = q_run(connD, querry)

				self.structuresort = True
			self.devdata = list()
			self.devdata.clear()
			for item in ans:
				self.devdata.append(item)
			self.loadpoints()
		def loadpoints(self):
			self.deviceslistbox.delete(0, END)
			checkdevlist = list()
			checkdevlist.clear()
			devlist.clear()

			for line in self.devdata:
				dev = device()
				dev.id = str(line[0])
				dev.name = str(line[1])
				dev.point = str(line[2])
				dev.bearing = str(line[3])
				dev.seal = str(line[4])
				dev.additional = str(line[5])
				dev.sort = str(line[6])
				dev.visible = str(line[7])
				devlist.append(dev)
				if line[1] not in checkdevlist:
					self.deviceslistbox.insert(END, line[1])
					checkdevlist.append(line[1])

			self.deviceslistbox.pack(fill=BOTH, expand = 1)
		def makecontrols(self,devname,connD):
			querry = "select id from devices where name = '{}' and parent = {}".format(devname,self.shipid)
			self.devid = list(q_run(connD,querry))[0][0]
			querry = "select point,visible from points where id =(select id from devices where name = '{}' and parent = {}) order by sort".format(devname,self.shipid)
			pointslist = column(list(q_run(connD,querry)),0)
			querry ="select bearing from bearings_freq group by bearing order by bearing"
			bearingslist = column(list(q_run(connD, querry)), 0)
			querry ="select seal from bearings_seals  group by seal order by seal"
			seallist = column(list(q_run(connD, querry)), 0)
			querry ="select add from bearings_add group by add order by add"
			addlist = column(list(q_run(connD, querry)), 0)
			visiblelist = ['True','False']

			for widget in self.detailframe.winfo_children():
				widget.destroy()
			self.CombPointList = list()
			self.CombPointList.clear()
			self.CombBearingList = list()
			self.CombBearingList.clear()
			self.CombBearingSealList = list()
			self.CombBearingSealList.clear()
			self.CombBearingAddList = list()
			self.CombBearingAddList.clear()
			self.CombVisibleList = list()
			self.CombVisibleList.clear()
			c=0
			self.uploadbutton = tk.Button(self.detailframe,text = 'Upload points', command = self.UploadPoints)
			self.uploadbutton.grid(row = c, column = 0)
			for line in devlist:
				if str(line.name) == str(devname):
					c+=1
					self.namelab = tk.Label(self.detailframe, text=str(line.sort))
					self.namelab.grid(row=c, column=0)
					self.CombPointList.append(PointComboboxObject(self.detailframe,pointslist,c,self))
					self.CombBearingList.append(BearingComboboxObject(self.detailframe,line.bearing, c,2, bearingslist))
					self.CombBearingSealList.append(
						BearingComboboxObject(self.detailframe, line.seal, c, 3, seallist))
					self.CombBearingAddList.append(BearingComboboxObject(self.detailframe, line.additional, c,4, addlist))
					self.CombVisibleList.append(BearingComboboxObject(self.detailframe, line.visible, c, 5, visiblelist))



			self.addbutton = tk.Button(self.detailframe, text='Add point', command = self.AddPoint)
			self.addbutton.grid(row=c+1, column=0)

			self.delbutton = tk.Button(self.detailframe, text='Delete point', command = self.DeletePoint)
			self.delbutton.grid(row=c+1, column=1)
		def __init__(self, parent, shipid, connD):
			def getdetails(evt):
				w = evt.widget
				index = int(w.curselection()[0])
				devname = w.get(index)
				self.devname = devname
				self.makecontrols(devname,connD)
			self.connD = connD
			self.shipid = shipid
			self.structuresort = True
			self.sortbutton = Button(parent,text = 'Change sort', command = lambda: self.reloadquerry(self.structuresort,shipid,connD,True))
			self.sortbutton.pack(side = TOP, anchor = W)
			self.deviceslistbox = Listbox(parent, exportselection=False)
			self.deviceslistbox.config(width=0)
			self.detailframe = Frame(parent,borderwidth = 1)
			self.detailframe.pack(side=RIGHT, anchor=W, fill=BOTH, expand = 1)
			self.reloadquerry(self.structuresort, shipid, connD,True)
			self.deviceslistbox.bind('<Double-Button>',getdetails )
			parent.pack(side=LEFT)
	class StructFrame:
		def reloadquerrys(self,shipid,connD):
			querry = """
			select dss.id, dev.name,dss.sort from ds_structure dss 
			left join devices dev on cast(dev.id as text) = dss.id
			where dss.parent = {} order by dss.sort
			""".format(shipid)
			self.devlist = list(q_run(connD,querry))
			self.loaddevices()
		def loaddevices(self):
			for line in self.devlist:
				if str(line[1]) != 'None':
					self.deviceslistbox.insert(END, '{}@{}'.format(line[1],line[0]) )
				else:
					if str(line[2])[-5:] == '00.00':
						self.deviceslistbox.insert(END, line[0])
						self.deviceslistbox.itemconfig(END, fg='purple')
					elif str(line[2])[-3:] == '.00':
						self.deviceslistbox.insert(END, line[0])
						self.deviceslistbox.itemconfig(END, fg='blue')
			self.deviceslistbox.pack(fill=BOTH, expand = 1)
			savebutton = tk.Button(self.detailframe,text = 'Save structure')
			savebutton.config(command = self.savestruct)
			savebutton.pack(side=TOP, anchor=W)

			adddevicebutton = tk.Button(self.detailframe,text = 'Add device')
			adddevicebutton.config(command = self.adddevice)
			adddevicebutton.pack(side=TOP, anchor=W)

			addplaceebutton = tk.Button(self.detailframe,text = 'Add place')
			addplaceebutton.config(command = self.addplace)
			addplaceebutton.pack(side=TOP, anchor=W)

			addgroupbutton = tk.Button(self.detailframe,text = 'Add group')
			addgroupbutton.config(command = self.addgroup)
			addgroupbutton.pack(side=TOP, anchor=W)

			deletebutton = tk.Button(self.detailframe,text = 'Delete')
			deletebutton.config(command = self.delete)
			deletebutton.pack(side=TOP, anchor=W)
		def savestruct(self):
			class counter:
				def __init__(self):
					self.lvl1 = 0
					self.lvl2 = 0
					self.lvl3 = 0
				def add(self,lvl):
					if lvl == 1:
						self.lvl1 += 1
						self.lvl2 = 0
						self.lvl3 = 0
					if lvl == 2:
						self.lvl2 += 1
						self.lvl3 = 0
					if lvl == 3:
						self.lvl3 += 1

					if len(str(self.lvl1)) == 1:strlvl1 = '0{}'.format(self.lvl1)
					else:strlvl1 = str(self.lvl1)
					if len(str(self.lvl2)) == 1:strlvl2 = '0{}'.format(self.lvl2)
					else:strlvl2 = str(self.lvl2)
					if len(str(self.lvl3)) == 1:strlvl3 = '0{}'.format(self.lvl3)
					else:strlvl3 = str(self.lvl3)
					cc = '{}.{}.{}'.format(strlvl1,strlvl2,strlvl3)
					return cc
			i = -1
			dsstruct = list()
			dsstruct.clear()
			cc = counter()
			for item in enumerate(self.deviceslistbox.get(0, END)):
				i+=1
				color = self.deviceslistbox.itemcget(i, "fg")
				if str(color) == 'purple':
					tup = [cc.add(1), item[1]]
					dsstruct.append(tup)
					pass
				elif str(color) == 'blue':
					tup = [cc.add(2), item[1]]
					dsstruct.append(tup)
					pass
				else:
					at = item[1].find('@')
					tup = [cc.add(3), item[1][at+1:]]
					dsstruct.append(tup)

			querry = "UPDATE ds_structure set parent = 999999 where parent = {}".format(self.shipid)
			q_run(self.connD, querry)
			try:
				for line in tqdm(dsstruct):
					querry = "insert into ds_structure(parent,sort,id) values ({},'{}','{}')".format(self.shipid,line[0],line[1])
					q_run(self.connD,querry)
				querry = "delete from ds_structure where parent = 999999"
				q_run(self.connD, querry)
			except:
				querry = "UPDATE ds_structure set parent = {} where parent = 999999".format(self.shipid)
				q_run(self.connD, querry)
		def adddevice(self):
			try:
				idx = self.deviceslistbox.curselection()[0]
			except:
				idx = 0
			chosedevicewindow(['testuser', 'info', 'localhost'], 160, self.deviceslistbox)
		def addplace(self):
			try:
				idx = self.deviceslistbox.curselection()[0]
			except:
				idx = 0
			place = simpledialog.askstring("Add place", "Enter place name:")
			self.deviceslistbox.insert(idx,  place)
			self.deviceslistbox.itemconfig(idx, fg='purple')
		def addgroup(self):
			try:
				idx = self.deviceslistbox.curselection()[0]
			except:
				idx = 0
			group = simpledialog.askstring("Add group", "Enter group name:")
			self.deviceslistbox.insert(idx, group)
			self.deviceslistbox.itemconfig(idx, fg='blue')
		def delete(self):
			try:
				idx = self.deviceslistbox.curselection()[0]
				self.deviceslistbox.delete(idx)
			except:
				idx = 0
		def __init__(self,parent,shipid,connD):
			def getdetails(evt):
				w = evt.widget
				index = int(w.curselection()[0])
				devname = w.get(index)
			self.shipid = shipid
			self.connD= connD
			self.deviceslistbox = DragDropListbox(parent, exportselection=False)
			self.deviceslistbox.config(width=0)
			self.detailframe = Frame(parent,borderwidth = 1)
			self.detailframe.pack(side=RIGHT, anchor=W, fill=BOTH, expand = 1)

			self.reloadquerrys(shipid,connD)
	def __init__(self,connD):
		def getships(evt):
			w = evt.widget
			index = int(w.curselection()[0])
			shipname = w.get(index)
			self.Applistbox.delete(0, 'end')
			makeships(shipname)
		def makeships(shipname):
			querry = "select name from main where parent =(select id from main where name = '" + str(
				shipname) + "' limit 1) order by name"
			ships = q_run(connD, querry)
			self.Shiplistbox.delete(0, 'end')
			for line in ships:
				self.Shiplistbox.insert(END, line[0])
		def getaps(evt):
			w = evt.widget
			index = int(w.curselection()[0])
			shipname = w.get(index)
			querry = "(select id from main where name = '{}')".format(str(shipname))
			self.shipid = list(q_run(connD, querry))[0][0]
			self.Applistbox.delete(0, 'end')
			self.Applistbox.insert(END, 'Crosstable')
			self.Applistbox.insert(END, 'Devices')
			self.Applistbox.insert(END, 'Points')
			self.Applistbox.insert(END, 'Structure')
		def makeframe(evt):
			w = evt.widget
			index = int(w.curselection()[0])
			framename = w.get(index)
			for widget in self.Workframe.winfo_children():
				widget.destroy()
			if str(framename) == 'Devices':
				self.DevicesFrame(self.Workframe,self.shipid,connD)
			if str(framename) == 'Points':
				self.PointsFrame(self.Workframe, self.shipid, connD)
			if str(framename) == 'Structure':
				self.StructFrame(self.Workframe,self.shipid, connD)
		self.connD = connD
		self.shipid = ''
		self.stWindow = tk.Tk()
		self.stWindow.title("Structure")
		self.Ownerlistbox = Listbox(self.stWindow, exportselection=False)
		self.Ownerlistbox.config(width=0)
		self.Ownerlistbox.bind('<Double-Button>', getships)
		self.Shiplistbox = Listbox(self.stWindow, exportselection=False)
		self.Shiplistbox.config(width=0)
		self.shipid = ''
		self.Shiplistbox.bind('<Double-Button>', getaps)
		self.Applistbox = Listbox(self.stWindow, exportselection=False)
		self.Applistbox.config(width=0)
		self.Applistbox.bind('<Double-Button>',makeframe)
		self.Workframe = Frame(self.stWindow, borderwidth = 1)
		querry = "select name,id from main where parent = 1 order by name"
		resultrr = q_run(connD, querry)
		for line in resultrr:
			self.Ownerlistbox.insert(END, line[0])
		self.Ownerlistbox.pack(side=LEFT, fill=BOTH)
		self.Shiplistbox.pack(side=LEFT, fill=BOTH)
		self.Applistbox.pack(side=LEFT, fill=BOTH)
		self.Workframe.pack(side=LEFT, fill=BOTH)
		self.stWindow.mainloop()



LogApplication()
ModelMakerWindow(['filipb','@infomarine','localhost'])
