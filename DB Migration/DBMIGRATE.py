import psycopg2
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
username = 'filipb'
password = '@infomarine'
host1 = 'localhost'
host2 = 'localhost'
connBASE = [username,password,host1]
connTARGET = [username,password,host2]

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


	# #main_models
	# labmain_models = tk.Label(pbars, text = "main_models").grid(row=14, column=0)
	# main_modelsVar = StringVar()
	# main_modelsVar.set('0')
	# countmain_models = tk.Label(pbars,textvariable = main_modelsVar).grid(row=14, column=1)
	# main_modelsProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')
	#
	#
	#mcdata
	labmcdata = tk.Label(pbars, text = "mcdata").grid(row=15, column=0)
	mcdataVar = StringVar()
	mcdataVar.set('0')
	countmcdata = tk.Label(pbars,textvariable = mcdataVar).grid(row=15, column=1)
	mcdataProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')
	#
	#
	# #meascharts
	# labmeascharts = tk.Label(pbars, text = "meascharts").grid(row=16, column=0)
	# measchartsVar = StringVar()
	# measchartsVar.set('0')
	# countmeascharts = tk.Label(pbars,textvariable = measchartsVar).grid(row=16, column=1)
	# measchartsProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')
	#
	#
	# #measurements_low
	# labmeasurements_low = tk.Label(pbars, text = "measurements_low").grid(row=17, column=0)
	# measurements_lowVar = StringVar()
	# measurements_lowVar.set('0')
	# countmeasurements_low = tk.Label(pbars,textvariable = measurements_lowVar).grid(row=17, column=1)
	# measurements_lowProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')
	#
	# #points
	# labpoints = tk.Label(pbars, text = "points").grid(row=18, column=0)
	# pointsVar = StringVar()
	# pointsVar.set('0')
	# countpoints = tk.Label(pbars,textvariable = pointsVar).grid(row=18, column=1)
	# pointsProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')
	#
	#
	#remarks
	labremarks = tk.Label(pbars, text = "remarks").grid(row=19, column=0)
	remarksVar = StringVar()
	remarksVar.set('0')
	countremarks = tk.Label(pbars,textvariable = remarksVar).grid(row=19, column=1)
	remarksProgress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 300, mode = 'determinate')



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


	class main(object): ### DOKONCZYC
		def __init__(self):
			self.id = list()
			self.paren = list()
			self.name = list()
			self.color = list()
			self.reporttype = list()
			self.lastupdate = list()
			self.ovnercolor = list()
			self.sendinfo = list()
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



	#bearings()
	#bearings_add()
	#bearings_freq()
	#bearings_seals()
	#costcases()
	#costflags()
	#crosstable()
	#devices()
	#ds_structure()
	#equipment()
	#fdbflags()
	#feedbacks()
	#harmonogram przeniesc recznie - za duzo kolumn a za mało danych zeby było warto sie bawic
	main()

	#mcdata() #stestowac jeszcze raz - zmiana apostrofu na spacje



	#remarks()



	### KOMBAJNVER WSTAWIC RECZNIE ! ! ! !
	print("WSTAWIC RECZNIE KOMBAJNVER")
	
	
	pbars.mainloop()

	
migratestruct()