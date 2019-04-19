import psycopg2
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
username = 'filipb'
password = '@infomarine'
username2 = 'dbadmin'
password2 = '242QhpbS&9Fv'
host1 = '192.168.8.10'
host2 = '192.168.10.243'
connBASE = [username,password,host1]
connTARGET = [username2,password2,host2]

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
def copyharmo():
	querry = "select raport_number, shipid from reports where raport_number is not null and shipid is not null order by raport_number "
	for line in q_run(connBASE, querry):

		querry = "INSERT INTO HARMONOGRAM(shipid,report_number,pomiar,struct,datasheet,report, analysis, send_raport,remarks,feedbacks,accept,fdbrem,fdbrem2) VALUES (" +str(line[1]) + ",'" + str(line[0]) + "',True,True,True,True,True,True,True,True,True,True,True)"
		print(querry)
		q_run(connBASE, querry)

def migratestruct():
	pbars = tk.Tk()
	pbars.title("Move data")
	
	
	#BEARINGS
	labBearings = tk.Label(pbars, text = "Bearings").grid(row=0, column=0)
	beringsVar = StringVar()
	beringsVar.set('0')	
	countBearings = tk.Label(pbars,textvariable = beringsVar).grid(row=0, column=1)
	BearingsProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')
	
	#BEARINGS ADD
	labBearings_add = tk.Label(pbars, text = "Bearings_add").grid(row=1, column=0)
	berings_addVar = StringVar()
	berings_addVar.set('0')	
	countBearings_add = tk.Label(pbars,textvariable = berings_addVar).grid(row=1, column=1)
	Bearings_addProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')
	

	#BEARINGS FREQ
	labBearings_freq = tk.Label(pbars, text = "Bearings_freq").grid(row=2, column=0)
	berings_freqVar = StringVar()
	berings_freqVar.set('0')	
	countBearings_freq = tk.Label(pbars,textvariable = berings_freqVar).grid(row=2, column=1)
	Bearings_freqProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')


	#BEARINGS SEALS
	labBearings_seals = tk.Label(pbars, text = "Bearings_seals").grid(row=3, column=0)
	berings_sealsVar = StringVar()
	berings_sealsVar.set('0')	
	countBearings_seal = tk.Label(pbars,textvariable = berings_sealsVar).grid(row=3, column=1)
	Bearings_sealsProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')
	
	#costcases
	labCostcases = tk.Label(pbars, text = "Costcases").grid(row=4, column=0)
	CostcasesVar = StringVar()
	CostcasesVar.set('0')	
	countCostcases = tk.Label(pbars,textvariable = CostcasesVar).grid(row=4, column=1)
	CostcasesProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')

	#costflags
	labcostflags = tk.Label(pbars, text = "Costflags").grid(row=5, column=0)
	labcostflagsVar = StringVar()
	labcostflagsVar.set('0')	
	countcostflags = tk.Label(pbars,textvariable = labcostflagsVar).grid(row=5, column=1)
	costflagsProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')


	#crosstable
	labcrosstable = tk.Label(pbars, text = "Crosstable").grid(row=6, column=0)
	crosstableVar = StringVar()
	crosstableVar.set('0')	
	countcrosstable = tk.Label(pbars,textvariable = crosstableVar).grid(row=6, column=1)
	crosstableProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')


	#devices
	labdevices = tk.Label(pbars, text = "devices").grid(row=7, column=0)
	devicesVar = StringVar()
	devicesVar.set('0')	
	countdevices = tk.Label(pbars,textvariable = devicesVar).grid(row=7, column=1)
	devicesProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')

	#ds_structure
	labds_structure = tk.Label(pbars, text = "ds_structure").grid(row=8, column=0)
	ds_structureVar = StringVar()
	ds_structureVar.set('0')	
	countds_structure = tk.Label(pbars,textvariable = ds_structureVar).grid(row=8, column=1)
	ds_structureProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')

	#equipment
	labequipment = tk.Label(pbars, text = "equipment").grid(row=9, column=0)
	equipmentVar = StringVar()
	equipmentVar.set('0')	
	countequipment = tk.Label(pbars,textvariable = equipmentVar).grid(row=9, column=1)
	equipmentProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')

	#fdb_flags
	labfdb_flags = tk.Label(pbars, text = "fdb_flags").grid(row=10, column=0)
	fdb_flagsVar = StringVar()
	fdb_flagsVar.set('0')	
	countfdb_flags = tk.Label(pbars,textvariable = fdb_flagsVar).grid(row=10, column=1)
	fdb_flagsProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')





	#feedbacks
	labfeedbacks = tk.Label(pbars, text = "feedbacks").grid(row=11, column=0)
	feedbacksVar = StringVar()
	feedbacksVar.set('0')
	countfeedbacks = tk.Label(pbars,textvariable = feedbacksVar).grid(row=11, column=1)
	feedbacksProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')


	#harmonogra
	labharmonogra = tk.Label(pbars, text = "harmonogra").grid(row=12, column=0)
	countharmonogra = tk.Label(pbars,text= "RĘCZNIE").grid(row=12, column=1)


	#main
	labmain = tk.Label(pbars, text = "main").grid(row=13, column=0)
	mainVar = StringVar()
	mainVar.set('0')
	countmain = tk.Label(pbars,textvariable = mainVar).grid(row=13, column=1)
	mainProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')


	#main_models
	labmain_models = tk.Label(pbars, text = "main_models").grid(row=14, column=0)
	main_modelsVar = StringVar()
	main_modelsVar.set('0')
	countmain_models = tk.Label(pbars,textvariable = main_modelsVar).grid(row=14, column=1)
	main_modelsProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')


	#mcdata
	labmcdata = tk.Label(pbars, text = "mcdata").grid(row=15, column=0)
	mcdataVar = StringVar()
	mcdataVar.set('0')
	countmcdata = tk.Label(pbars,textvariable = mcdataVar).grid(row=15, column=1)
	mcdataProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')


	#meascharts
	labmeascharts = tk.Label(pbars, text = "meascharts").grid(row=16, column=0)
	measchartsVar = StringVar()
	measchartsVar.set('0')
	countmeascharts = tk.Label(pbars,textvariable = measchartsVar).grid(row=16, column=1)
	measchartsProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')
	#
	#
	#measurements_low
	labmeasurements_low = tk.Label(pbars, text = "measurements_low").grid(row=17, column=0)
	measurements_lowVar = StringVar()
	measurements_lowVar.set('0')
	countmeasurements_low = tk.Label(pbars,textvariable = measurements_lowVar).grid(row=17, column=1)
	measurements_lowProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')
	#
	#points
	labpoints = tk.Label(pbars, text = "points").grid(row=18, column=0)
	pointsVar = StringVar()
	pointsVar.set('0')
	countpoints = tk.Label(pbars,textvariable = pointsVar).grid(row=18, column=1)
	pointsProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')
	#
	#
	 #remarks
	labremarks = tk.Label(pbars, text = "remarks").grid(row=19, column=0)
	remarksVar = StringVar()
	remarksVar.set('0')
	countremarks = tk.Label(pbars,textvariable = remarksVar).grid(row=19, column=1)
	remarksProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')

	 #reminder
	labreminder = tk.Label(pbars, text = "reminder").grid(row=20, column=0)
	reminderVar = StringVar()
	reminderVar.set('0')
	countreminder = tk.Label(pbars,textvariable = reminderVar).grid(row=20, column=1)
	reminderProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')
	
	 #reports
	labreports = tk.Label(pbars, text = "reports").grid(row=21, column=0)
	reportsVar = StringVar()
	reportsVar.set('0')
	countreports = tk.Label(pbars,textvariable = reportsVar).grid(row=21, column=1)
	reportsProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')
	

	
	 #shipsdata
	labshipsdata = tk.Label(pbars, text = "shipsdata").grid(row=22, column=0)
	shipsdataVar = StringVar()
	shipsdataVar.set('0')
	countshipsdata = tk.Label(pbars,textvariable = shipsdataVar).grid(row=22, column=1)
	shipsdataProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')
	
	 #standards
	labstandards = tk.Label(pbars, text = "standards").grid(row=23, column=0)
	standardsVar = StringVar()
	standardsVar.set('0')
	countstandards = tk.Label(pbars,textvariable = standardsVar).grid(row=23, column=1)
	standardsProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')
	

	
	 #users
	labusers = tk.Label(pbars, text = "users").grid(row=24, column=0)
	usersVar = StringVar()
	usersVar.set('0')
	countusers = tk.Label(pbars,textvariable = usersVar).grid(row=24, column=1)
	usersProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')


	class bearings(object): 
		def __init__(self):
			self.id = list()
			self.point = list()
			self.bearing = list()
			self.seal = list()
			self.additional = list()	
			self.greasing = list()
			def getVals(self):
				c = -1
				querryGET = "Select id,point,bearing,seal,additional,greasing from bearings"
				bearingstable = q_run(connBASE,querryGET)
				BearingsProgress_bar['maximum'] =len(bearingstable)
				BearingsProgress_bar.grid(row=0, column=2)	
				for line in bearingstable:
					c += 1
					beringsVar.set(str(c+1) + ' / ' + str(len(bearingstable)))	
					BearingsProgress_bar['value'] = c +1
					BearingsProgress_bar.update()
					self.id.append(line[0])
					self.point.append(line[1])
					self.bearing.append(line[2])
					self.seal.append(line[3])
					self.additional.append(line[4])
					if str(line[5]) == 'None':
						self.greasing.append('Null')
					else:
						self.greasing.append(line[5])
					querryUP = "insert into bearings(id,point,bearing,seal,additional,greasing) values('" + str(self.id[c]) + "','"+ str(self.point[c]) + "','"+ str(self.bearing[c]) + "','"+ str(self.seal[c]) + "','"+ str(self.additional[c]) + "'," + str(self.greasing[c]) + ")"
					q_run(connTARGET,querryUP)
			getVals(self)
	class bearings_add(object): 
		def __init__(self):
			self.add = list()
			def getVals(self):
				c = -1
				querryGET = "Select add from bearings_add"
				bearingsaddtable = q_run(connBASE,querryGET)
				Bearings_addProgress_bar['maximum'] =len(bearingsaddtable)
				Bearings_addProgress_bar.grid(row=1, column=2)	
				for line in bearingsaddtable:
					c += 1
					berings_addVar.set(str(c+1) + ' / ' + str(len(bearingsaddtable)))	
					Bearings_addProgress_bar['value'] = c +1
					Bearings_addProgress_bar.update()
					self.add.append(line[0])

					querryUP = "insert into bearings_add(add) values('" + str(self.add[c]) + "')"
					q_run(connTARGET,querryUP)
			getVals(self)
	class bearings_freq(object): 
		def __init__(self):
			self.bearing = list()
			self.bpfo = list()
			self.bpfi = list()
			self.ftf = list()
			self.bsf = list()	
			self.env = list()
			def getVals(self):
				c = -1
				querryGET = "Select bearing,bpfo,bpfi,ftf,bsf,env from bearings_freq"
				bearingsfreqtable = q_run(connBASE,querryGET)
				Bearings_freqProgress_bar['maximum'] =len(bearingsfreqtable)
				Bearings_freqProgress_bar.grid(row=2, column=2)	
				for line in bearingsfreqtable:
					c += 1
					berings_freqVar.set(str(c+1) + ' / ' + str(len(bearingsfreqtable)))	
					Bearings_freqProgress_bar['value'] = c +1
					Bearings_freqProgress_bar.update()
					self.bearing.append(line[0])
					self.bpfo.append(line[1])
					self.bpfi.append(line[2])
					self.ftf.append(line[3])
					self.bsf.append(line[4])
					self.env.append(line[5])
					if str(line[5]) == 'None':
						self.env.append('Null')
					else:
						self.env.append(line[5])
					querryUP = "insert into bearings_freq(bearing,bpfo,bpfi,ftf,bsf,env) values('" + str(self.bearing[c]) + "','"+ str(self.bpfo[c]) + "','"+ str(self.bpfi[c]) + "','"+ str(self.ftf[c]) + "','"+ str(self.bsf[c]) + "'," + str(self.env[c]) + ")"
					q_run(connTARGET,querryUP)
			getVals(self)
	class bearings_seals(object): 
		def __init__(self):
			self.seal = list()
			def getVals(self):
				c = -1
				querryGET = "Select seal from bearings_seals"
				bearingsaddtable = q_run(connBASE,querryGET)
				Bearings_sealsProgress_bar['maximum'] =len(bearingsaddtable)
				Bearings_sealsProgress_bar.grid(row=3, column=2)	
				for line in bearingsaddtable:
					c += 1
					berings_sealsVar.set(str(c+1) + ' / ' + str(len(bearingsaddtable)))	
					Bearings_sealsProgress_bar['value'] = c +1
					Bearings_sealsProgress_bar.update()
					self.seal.append(line[0])

					querryUP = "insert into bearings_seals(seal) values('" + str(self.seal[c]) + "')"
					q_run(connTARGET,querryUP)
			getVals(self)
	class costcases(object): 
		def __init__(self):
			self.lp = list()
			self.costflag = list()
			self.typ = list()
			self.kwrange = list()
			self.price = list()	
			self.low = list()
			self.high = list()
			def getVals(self):
				c = -1
				querryGET = "Select lp,costflag,typ,kwrange,price,low,high from costcases"
				table = q_run(connBASE,querryGET)
				CostcasesProgress_bar['maximum'] =len(table)
				CostcasesProgress_bar.grid(row=4, column=2)	
				for line in table:
					c += 1
					CostcasesVar.set(str(c+1) + ' / ' + str(len(table)))	
					CostcasesProgress_bar['value'] = c +1
					CostcasesProgress_bar.update()
					
					self.lp.append(line[0])
					
					if str(line[1]) == 'None':self.costflag.append('Null')
					else: self.costflag.append(line[1])
						
					self.typ.append(line[2])
					
					if str(line[3]) == 'None': self.kwrange.append('Null') 
					else: self.kwrange.append("ARRAY" + str(line[3]))
					
					if str(line[4]) == 'None': self.price.append('Null') 
					else: self.price.append("ARRAY" + str(line[4]))
					
					if str(line[5]) == 'None': self.low.append('Null') 
					else: self.low.append("ARRAY" + str(line[5]))
					
					if str(line[6]) == 'None': self.high.append('Null') 
					else: self.high.append("ARRAY" + str(line[6]))

					querryUP = "insert into costcases(lp,costflag,typ,kwrange,price,low,high) values(" + str(self.lp[c]) + ","+ str(self.costflag[c]) + ",'"+ str(self.typ[c]) + "',"+ str(self.kwrange[c]) + ","+ str(self.price[c]) + "," + str(self.low[c]) + "," + str(self.high[c])+ ")"
					q_run(connTARGET,querryUP)
			getVals(self)
	class costflags(object):
		def __init__(self):
			self.lp = list()
			self.flagstr = list()
			def getVals(self):
				c = -1
				querryGET = "Select lp,flagstr from costflags"
				table = q_run(connBASE,querryGET)
				costflagsProgress_bar['maximum'] =len(table)
				costflagsProgress_bar.grid(row=5, column=2)	
				for line in table:
					c += 1
					labcostflagsVar.set(str(c+1) + ' / ' + str(len(table)))	
					costflagsProgress_bar['value'] = c +1
					costflagsProgress_bar.update()
					
					self.lp.append(line[0])
					self.flagstr.append(line[1])

					querryUP = "insert into costflags(lp,flagstr) values(" + str(self.lp[c]) + ",'"+ str(self.flagstr[c]) + "')"
					q_run(connTARGET,querryUP)
			getVals(self)
	class crosstable(object):
		def __init__(self):
			self.parent = list()
			self.nameindevice = list()
			self.id = list()
			def getVals(self):
				c = -1
				querryGET = "Select parent,nameindevice,id from crosstable"
				table = q_run(connBASE,querryGET)
				crosstableProgress_bar['maximum'] =len(table)
				crosstableProgress_bar.grid(row=6, column=2)	
				for line in table:
					c += 1
					crosstableVar.set(str(c+1) + ' / ' + str(len(table)))	
					crosstableProgress_bar['value'] = c +1
					crosstableProgress_bar.update()
					
					self.parent.append(line[0])
					self.nameindevice.append(line[1])
					self.id.append(line[2])
					
					querryUP = "insert into crosstable(parent,nameindevice,id) values(" + str(self.parent[c]) + ",'"+ str(self.nameindevice[c]) + "'," + str(self.id[c]) + ")"
					q_run(connTARGET,querryUP)
			getVals(self)
	class devices(object):
		def __init__(self):
			self.id = list()
			self.parent = list()
			self.name = list()
			self.model = list()
			self.type = list()
			self.points = list()
			self.kw = list()
			self.rpm = list()
			self.pms = list()
			self.info = list()
			self.norm = list()
			self.drivenby = list()
			self.meas_condition = list()
			self.cm = list()

			def getVals(self):
				c = -1
				querryGET = "Select id,parent,name,model,type,points,kw,rpm,pms,info,norm,drivenby,meas_condition,cm from devices"
				table = q_run(connBASE,querryGET)
				devicesProgress_bar['maximum'] =len(table)
				devicesProgress_bar.grid(row=7, column=2)	
				for line in table:
					c += 1
					devicesVar.set(str(c+1) + ' / ' + str(len(table)))	
					devicesProgress_bar['value'] = c +1
					devicesProgress_bar.update()

					self.id.append(line[0])
					self.parent.append(line[1])
					if str(line[2]) == 'None':self.name.append('Null')
					else: self.name.append("'" + str(line[2]) + "'")
					
					if str(line[3]) == 'None':self.model.append('Null')
					else: self.model.append("'" + str(line[3]) + "'")
					
					if str(line[4]) == 'None':self.type.append('Null')
					else: self.type.append("'" + str(line[4]) + "'")
					
					if str(line[5]) == 'None':self.points.append('Null')
					else: self.points.append("'" + str(line[5]) + "'")
					
					if str(line[6]) == 'None':self.kw.append('Null')
					else: self.kw.append("'" + str(line[6]) + "'")
					
					if str(line[7]) == 'None':self.rpm.append('Null')
					else: self.rpm.append("'" + str(line[7]) + "'")
					
					if str(line[8]) == 'None':self.pms.append('Null')
					else: self.pms.append("'" + str(line[8]) + "'")
					
					
					if str(line[9]) == 'None':self.info.append('Null')
					else: self.info.append("'" + str(line[9]) + "'")
					
					if str(line[10]) == 'None':self.norm.append('Null')
					else: self.norm.append("'" + str(line[10]) + "'")
					
					if str(line[11]) == 'None':self.drivenby.append('Null')
					else: self.drivenby.append(line[11])
					
					
					if str(line[12]) == 'None':self.meas_condition.append('Null')
					else: self.meas_condition.append("'" + str(line[12]) + "'")
					
					if str(line[13]) == 'None':self.cm.append('Null')
					else: self.cm.append(line[13])
					
					querryUP = "insert into devices(id,parent,name,model,type,points,kw,rpm,pms,info,norm,drivenby,meas_condition,cm)values("+ str(self.id[c]) + "," + str(self.parent[c]) + "," + str(self.name[c]) + "," + str(self.model[c]) + "," + str(self.type[c]) + ","+ str(self.points[c]) + "," + str(self.kw[c]) + "," + str(self.rpm[c]) + "," + str(self.pms[c]) + "," + str(self.info[c]) + "," + str(self.norm[c]) + "," + str(self.drivenby[c]) + "," + str(self.meas_condition[c]) + "," + str(self.cm[c]) + ")"
					q_run(connTARGET,querryUP)
			getVals(self)
	class ds_structure(object):
		def __init__(self):
			self.parent = list()
			self.sort = list()
			self.id = list()
			def getVals(self):
				c = -1
				querryGET = "Select parent,sort,id from ds_structure"
				table = q_run(connBASE,querryGET)
				ds_structureProgress_bar['maximum'] =len(table)
				ds_structureProgress_bar.grid(row=8, column=2)	
				for line in table:
					c += 1
					ds_structureVar.set(str(c+1) + ' / ' + str(len(table)))	
					ds_structureProgress_bar['value'] = c +1
					ds_structureProgress_bar.update()
					
					self.parent.append(line[0])
					self.sort.append(line[1])
					self.id.append(line[2])
					
					querryUP = "insert into ds_structure(parent,sort,id) values(" + str(self.parent[c]) + ",'"+ str(self.sort[c]) + "','" + str(self.id[c]) + "')"
					q_run(connTARGET,querryUP)
			getVals(self)		
	class equipment(object):
		def __init__(self):
			self.lp = list()
			self.device = list()
			self.serialno = list()
			self.caldue = list()
			self.manudate = list()
			def getVals(self):
				c = -1
				querryGET = "Select lp,device,serialno,caldue,manudate from equipment"
				table = q_run(connBASE,querryGET)
				equipmentProgress_bar['maximum'] =len(table)
				equipmentProgress_bar.grid(row=9, column=2)	
				for line in table:
					c += 1
					equipmentVar.set(str(c+1) + ' / ' + str(len(table)))	
					equipmentProgress_bar['value'] = c +1
					equipmentProgress_bar.update()
					
					self.lp.append(line[0])
					self.device.append(line[1])
					self.serialno.append(line[2])
					self.caldue.append(line[3])
					self.manudate.append(line[4])
					
					querryUP = "insert into equipment(lp,device,serialno,caldue,manudate) values(" + str(self.lp[c]) + ",'"+ str(self.device[c]) + "','" + str(self.serialno[c]) + "','" + str(self.caldue[c]) +"','" + str(self.manudate[c]) + "')"
					q_run(connTARGET,querryUP)
			getVals(self)	
	class fdbflags(object):
		def __init__(self):
			self.lp = list()
			self.flagstr = list()
			def getVals(self):
				c = -1
				querryGET = "Select lp,flagstr from fdbflags"
				table = q_run(connBASE,querryGET)
				costflagsProgress_bar['maximum'] =len(table)
				costflagsProgress_bar.grid(row=10, column=2)	
				for line in table:
					c += 1
					fdb_flagsVar.set(str(c+1) + ' / ' + str(len(table)))	
					costflagsProgress_bar['value'] = c +1
					costflagsProgress_bar.update()
					
					self.lp.append(line[0])
					self.flagstr.append(line[1])

					querryUP = "insert into fdbflags(lp,flagstr) values(" + str(self.lp[c]) + ",'"+ str(self.flagstr[c]) + "')"
					q_run(connTARGET,querryUP)
			getVals(self)

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
			def getVals(self):
				c = -1
				querryGET = "select parent,id,feedback,documentdate,fdbflag,costflag, raport_number, price, low, high from feedbacks where id is not null and parent is not null"
				table = q_run(connBASE, querryGET)
				feedbacksProgress_bar['maximum'] = len(table)
				feedbacksProgress_bar.grid(row=11, column=2)
				for line in table:
					c += 1
					feedbacksVar.set(str(c + 1) + ' / ' + str(len(table)))
					feedbacksProgress_bar['value'] = c + 1
					feedbacksProgress_bar.update()
					self.parent.append(line[0])
					self.id.append(line[1])
					if str(line[2]) == 'None':self.feedback.append('Null')
					else: self.feedback.append("'" + str(line[2]) + "'")
					if str(line[3]) == 'None':self.documentdate.append('Null')
					else: self.documentdate.append("'" + str(line[3]) + "'")
					if str(line[4]) == 'None':self.fdbflag.append('Null')
					else: self.fdbflag.append(str(line[4]))
					if str(line[5]) == 'None':self.costflag.append('Null')
					else: self.costflag.append(str(line[5]))
					if str(line[6]) == 'None':self.raport_number.append('Null')
					else: self.raport_number.append("'" + str(line[6]) + "'")
					if str(line[7]) == 'None': self.price.append('Null')
					else: self.price.append("ARRAY" + str(line[7]))
					if str(line[8]) == 'None': self.low.append('Null')
					else: self.low.append("ARRAY" + str(line[8]))
					if str(line[9]) == 'None': self.high.append('Null')
					else: self.high.append("ARRAY" + str(line[9]))
					querryUP = "insert into feedbacks(parent,id,feedback,documentdate,fdbflag,costflag, raport_number, price, low, high) values("+ str(self.parent[c]) + "," + str(self.id[c]) + "," + str(self.feedback[c])+ "," + str(self.documentdate[c])+ "," + str(self.fdbflag[c])+ "," +str(self.costflag[c])+ "," +str(self.raport_number[c])+ "," +str(self.price[c])+ "," +str(self.low[c])+"," +str(self.high[c])+ ")"
					q_run(connTARGET, querryUP)
			getVals(self)


	class main(object):
		def __init__(self):
			self.id = list()
			self.parent= list()
			self.name = list()
			self.color = list()
			self.reporttype = list()
			self.lastupdate = list()
			self.ownercolor = list()
			self.sendinfo = list()
			def getVals(self):
				c = -1
				querryGET = "select id, parent, name, color, reporttype, lastupdate, ownercolor, sendinfo from main"
				table = q_run(connBASE, querryGET)
				mainProgress_bar['maximum'] = len(table)
				mainProgress_bar.grid(row=13, column=2)
				for line in table:
					c += 1
					mainVar.set(str(c + 1) + ' / ' + str(len(table)))
					mainProgress_bar['value'] = c + 1
					mainProgress_bar.update()
					self.id.append(line[0])
					if str(line[1]) == 'None':self.parent.append('Null')
					else: self.parent.append(str(line[1]))
					if str(line[2]) == 'None':self.name.append('Null')
					else: self.name.append("'" + str(line[2]) + "'")
					if str(line[3]) == 'None':self.color.append('Null')
					else: self.color.append("'" + str(line[3]) + "'")
					if str(line[4]) == 'None':self.reporttype.append('Null')
					else: self.reporttype.append("'" + str(line[4]) + "'")
					if str(line[5]) == 'None':self.lastupdate.append('Null')
					else: self.lastupdate.append("'" + str(line[5]) + "'")
					if str(line[6]) == 'None':self.ownercolor.append('Null')
					else: self.ownercolor.append("'" + str(line[6]) + "'")
					if str(line[7]) == 'None':self.sendinfo.append('Null')
					else: self.sendinfo.append("'" + str(line[7]) + "'")


					querryUP = "insert into main(id,parent,name,color,reporttype,lastupdate,ownercolor,sendinfo) values("+ str(self.id[c]) + "," + str(self.parent[c]) + "," + str(self.name[c])+ "," + str(self.color[c])+ "," + str(self.reporttype[c]) + "," + str(self.lastupdate[c])+","+ str(self.ownercolor[c])+","+ str(self.sendinfo[c])+")"
					q_run(connTARGET, querryUP)
			getVals(self)

	class main_models(object):
		def __init__(self):
			self.id = list()
			self.parent= list()
			self.name = list()
			self.type = list()

			def getVals(self):
				c = -1
				querryGET = "select id, parent, name, type from main_models"
				table = q_run(connBASE, querryGET)
				main_modelsProgress_bar['maximum'] = len(table)
				main_modelsProgress_bar.grid(row=14, column=2)
				for line in table:
					c += 1
					main_modelsVar.set(str(c + 1) + ' / ' + str(len(table)))
					main_modelsProgress_bar['value'] = c + 1
					main_modelsProgress_bar.update()
					self.id.append(line[0])
					if str(line[1]) == 'None':self.parent.append('Null')
					else: self.parent.append(str(line[1]))
					if str(line[2]) == 'None':self.name.append('Null')
					else: self.name.append("'" + str(line[2]) + "'")
					if str(line[3]) == 'None':self.type.append('Null')
					else: self.type.append("'" + str(line[3]) + "'")

					querryUP = "insert into main_models(id,parent,name,type) values("+ str(self.id[c]) + "," + str(self.parent[c]) + "," + str(self.name[c])+ "," + str(self.type[c])+")"
					q_run(connTARGET, querryUP)
			getVals(self)



	class mcdata(object):
		def __init__(self):
			self.parent = list()
			self.id = list()
			self.mcremark = list()
			self.documentdate = list()
			self.raport_number = list()
			def getVals(self):
				c = -1
				querryGET = "select parent,id,mcremark,documentdate,raport_number from mcdata where id is not null and parent is not null"
				table = q_run(connBASE, querryGET)
				mcdataProgress_bar['maximum'] = len(table)
				mcdataProgress_bar.grid(row=15, column=2)
				for line in table:
					c += 1
					mcdataVar.set(str(c + 1) + ' / ' + str(len(table)))
					mcdataProgress_bar['value'] = c + 1
					mcdataProgress_bar.update()
					self.parent.append(line[0])
					self.id.append(line[1])
					if str(line[2]) == 'None':self.mcremark.append('Null')
					else: self.mcremark.append("'" + (str(line[2])).replace("'"," ") + "'")
					if str(line[3]) == 'None':self.documentdate.append('Null')
					else: self.documentdate.append("'" + str(line[3]) + "'")
					if str(line[4]) == 'None':self.raport_number.append('Null')
					else: self.raport_number.append("'" + str(line[4]) + "'")
					querryUP = "insert into mcdata(parent,id,mcremark,documentdate,raport_number) values("+ str(self.parent[c]) + "," + str(self.id[c]) + "," + str(self.mcremark[c])+ "," + str(self.documentdate[c])+ "," + str(self.raport_number[c]) + ")"
					q_run(connTARGET, querryUP)
			getVals(self)

	class meascharts(object):
		def __init__(self):
			self.lp = list()
			self.shipid= list()
			self.id = list()
			self.point = list()
			self.report_number = list()
			self.date = list()
			self.domain = list()
			self.type = list()
			self.unit = list()
			self.chart = list()


			def getVals(self):
				c = -1
				querryGET = "select lp, shipid, id, point, report_number, date, domain, type, unit, chart from meascharts"
				table = q_run(connBASE, querryGET)
				measchartsProgress_bar['maximum'] = len(table)
				measchartsProgress_bar.grid(row=16, column=2)
				for line in table:
					c += 1
					measchartsVar.set(str(c + 1) + ' / ' + str(len(table)))
					measchartsProgress_bar['value'] = c + 1
					measchartsProgress_bar.update()
					self.lp.append(line[0])
					if str(line[1]) == 'None':self.shipid.append('Null')
					else: self.shipid.append(str(line[1]))
					if str(line[2]) == 'None':self.id.append('Null')
					else: self.id.append("'" + str(line[2]) + "'")
					if str(line[3]) == 'None':self.point.append('Null')
					else: self.point.append("'" + str(line[3]) + "'")
					if str(line[4]) == 'None':self.report_number.append('Null')
					else: self.report_number.append("'" +str(line[4]) + "'")
					if str(line[5]) == 'None':self.date.append('Null')
					else: self.date.append("'" + str(line[5]) + "'")
					if str(line[6]) == 'None':self.domain.append('Null')
					else: self.domain.append("'" + str(line[6]) + "'")
					if str(line[7]) == 'None':self.type.append('Null')
					else: self.type.append(str("'" +str(line[7]) + "'"))
					if str(line[8]) == 'None':self.unit.append('Null')
					else: self.unit.append("'" + str(line[8]) + "'")
					if str(line[9]) == 'None':self.chart.append('Null')
					else: self.chart.append("'" + str(line[9]) + "'")

					querryUP = "insert into meascharts(lp, shipid, id, point, report_number, date, domain, type, unit, chart) values(" + str(self.lp[c]) + "," + str(self.shipid[c]) + "," + str(self.id[c])+ "," + str(self.point[c])+ "," + str(self.report_number[c]) + "," + str(self.date[c]) + "," + str(self.domain[c]) + "," + str(self.type[c]) +","+ str(self.unit[c]) + "," + str(self.chart[c]) + ")"
					q_run(connTARGET, querryUP)
			getVals(self)

	class measurements_low(object):
		def __init__(self):
			self.parent= list()
			self.id = list()
			self.point = list()
			self.raport_number = list()
			self.date = list()
			self.value = list()
			self.type = list()
			self.unit = list()


			def getVals(self):
				c = -1
				querryGET = "select parent, id, point, raport_number, date, value, type, unit from measurements_low"
				table = q_run(connBASE, querryGET)
				measurements_lowProgress_bar['maximum'] = len(table)
				measurements_lowProgress_bar.grid(row=17, column=2)
				for line in table:
					c += 1
					measurements_lowVar.set(str(c + 1) + ' / ' + str(len(table)))
					measurements_lowProgress_bar['value'] = c + 1
					measurements_lowProgress_bar.update()
					if str(line[0]) == 'None':self.parent.append('Null')
					else: self.parent.append("'" + str(line[0]) + "'")
					if str(line[1]) == 'None':self.id.append('Null')
					else: self.id.append("'" + str(line[1]) + "'")
					if str(line[2]) == 'None':self.point.append('Null')
					else: self.point.append("'" + str(line[2]) + "'")
					if str(line[3]) == 'None':self.raport_number.append('Null')
					else: self.raport_number.append("'" +str(line[3]) + "'")
					if str(line[4]) == 'None':self.date.append('Null')
					else: self.date.append("'" + str(line[4]) + "'")
					if str(line[5]) == 'None':self.value.append('Null')
					else: self.value.append("'" + str(line[5]) + "'")
					if str(line[6]) == 'None':self.type.append('Null')
					else: self.type.append(str("'" +str(line[6]) + "'"))
					if str(line[7]) == 'None':self.unit.append('Null')
					else: self.unit.append("'" + str(line[7]) + "'")


					querryUP = "insert into measurements_low(parent, id, point, raport_number, date, value, type, unit) values(" \
							   + str(self.parent[c]) + "," + str(self.id[c])+ "," + str(self.point[c])+ "," \
							   + str(self.raport_number[c]) + "," + str(self.date[c]) + "," + str(self.value[c]) + "," \
							   + str(self.type[c]) +","+ str(self.unit[c]) + ")"
					q_run(connTARGET, querryUP)
			getVals(self)

	class points(object):
		def __init__(self):
			self.id = list()
			self.point = list()
			self.sort = list()
			self.visible = list()
			def getVals(self):
				c = -1
				querryGET = "select id,point,sort,visible from points where id is not null and point is not null"
				table = q_run(connBASE, querryGET)
				pointsProgress_bar['maximum'] = len(table)
				pointsProgress_bar.grid(row=18, column=2)
				for line in table:
					c += 1
					pointsVar.set(str(c + 1) + ' / ' + str(len(table)))
					pointsProgress_bar['value'] = c + 1
					pointsProgress_bar.update()
					self.id.append(line[0])
					if str(line[1]) == 'None':self.point.append('Null')
					else:self.point.append("'" + str(line[1]) + "'")
					if str(line[2]) == 'None':self.sort.append('Null')
					else: self.sort.append("'" + str(line[2]) + "'")
					if str(line[3]) == 'None':self.visible.append('Null')
					else: self.visible.append("'" + str(line[3]) + "'")

					querryUP = "insert into points(id,point,sort,visible) values("+ str(self.id[c]) + "," + str(self.point[c]) + "," + str(self.sort[c])+ "," + str(self.visible[c])+ ")"
					q_run(connTARGET, querryUP)
			getVals(self)

	class remarks(object):
		def __init__(self):
			self.parent = list()
			self.id = list()
			self.remark = list()
			self.documentdate = list()
			self.raport_number = list()
			self.sended = list()
			def getVals(self):
				c = -1
				querryGET = "select parent,id,remark,documentdate, raport_number, sended from remarks where id is not null and parent is not null"
				table = q_run(connBASE, querryGET)
				remarksProgress_bar['maximum'] = len(table)
				remarksProgress_bar.grid(row=19, column=2)
				for line in table:
					c += 1
					remarksVar.set(str(c + 1) + ' / ' + str(len(table)))
					remarksProgress_bar['value'] = c + 1
					remarksProgress_bar.update()
					self.parent.append(line[0])
					self.id.append(line[1])
					if str(line[2]) == 'None':self.remark.append('Null')
					else: self.remark.append("'" + str(line[2]) + "'")
					if str(line[3]) == 'None':self.documentdate.append('Null')
					else: self.documentdate.append("'" + str(line[3]) + "'")
					if str(line[4]) == 'None':self.raport_number.append('Null')
					else: self.raport_number.append("'" + str(line[4]) + "'")
					if str(line[5]) == 'None': self.sended.append('Null')
					else: self.sended.append(str(line[5]))

					querryUP = "insert into remarks(parent,id,remark,documentdate,raport_number, sended) values("+ str(self.parent[c]) + "," + str(self.id[c]) + "," + str(self.remark[c])+ "," + str(self.documentdate[c])+ "," + str(self.raport_number[c])+ "," +str(self.sended[c])+ ")"
					q_run(connTARGET, querryUP)
			getVals(self)

	class reminder(object):
		def __init__(self):
			self.parent = list()
			self.raport_number = list()
			self.send_date = list()
			self.request_date = list()
			self.status = list()
			self.remcom = list()
			self.im_comment = list()
			self.id = list()

			def getVals(self):
				c = -1
				querryGET = "select parent, raport_number,send_date,request_date,status,remcom,im_comment,Id from reminder"
				table = q_run(connBASE, querryGET)
				reminderProgress_bar['maximum'] = len(table)
				reminderProgress_bar.grid(row=20, column=2)
				for line in table:
					c += 1
					reminderVar.set(str(c + 1) + ' / ' + str(len(table)))
					reminderProgress_bar['value'] = c + 1
					reminderProgress_bar.update()
					self.parent.append(line[0])
					if str(line[1]) == 'None':self.raport_number.append('Null')
					else: self.raport_number.append("'" + str(line[1]) + "'")
					if str(line[2]) == 'None':self.send_date.append('Null')
					else: self.send_date.append("'" + str(line[2]) + "'")
					if str(line[3]) == 'None':self.request_date.append('Null')
					else: self.request_date.append("'" + str(line[3]) + "'")
					if str(line[4]) == 'None':self.status.append('Null')
					else: self.status.append("'" + str(line[4]) + "'")
					if str(line[5]) == 'None':self.remcom.append('Null')
					else: self.remcom.append("'" + str(line[5]) + "'")
					if str(line[6]) == 'None':self.im_comment.append('Null')
					else: self.im_comment.append("'" + str(line[6]) + "'")
					if str(line[7]) == 'None':self.id.append('Null')
					else: self.id.append("'" + str(line[7]) + "'")

					querryUP = "insert into reminder(parent, raport_number,send_date,request_date,status,remcom,im_comment,Id) values("\
							   + str(self.parent[c]) + "," + str(self.raport_number[c]) + "," + str(self.send_date[c])+ "," + str(self.request_date[c])+"," \
							   + str(self.status[c]) + "," + str(self.remcom[c]) + "," + str(self.im_comment[c]) + "," + str(self.id[c]) + ")"
					q_run(connTARGET, querryUP)


			getVals(self)



	class reports(object):
		def __init__(self):
			self.shipid = list()
			self.raport_number = list()
			self.raport_date = list()
			self.person = list()
			self.color = list()


			def getVals(self):
				c = -1
				querryGET = "select shipid, raport_number, raport_date, person, color from reports where shipid is not null"
				table = q_run(connBASE, querryGET)
				reportsProgress_bar['maximum'] = len(table)
				reportsProgress_bar.grid(row=21, column=2)
				for line in table:
					c += 1
					reportsVar.set(str(c + 1) + ' / ' + str(len(table)))
					reportsProgress_bar['value'] = c + 1
					reportsProgress_bar.update()
					self.shipid.append(line[0])
					if str(line[1]) == 'None':self.raport_number.append('Null')
					else: self.raport_number.append("'" + str(line[1]) + "'")
					if str(line[2]) == 'None':self.raport_date.append('Null')
					else: self.raport_date.append("'" + str(line[2]) + "'")
					if str(line[3]) == 'None':self.person.append('Null')
					else: self.person.append("'" + str(line[3]) + "'")
					if str(line[4]) == 'None':self.color.append('Null')
					else: self.color.append("'" + str(line[4]) + "'")

					querryUP = "insert into reports(shipid, raport_number,raport_date,person,color) values("\
							   + str(self.shipid[c]) + "," + str(self.raport_number[c]) + "," + str(self.raport_date[c])+ "," + str(self.person[c]) \
							   +"," + str(self.color[c]) + ")"
					q_run(connTARGET, querryUP)


			getVals(self)



	class shipsdata(object):
		def __init__(self):
			self.name = list()
			self.shiptype = list()
			self.lenght = list()
			self.bradth = list()
			self.shmarvib = list()
			self.dateofmanufacture = list()
			self.measrange = list()
			self.error = list()
			self.imo = list()
			self.serialnumber = list()
			self.shipid = list()
			self.equipment = list()
			def getVals(self):
				c = -1
				querryGET = "select name,shiptype,lenght,bradth,shmarvib,dateofmanufacture,measrange,error,imo,serialnumber,shipid,equipment from shipsdata"
				table = q_run(connBASE, querryGET)
				shipsdataProgress_bar['maximum'] = len(table)
				shipsdataProgress_bar.grid(row=22, column=2)
				for line in table:
					c += 1
					shipsdataVar.set(str(c + 1) + ' / ' + str(len(table)))
					shipsdataProgress_bar['value'] = c + 1
					shipsdataProgress_bar.update()
					if str(line[0]) == 'None':self.name.append('Null')
					else: self.name.append("'" + str(line[0]) + "'")
					if str(line[1]) == 'None':self.shiptype.append('Null')
					else: self.shiptype.append("'" + str(line[1]) + "'")
					if str(line[2]) == 'None':self.lenght.append('Null')
					else: self.lenght.append("'" + str(line[2]) + "'")
					if str(line[3]) == 'None':self.bradth.append('Null')
					else: self.bradth.append("'" + str(line[3]) + "'")
					if str(line[4]) == 'None':self.shmarvib.append('Null')
					else: self.shmarvib.append("'" + str(line[4]) + "'")
					if str(line[5]) == 'None':self.dateofmanufacture.append('Null')
					else: self.dateofmanufacture.append("'" + str(line[5]) + "'")
					if str(line[6]) == 'None':self.measrange.append('Null')
					else: self.measrange.append("'" + str(line[6]) + "'")
					if str(line[7]) == 'None':self.error.append('Null')
					else: self.error.append("'" + str(line[7]) + "'")
					if str(line[8]) == 'None':self.imo.append('Null')
					else: self.imo.append("'" + str(line[8]) + "'")
					if str(line[9]) == 'None':self.serialnumber.append('Null')
					else: self.serialnumber.append("'" + str(line[9]) + "'")
					if str(line[10]) == 'None':self.shipid.append('Null')
					else: self.shipid.append("'" + str(line[10]) + "'")
					if str(line[11]) == 'None':self.equipment.append('Null')
					else: self.equipment.append("'" + str(line[11]) + "'")

					querryUP = "insert into shipsdata(name,shiptype,lenght,bradth,shmarvib,dateofmanufacture,measrange,error,imo,serialnumber,shipid,equipment) values("\
							   + str(self.name[c]) + "," + str(self.shiptype[c]) + "," + str(self.lenght[c])+ "," + str(self.bradth[c]) \
							   + "," + str(self.shmarvib[c]) + "," + str(self.dateofmanufacture[c]) + "," + str(self.measrange[c])+ "," + str(self.error[c]) \
							   + "," + str(self.imo[c]) + "," + str(self.serialnumber[c]) + "," + str(self.shipid[c])+ "," + str(self.equipment[c]) \
							   + ")"
					q_run(connTARGET, querryUP)


			getVals(self)


	class standards(object):
		def __init__(self):
			self.standard = list()
			self.limit_1_name = list()
			self.limit_1_value = list()
			self.limit_2_name = list()
			self.limit_2_value = list()
			self.limit_3_name = list()
			self.limit_3_value = list()
			self.limit_4_name = list()
			self.limit_4_value = list()
			self.informations = list()
			self.envflag = list()
			def getVals(self):
				c = -1
				querryGET = "select standard, limit_1_name,limit_1_value,limit_2_name, limit_2_value, limit_3_name, limit_3_value, limit_4_name, limit_4_value, informations, envflag from standards"
				table = q_run(connBASE, querryGET)
				standardsProgress_bar['maximum'] = len(table)
				standardsProgress_bar.grid(row=23, column=2)
				for line in table:
					c += 1
					standardsVar.set(str(c + 1) + ' / ' + str(len(table)))
					standardsProgress_bar['value'] = c + 1
					standardsProgress_bar.update()
					self.standard.append(line[0])
					self.limit_1_name.append(line[1])
					self.limit_1_value.append(line[2])
					self.limit_2_name.append(line[3])
					self.limit_2_value.append(line[4])
					self.limit_3_name.append(line[5])
					self.limit_3_value.append(line[6])
					self.limit_4_name.append(line[7])
					self.limit_4_value.append(line[8])
					self.informations.append(line[9])
					self.envflag.append(line[10])


					querryUP = "insert into standards(standard, limit_1_name, limit_2_value, limit_3_name, limit_3_value, limit_4_name, limit_4_value, informations, envflag) values('"\
							   + str(self.standard[c]) + "','" + str(self.limit_1_name[c]) + "','" + str(self.limit_2_value[c])+ "','" + str(self.limit_3_name[c]) \
							   +  "','" + str(self.limit_3_value[c]) + "','" + str(self.limit_4_name[c]) + "','" + str(self.limit_4_value[c])+ "','" + str(self.informations[c]) \
							   +  "','" + str(self.envflag[c]) + "')"
					q_run(connTARGET, querryUP)


			getVals(self)

	class users(object):
		def __init__(self):
			self.login = list()
			self.full_name = list()
			self.analyzer = list()
			self.feedbacks = list()
			self.reminder = list()
			self.deviceupdater = list()
			self.ini = list()
			self.master = list()
			self.majoradd = list()
			self.uploader = list()
			self.selector = list()
			self.todo = list()
			self.charter = list()
			self.mailer = list()

			def getVals(self):
				c = -1
				querryGET = "select login, full_name, analyzer, feedbacks, reminder, deviceupdater, ini, master, majoradd, uploader, selector, todo, charter, mailer from users"
				table = q_run(connBASE, querryGET)
				usersProgress_bar['maximum'] = len(table)
				usersProgress_bar.grid(row=24, column=2)
				for line in table:
					c += 1
					usersVar.set(str(c + 1) + ' / ' + str(len(table)))
					usersProgress_bar['value'] = c + 1
					usersProgress_bar.update()
					self.login.append(line[0])
					self.full_name.append(line[1])
					self.ini.append(line[6])
					if str(line[2]) == 'None':self.analyzer.append('False')
					else: self.analyzer.append(str(line[2]))
					if str(line[3]) == 'None':self.feedbacks.append('False')
					else: self.feedbacks.append(str(line[3]))
					if str(line[4]) == 'None':self.reminder.append('False')
					else: self.reminder.append(str(line[4]))
					if str(line[5]) == 'None':self.deviceupdater.append('False')
					else: self.deviceupdater.append(str(line[5]))
					if str(line[7]) == 'None':self.master.append('False')
					else: self.master.append(str(line[7]))
					if str(line[8]) == 'None':self.majoradd.append('False')
					else: self.majoradd.append(str(line[8]))
					if str(line[9]) == 'None':self.uploader.append('False')
					else: self.uploader.append(str(line[9]))
					if str(line[10]) == 'None':self.selector.append('False')
					else: self.selector.append(str(line[10]))
					if str(line[11]) == 'None':self.todo.append('False')
					else: self.todo.append(str(line[11]))
					if str(line[12]) == 'None':self.charter.append('False')
					else: self.charter.append(str(line[12]))
					if str(line[13]) == 'None':self.mailer.append('False')
					else: self.mailer.append(str(line[13]))



					querryUP = "insert into users(login, full_name, analyzer, feedbacks, reminder, deviceupdater, ini, master, majoradd, uploader, selector, todo, charter, mailer) values('"\
							   + str(self.login[c]) + "','" + str(self.full_name[c]) + "','" + str(self.analyzer[c])+ "','" + str(self.feedbacks[c]) \
							   + "','" + str(self.reminder[c]) + "','" + str(self.deviceupdater[c]) + "','" + str(self.ini[c])+ "','" + str(self.master[c]) \
							   + "','" + str(self.majoradd[c]) + "','" + str(self.uploader[c]) + "','" + str(self.selector[c]) + "','" + str(self.todo[c]) \
							   + "','" + str(self.charter[c]) + "','" + str(self.mailer[c]) + "')"
					q_run(connTARGET, querryUP)


			getVals(self)






	# main()
	# shipsdata()
	# users()
	# ds_structure()
	# devices()
	#
	#
	# costcases()
	# costflags()
	# crosstable()
	# points() #PRZETESTOWANE CZESCIOWO - ZAMULILO STRASZNIE W TRAKCIE
	#
	# standards()
	#
	# bearings()
	# bearings_add()
	# bearings_freq()
	# bearings_seals()
	#
	#
	#
	# equipment()
	# fdbflags()

	# #harmonogram przeniesc recznie - za duzo kolumn a za mało danych zeby było warto sie bawic
	#
	# main_models()
	#
	# meascharts()

	remarks()
	# feedbacks()
	#reminder()


	mcdata()  # stestowac jeszcze raz - zmiana apostrofu na spacje


	print("WSTAWIC RECZNIE KOMBAJNVER")
	print("WSTAWIC RECZNIE HARMONOGRAM")

	## TE ZOSTAŁY
	#reports()
	#measurements_low()


	pbars.mainloop()

	
migratestruct()
#copyharmo()



#q_run(connTARGET, 'select * from main')