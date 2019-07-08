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
			StructWindow(connD)


devlist = list()
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
		
def column(matrix, i):
    return [row[i] for row in matrix]

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

class StructWindow:
	class DevicesFrame:
		def reloadquerry(self,structuresort,shipid,connD):
			if structuresort == True:
				querry = """select dev.id, name,model,type,kw,rpm,pms,info,norm,drivenby, meas_condition,cm,interval_type,interval_length
							from devices dev
							left join ds_structure dss on cast(dev.id as text) = dss.id
							where dev.parent ={}
							order by dss.sort""".format(str(shipid))
				ans = q_run(connD, querry)
				self.structuresort = False
			else:
				querry = "select id, name,model,type,kw,rpm,pms,info,norm,drivenby, meas_condition,cm,interval_type,interval_length from devices where parent = {} order by name".format(
					str(shipid))
				ans= q_run(connD, querry)
				self.structuresort = True
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
				self.deviceslistbox.insert(END, line[1])
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
				dev.interval_type = str(line[12])
				dev.interval_length = str(line[13])
				devlist.append(dev)

			self.deviceslistbox.pack()
		def __init__(self,parent,shipid,connD):
			def getdetails(evt):
				w = evt.widget
				index = int(w.curselection()[0])
				devname = w.get(index)
				for widget in self.detailframe.winfo_children():
					widget.destroy()
				for line in devlist:
					if str(line.name) == str(devname):

						self.title = tk.Label(self.detailframe, text='Id: '+str(line.id))
						self.title.grid(row=0, column=2)


						self.lab_name_l = tk.Label(self.detailframe, text="Name").grid(row=2, column=1)
						self.lab_name_e = tk.Entry(self.detailframe)
						self.lab_name_e.grid(row=2, column=2)
						self.lab_name_e.insert(0, str(line.name))
						self.lab_model_l = tk.Label(self.detailframe, text="Model").grid(row=3, column=1)
						self.lab_model_e = tk.Entry(self.detailframe)
						self.lab_model_e.grid(row=3, column=2)
						self.lab_model_e.insert(0, str(line.model))
						self.lab_type_l = tk.Label(self.detailframe, text="Type").grid(row=4, column=1)
						self.lab_type_e = tk.Entry(self.detailframe, text="")
						self.lab_type_e.grid(row=4, column=2)
						self.lab_type_e.insert(0, str(line.type))
						self.lab_kw_l = tk.Label(self.detailframe, text="kW").grid(row=5, column=1)
						self.lab_kw_e = tk.Entry(self.detailframe, text="")
						self.lab_kw_e.grid(row=5, column=2)
						self.lab_kw_e.insert(0, str(line.kw))
						self.lab_rpm_l = tk.Label(self.detailframe, text="rpm").grid(row=6, column=1)
						self.lab_rpm_e = tk.Entry(self.detailframe, text="")
						self.lab_rpm_e.grid(row=6, column=2)
						self.lab_rpm_e.insert(0, str(line.rpm))
						self.lab_pms_l = tk.Label(self.detailframe, text="PMS").grid(row=7, column=1)
						self.lab_pms_e = tk.Entry(self.detailframe, text="")
						self.lab_pms_e.grid(row=7, column=2)
						self.lab_pms_e.insert(0, str(line.pms))
						self.lab_info_l = tk.Label(self.detailframe, text="Info").grid(row=8, column=1)
						self.lab_info_e = tk.Entry(self.detailframe, text="")
						self.lab_info_e.grid(row=8, column=2)
						self.lab_info_e.insert(0, str(line.info))
						self.lab_norm_l = tk.Label(self.detailframe, text="Norm").grid(row=9, column=1)
						self.lab_norm_e = tk.Entry(self.detailframe, text="")
						self.lab_norm_e.grid(row=9, column=2)
						self.lab_norm_e.insert(0, str(line.norm))
						self.lab_drivenby_l = tk.Label(self.detailframe, text="Drivenby").grid(row=10, column=1)
						self.lab_drivenby_e = tk.Entry(self.detailframe, text="")
						self.lab_drivenby_e.grid(row=10, column=2)
						self.lab_drivenby_e.insert(0, str(line.drivenby))
						self.lab_meas_condition_l = tk.Label(self.detailframe, text="Meas condition").grid(row=11, column=1)
						self.lab_meas_condition_e = tk.Entry(self.detailframe, text="")
						self.lab_meas_condition_e.grid(row=11, column=2)
						self.lab_meas_condition_e.insert(0, str(line.meas_condition))
						self.lab_cm_l = tk.Label(self.detailframe, text="CM").grid(row=12, column=1)
						self.lab_cm_e = tk.Entry(self.detailframe, text="")
						self.lab_cm_e.grid(row=12, column=2)
						self.lab_cm_e.insert(0, str(line.cm))
						self.lab_interval_type_l = tk.Label(self.detailframe, text="Interval type").grid(row=13, column=1)
						self.lab_interval_type_e = tk.Entry(self.detailframe, text="")
						self.lab_interval_type_e.grid(row=13, column=2)
						self.lab_interval_type_e.insert(0, str(line.interval_type))
						self.lab_interval_length_l = tk.Label(self.detailframe, text="Interval_length").grid(row=14, column=1)
						self.lab_interval_length_e = tk.Entry(self.detailframe, text="")
						self.lab_interval_length_e.grid(row=14, column=2)
						self.lab_interval_length_e.insert(0, str(line.interval_length))
			self.structuresort = True
			self.sortbutton = Button(parent,text = 'Change sort', command = lambda: self.reloadquerry(self.structuresort,shipid,connD))
			self.sortbutton.pack(side = TOP, anchor = W)
			self.deviceslistbox = Listbox(parent, exportselection=False)
			self.detailframe = Frame(parent)
			self.detailframe.pack(side = RIGHT, anchor = W)
			self.reloadquerry(self.structuresort,shipid,connD)
			self.deviceslistbox.bind('<Double-Button>', getdetails)
			parent.pack(side=LEFT)
	class PointsFrame:
		def AddPoint(self):
			querry = "select max(sort) from points where id = {}".format(self.devid)
			maxsort = list(q_run(self.connD, querry))[0][0]
			querry = "insert into points(id,point,sort) values ({},'{}',{})".format(self.devid,'NEWPOINT',maxsort+1)
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


					querry = "update points set point = '{}',visible = '{}' where sort = {} and id = {}".format(point,self.CombVisibleList[counter].showvalue, counter+1,self.devid)
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

			self.deviceslistbox.pack(fill=BOTH)
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
			self.detailframe = Frame(parent)
			self.detailframe.pack(side=RIGHT, anchor=W)
			self.reloadquerry(self.structuresort, shipid, connD,True)
			self.deviceslistbox.bind('<Double-Button>',getdetails )
			parent.pack(side=LEFT)
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
		self.Workframe = Frame(self.stWindow, bd = 2)
		querry = "select name,id from main where parent = 1 order by name"
		resultrr = q_run(connD, querry)
		for line in resultrr:
			self.Ownerlistbox.insert(END, line[0])
		self.Ownerlistbox.pack(side=LEFT, fill=BOTH)
		self.Shiplistbox.pack(side=LEFT, fill=BOTH)
		self.Applistbox.pack(side=LEFT, fill=BOTH)
		self.stWindow.mainloop()


LogApplication()

