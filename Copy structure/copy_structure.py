
#adasdsad
### TEST


import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
from postgresquerrys import *
parent = 31
username = 'filipb'
password = ' ' ###########NIE DZIAŁA < TRZEBA ZMIENIC DODAWANIE FLAGI VISIBLE W PUNKTACH, I nie force dodawanie id
host = 'localhost'
connD = [username,password,host]
	
def ShowStructWindow(connD,parent):
	Window = tk.Tk()
	Window.title("Copy")
	querry = "SELECT id from ds_structure where parent = '" + str(parent) + "' order by sort"
	sortquerry = q_run(connD, querry)
	querry = "select id,name from devices where parent = '" + str(parent) + "'"
	devnamesquerry = q_run(connD, querry)
	mylist = Listbox(Window)
	mylist.config(width=100)

	for x in sortquerry:
		i=0
		for xx in devnamesquerry:
			if x[0].isnumeric() == False:
				mylist.insert(END,str(x[0]))
				break
			if str(x[0]) == str(xx[0]):
				mylist.insert(END,str(xx[1]))
				break

	mylist.pack(side = TOP)
	okbutton = tk.Button(Window, text = 'COPY')
	okbutton.pack(side = TOP)
	Window.mainloop()


def copyStruct(connD,parent):
	
	class measurements_low(object): 
		def __init__(self):
			self.parent = list()
			self.id = list()
			self.point = list()
			self.type = list()
			self.unit = list()	
			self.date = list()
			self.value = list()			
			self.raport_number = list()
		def getQuerrys(self):
			querry = "select parent,id,point,type,unit,date,value,raport_number from measurements_low where id is not null and raport_number is not null and parent =  " + str(parent)
			measquerry = q_run(connD, querry)
			p=0
			for line in measquerry:
				self.parent.append(line[0])
				self.id.append(line[1])
				self.point.append(line[2]) 
				self.type.append(line[3]) 
				self.unit.append(line[4]) 
				self.date.append(line[5]) 
				self.value.append(line[6]) 			
				self.raport_number.append(line[7]) 
				p += 1
		def upload(self):
			pbar = tk.Tk()
			pbar.title("Measurements")
			progress_bar = ttk.Progressbar(pbar,orient = 'horizontal',lengt = 286, mode = 'determinate')
			progress_bar['maximum'] =len(self.id)
			progress_bar.pack()	
			p=0	
			for line in self.id:
				progress_bar['value'] = p
				progress_bar.update()
				querry = """insert into measurements_low(parent,id,point,type,unit,date,value,raport_number) 
values (""" + str(self.parent[p]) + ",'" + str(line) + "','" +str(self.point[p]) + "','" +str(self.type[p]) + "','" + """
""" + str(self.unit[p]) + "','" + str(self.date[p]) + "','" +str(self.value[p]) + "','" +str(self.raport_number[p]) + "')" 
				q_run(connD,querry)
				p += 1
			pbar.destroy()
	class remarks(object): 
		def __init__(self):
			self.parent = list()
			self.id = list()
			self.remark = list()
			self.documentdate = list()
			self.raport_number = list()
			self.sended = list()
		def getQuerrys(self):
			querry = "select parent,id,remark,documentdate,raport_number,sended from remarks where raport_number is not null and parent =  " + str(parent)
			measquerry = q_run(connD, querry)
			p=0
			for line in measquerry:
				self.parent.append(line[0])
				self.id.append(line[1])
				self.remark.append(line[2]) 
				self.documentdate.append(line[3]) 
				self.raport_number.append(line[4]) 
				self.sended.append(line[5]) 
				p += 1
		def upload(self):
			pbar = tk.Tk()
			pbar.title("Remarks")
			progress_bar = ttk.Progressbar(pbar,orient = 'horizontal',lengt = 286, mode = 'determinate')
			progress_bar['maximum'] =len(self.id)
			progress_bar.pack()	
			p=0	
			for line in self.id:
				progress_bar['value'] = p
				progress_bar.update()
				if str(self.sended[p]) == 'None': self.sended[p] = 'Null'
				querry = """insert into remarks(parent,id,remark,documentdate,raport_number,sended) 
values (""" + str(self.parent[p]) + ",'" + str(self.id[p]) + "','" +str(self.remark[p]) + "','" +str(self.documentdate[p]) + "','" + str(self.raport_number[p]) + "'," + str(self.sended[p]) + ")" 
				print(querry)
				q_run(connD,querry)
				p += 1
			pbar.destroy()				
	class feedbacks(object):
		def __init__(self):
			self.parent = list()
			self.id = list()
			self.feedback = list()
			self.documentdate = list()
			self.fdbflag = list()
			self.costflag = list()
			self.raport_number = list()
			self.price = list()
			self.low = list()
			self.high = list()
		def getQuerrys(self):
			querry = "select parent,id,feedback,documentdate,fdbflag,costflag, raport_number, price, low, high from feedbacks where raport_number is not null and parent =  " + str(parent)
			measquerry = q_run(connD, querry)
			p=0
			for line in measquerry:
				self.parent.append(line[0])
				self.id.append(line[1])
				self.feedback.append(line[2]) 
				self.documentdate.append(line[3]) 
				self.fdbflag.append(line[4]) 
				self.costflag.append(line[5])
				self.raport_number.append(line[6]) 
				self.price.append(line[7]) 
				self.low.append(line[8]) 
				self.high.append(line[9]) 
				p += 1
		def upload(self):
			pbar = tk.Tk()
			pbar.title("Remarks")
			progress_bar = ttk.Progressbar(pbar,orient = 'horizontal',lengt = 286, mode = 'determinate')
			progress_bar['maximum'] =len(self.id)
			progress_bar.pack()	
			p=0	
			for line in self.id:
				progress_bar['value'] = p
				progress_bar.update()
				if str(self.fdbflag[p]) == 'None': self.fdbflag[p] = 'Null'
				if str(self.costflag[p]) == 'None': self.costflag[p] = 'Null'
				

				if str(self.price[p]) == 'None': self.price[p] = 'Null' 
				else: self.price[p] = "ARRAY" + str(self.price[p])
				if str(self.low[p]) == 'None': self.low[p] = 'Null' 
				else: self.low[p] = "ARRAY" +  str(self.low[p])
				if str(self.high[p]) == 'None': self.high[p] = 'Null' 
				else: self.high[p] = "ARRAY" +  str(self.high[p])
				
				
				
				querry = """insert into feedbacks(parent,id,feedback,documentdate,fdbflag,costflag,raport_number,price,low,high) 
values (""" + str(self.parent[p]) + ",'" + str(self.id[p]) + "','" +str(self.feedback[p]) + "','" +str(self.documentdate[p]) + "'," + """
""" + str(self.fdbflag[p]) + "," + str(self.costflag[p]) + ",'" + str(self.raport_number[p]) + "'," +str(self.price[p]) + "," + """ 
""" + str(self.low[p]) + "," + str(self.high[p]) + ")"

				q_run(connD,querry)
				p += 1
			pbar.destroy()				
	class points(object):
		def __init__(self):
			self.id = list()
			self.point = list()
			self.bearing = list()
			self.seal = list()
			self.additional = list()
			self.sort = list()
		def getQuerrys(self):
			querry = """select pts.id, pts.point, brg.bearing, brg.seal, brg.additional, pts.sort
						from points as pts
						left join bearings as brg on pts.id = brg.id and pts.point = brg.point
						where pts.id in 
						(select id from devices where parent = """+ str(parent) + """)
						order by pts.id,pts.sort"""
			pointsquerry = q_run(connD, querry)
			for line in pointsquerry:
				self.id.append(line[0])
				self.point.append(line[1])
				self.bearing.append(line[2])
				self.seal.append(line[3])
				self.additional.append(line[4])
				self.sort.append(line[5])
		def uploadNewPoints(self):
			pbar = tk.Tk()
			pbar.title("Points and bearings")
			progress_bar = ttk.Progressbar(pbar,orient = 'horizontal',lengt = 286, mode = 'determinate')
			progress_bar['maximum'] =len(self.sort)
			progress_bar.pack()	
			p=0	

			for line in self.id:
				progress_bar['value'] = p
				progress_bar.update()
				querry = "insert into points(id,point,sort) values ('" +str(line)+ "','" + str(self.point[p]) + "','" +str(self.sort[p]) + "')"
				q_run(connD,querry)
				if str(self.bearing[p]) == 'None': self.bearing[p] = ''
				if str(self.seal[p]) == 'None': self.seal[p] = ''
				if str(self.additional[p]) == 'None': self.additional[p] = ''
				querry = "insert into bearings(id,point,bearing,seal,additional) values ('" +str(line) + "','" + str(self.point[p]) + "','" +str(self.bearing[p]) + "','" + str(self.seal[p]) + "','" + str(self.additional[p]) + "')"
				q_run(connD,querry)

				p += 1
			pbar.destroy()
	class struct(object):
		def __init__(self):
			self.ownerid = []
			self.newid = []
			self.sort = list()
			self.name = list()
			self.copyid = list()
			self.copydrivenby=list()
			self.pasteid = list()
			self.pastedrivenby = list()
			self.drivenbystruct = list()
			self.model = list()
			self.type = list()
			self.points = list()
			self.kw = list()
			self.rpm = list()
			self.pms = list()
			self.info = list()
			self.norm = list()
			self.meas_condition = list()
			self.cm = list()
			self.routename = list()
			self.shiptype = []
			self.length = []
			self.bradth = []
			self.imo = []
			self.catStructString = list()
			self.catStructSort = list()
		def getQuerrys(self):
			querry = "select parent from main where id =" + str(parent) 
			self.ownerid = q_run(connD, querry)[0][0]
			querry = "select shiptype, lenght, bradth, imo from shipsdata where shipid = " + str(parent) 
			self.shiptype = q_run(connD, querry)[0][0]	
			self.length = q_run(connD, querry)[0][1]	
			self.bradth = q_run(connD, querry)[0][2]
			self.imo = q_run(connD, querry)[0][2]
			querry = "select sort, id from ds_structure where parent =" + str(parent)
			namesortlist = q_run(connD, querry)
			for line in namesortlist:
				if str(line[0][-3:]) == '.00' :
					self.catStructString.append(str(line[1]))
					self.catStructSort.append(str(line[0]))
			querry = """ select
							dss.sort, dss.id, 
							dev.drivenby, dev.name,
							
							dev.model,dev.type,dev.points,dev.kw,dev.rpm,dev.pms,dev.info,dev.norm,dev.meas_condition,dev.cm,
							css.nameindevice
							from 
							ds_structure as dss
							left join devices as dev on CAST(dss.id as integer) = dev.id
							left join crosstable as css ON dss.parent = css.parent and CAST(dss.id as integer) = css.id
							where dss.id ~ '^\d+(\.\d+)?$' and dss.parent = """+ str(parent) + """
							order by sort """
			structquerry = q_run(connD, querry)
			for line in structquerry:
				(self.sort).append(line[0])
				(self.copyid).append(line[1])
				if str(line[2]) == 'None' :
					(self.copydrivenby).append('0')
				else:
					(self.copydrivenby).append(line[2])

				(self.name).append(line[3])
				(self.model).append(line[4])
				(self.type).append(line[5])
				(self.points).append(line[6])
				(self.kw).append(line[7])
				(self.rpm).append(line[8])
				(self.pms).append(line[9])
				(self.info).append(line[10])
				(self.norm).append(line[11])
				(self.meas_condition).append(line[12])
				(self.cm).append(line[13])
				self.routename.append(line[14])
		def copyStruct(self):
		
			querry = "select max(id) from devices"
			idquerry = q_run(connD, querry)
			id = idquerry[0][0]
		
			id = int(id) + 1
			i = 0 ## GET ID /// DOPISAC ZEBY POBIERAŁO NAZWE I INNE DANE URZADZENIA
			for line in self.sort:
				self.pasteid.append(id)
				id += 1
				
			i=0 ### GET DRIVEN BY STRUCT PLACE
			for line in self.sort:
				
				if str(self.copydrivenby[i]).strip() == '0':
					self.drivenbystruct.append('0')
				else:
					j = 0
					for drivenby in self.copyid:
						
						if str(self.copydrivenby[i]) == drivenby:
							
							self.drivenbystruct.append(self.sort[j])
						j += 1
					j = 0
				i += 1
	
			## GET NEW DRIVEN BY 
			for line in self.drivenbystruct: #iteracja miejsca w strukturze drivenby
				i=-1
				for line2 in self.sort: #iteracja miejsca w strukturze
					i += 1
					#print(line)
					#print(line2)
					if str(line) == '0':
						self.pastedrivenby.append('0') 
						break
					elif str(line) == str(line2):
						self.pastedrivenby.append(self.pasteid[i]) 
						break
					# else:
						# self.pastedrivenby.append('0') 
						

		def InputWindow(self):
			inputwindow = Tk()
			l=Label(inputwindow, text = "Ship Name")
			l.pack()
			e = Entry(inputwindow)
			e.pack()
			e.focus_set()
			def pasteStruct(self,newname):
				querry = 'Select max(id) from main'
				maxid = q_run(connD,querry)
				self.newid = int(maxid[0][0]) + 1
				newid = int(maxid[0][0]) + 1
				querry = 'insert into main(id,parent,name) values (' + str(newid) + ',' + str(self.ownerid)+ ",'" + str(newname) + "')"
				q_run(connD,querry)
				querry = """insert into shipsdata(shipid, shiptype, lenght, bradth, imo) values 
				('"""  + str(newid) + "','" + str(self.shiptype) + "','" + str(self.length) + "','" + str(self.bradth) + "','" + str(self.imo) +  "')"
				q_run(connD,querry)
				pbar = tk.Tk()
				pbar.title("Devices")
				progress_bar = ttk.Progressbar(pbar,orient = 'horizontal',lengt = 286, mode = 'determinate')
				progress_bar['maximum'] =len(self.sort)
				progress_bar.pack()	
				p = 0 		
				for line in self.sort:
					progress_bar['value'] = p
					progress_bar.update()
					querry = """insert into devices(id, parent, name, model, type,points,kw,rpm,pms,info,norm, meas_condition, drivenby, cm) values 
('"""  + str(self.pasteid[p]) + "','" + str(newid) + "','" + str(self.name[p]) + "','" + str(self.model[p]) + """
""" + "','" + str(self.type[p]) + "','" + str(self.points[p]) + "','" + str(self.kw[p]) + "','" + str(self.rpm[p]) + """
""" + "','" + str(self.pms[p]) + "','" + str(self.info[p]) + "','" + str(self.norm[p]) + "','" + str(self.meas_condition[p]) + """
""" + "','" + str(self.pastedrivenby[p]) + "'," + str(self.cm[p]) + ")" 
					q_run(connD,querry)
					### tu chyba brakuje drivenby - trzeba dac i tak oddzielnie jako update ? 
					
					
					## Gdzies tu trzeba przeniesc copy
					
					
					
					querry = "insert into ds_structure(parent,sort,id) values ('" + str(newid) + "','" + str(self.sort[p]) + "','" +str(self.pasteid[p]) + "')"
					q_run(connD,querry)
					querry = "insert into crosstable(parent,nameindevice,id) values ('" + str(newid) + "','" + str(self.routename[p]) + "','" +str(self.pasteid[p]) + "')"
					q_run(connD,querry)
					p += 1
				p=0	
				for structStrLine in self.catStructSort:
					querry = "insert into ds_structure(parent,sort,id) values ('" + str(newid) + "','" + str(self.catStructSort[p]) + "','" +str(self.catStructString[p]) + "')"
					q_run(connD,querry)
					p += 1
				pbar.destroy()
			def callback():
				newname = str(e.get()) 
				inputwindow.destroy()
				pasteStruct(self,newname)
				
			b = Button(inputwindow, text = "OK", width = 10, command = callback)
			b.pack()
			mainloop()
	def updatePointID(y,x):
		i = -1
		for line1 in y.id:
			i +=1
			j = -1
			for line2 in x.copyid:
				j += 1
				if str(line1) == str(line2):
					y.id[i] = x.pasteid[j]
	
	def updateParentId(to_change,structtable):
		#to_change.id
		#to_change.parent
		#structtable.copyid
		#structtable.pasteid
		#structtable.ownerid

		i = -1
		for line1 in to_change.id:
			i +=1
			to_change.parent[i]=structtable.newid
			j = -1
			for line2 in structtable.copyid:
				j += 1
				if str(line1) == str(line2):
					to_change.id[i] = structtable.pasteid[j]
			
	x = struct()
	x.getQuerrys()
	x.copyStruct()
	x.InputWindow()
	print('przedpoints')
	y = points()
	print('przedgwtquerrys')
	y.getQuerrys()
	print('przedupdatepoints')
	updatePointID(y,x)
	print('przeduploadpoints')
	y.uploadNewPoints()
	
	ml = measurements_low()
	ml.getQuerrys()
	rm = remarks()
	rm.getQuerrys()
	fd = feedbacks()
	fd.getQuerrys()
	
	updateParentId(ml,x)
	updateParentId(rm,x)
	updateParentId(fd,x)
	#ml.upload()
	rm.upload()
	fd.upload()
	i=0
	# for test in x.sort:
		# print (str(x.sort[i])+' ID: '+str(x.copyid[i])+' NORM: '+str(x.copydrivenby[i]))
		# i +=1
		# if i == 10:break
	
	#print (len(ml.id))
	# for test in ml.id:
		# print(ml.parent)

		

copyStruct(connD,parent)
