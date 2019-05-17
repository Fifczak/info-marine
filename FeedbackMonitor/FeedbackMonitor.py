import Monitor
import UnknowSentFlag
import RemarksWithoutFeedbacksMonitor
import psycopg2
import csv
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *

def runprogram():
	username = 'filipb'
	password = '@infomarine'
	host = '192.168.10.243'
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
	def ClDNoRem():
		def countLimit(standard, value):
			limSrt = 'NOPE'
			for limNo in limits:
				if str(limNo[0]) == str(standard):
					if value <= float(limNo[3]):  # IF LIM1
						limSrt = str(limNo[2])
						break
					else:
						if value <= float(limNo[5]):  # IF LIM2
							limSrt = str(limNo[4])
							break
						else:
							if value <= float(limNo[7]):  # IF LIM3
								limSrt = str(limNo[6])
								break
							else:
								limSrt = str(limNo[8])
								break
			return limSrt

		querry = """select standard,
								limit_1_value,limit_1_name,
								limit_2_value,limit_2_name, 
								limit_3_value,limit_3_name,
								limit_4_value,limit_4_name,
							envflag
						from standards"""
		limits = q_run(connD, querry)

		querry = """select 
							 ml.id, ml.raport_number, max(ml.value) as RMS, dev.norm, main.name,dev.name,dev.parent,main.id
							from measurements_low as ml
							 left join devices as dev on ml.id = dev.id and dev.parent = ml.parent
							 left join main as main on ml.parent = main.id
							 where ml.type = 'RMS' and raport_number is not null and raport_number <> 'Archive' and raport_number <> '' and dev.norm is not null and (ml.point !~ 'A') and ml.date >= '2018-01-01'
							 group by ml.id, ml.raport_number,dev.norm, main.name,dev.name,dev.parent,main.id order by raport_number DESC"""

		measurements = q_run(connD, querry)
		querry = "select rem.raport_number,rem.id,main.name,dev.name,dev.parent,main.id from remarks as rem left join devices as dev on rem.id = dev.id left join main as main on dev.parent = main.id group by rem.raport_number,rem.id,main.name,dev.name,dev.parent,main.id order by main.name, raport_number, rem.id"

		##LISTA STATKOW NO CBM - TO IGNORE####

		forbiden = list()
		forbiden.append(52)
		forbiden.append(56)
		forbiden.append(57)
		forbiden.append(86)
		forbiden.append(87)
		forbiden.append(95)
		forbiden.append(111)
		forbiden.append(123)
		forbiden.append(131)
		forbiden.append(132)
		forbiden.append(137)
		forbiden.append(140)
		forbiden.append(141)
		forbiden.append(147)
		forbiden.append(156)
		forbiden.append(168)
		forbiden.append(171)
		forbiden.append(173)
		forbiden.append(179)
		forbiden.append(185)
		forbiden.append(189)
		forbiden.append(193)
		forbiden.append(200)
		forbiden.append(202)
		forbiden.append(203)
		forbiden.append(204)
		forbiden.append(205)
		remarksraportstemp = q_run(connD, querry)
		RemExistList = list()
		for line in remarksraportstemp:
			RemExistList.append(str(
				str(line[5]).strip() + '#' + str(line[2]).strip() + '##' + str(line[0]).strip() + '###' + str(
					line[1]).strip() + '####' + str(line[3]).strip()))
		p = -1
		reportlist1 = list()
		for line in measurements:
			p += 1
			lim = countLimit(line[3], line[2])

			if line[6] not in forbiden:
				if str(lim) == 'Cl. D' or str(lim) == 'V. III':
					# print(str(line[1]) + ' ' + str(line[5]) + ' ' + str(lim) + ' ' + str(line[3]) + ' ' + str(line[2]) )
					strip = str(
						str(line[7]).strip() + '#' + str(line[4]).strip() + '##' + str(line[1]).strip() + '###' + str(
							line[0]).strip() + '####' + str(line[5]).strip())
					if not strip in reportlist1:
						reportlist1.append(strip)

		replist = [item for item in reportlist1 if item not in RemExistList]

		noRemList = list()

		for line in replist:
			hash1 = line.find("#")
			hash2 = line.find("##")
			hash3 = line.find("###")
			hash4 = line.find("####")
			shipid = line[:hash1]
			shipname = line[hash1 + 1:hash2]
			rn = line[hash2 + 2:hash3]
			devid = line[hash3 + 3:hash4]
			devname = line[hash4 + 4:]

			noRemStrip = [shipname, shipid, rn, devname, devid]
			noRemList.append(noRemStrip)

		return list(noRemList)


	def unknowstateremarks():
		querry = "select id,raport_number from remarks where sended is null order by raport_number, id"
		nosendedlist = q_run(connD, querry)
		return (nosendedlist)
	def NoFdbRem():
		querry = """ select rem.id, dev.name, rem.raport_number, main.name,main.id
	from remarks as rem
	left join feedbacks as fdb on rem.id = fdb.id and rem.raport_number = fdb.raport_number
	left join devices as dev on rem.id = dev.id
	left join main as main on dev.parent = main.id
	where rem.sended = True and fdb.feedback is null and dev.name is not null
	group by  rem.id , dev.name, rem.raport_number,main.name,rem.name,main.id  order by main.name,rem.raport_number,rem.name """
		nofdblist = q_run(connD, querry)	
		return (nofdblist)
	def FdbFlagLeft():
		querry = "select id,raport_number from feedbacks where fdbflag is null and parent not in(select id from main  where parent = 10) "
		fdbflagleft = q_run(connD, querry)	
		return (fdbflagleft)	
	def CostFlagLeft():
		querry = "select id,raport_number from feedbacks where costflag IS Null and fdbflag is not null and fdbflag<> 7 and fdbflag<> 8 and fdbflag<> 9"
		costflagleft = q_run(connD, querry)	
		return (costflagleft)	
	def details1():
		with open('Cl D no remark.csv', 'w', newline='') as file:
			for l in r1:
				file.write(str(l))
				file.write('\n')

	def details2():	
		with open('Remarks with unknow stats.csv', 'w', newline='') as file:
			for l in r2:
				file.write(str(l))
				file.write('\n')
	def details3():	
		with open('Sent remarks without feedbacks.csv', 'w', newline='') as file:
			for l in r3:
				file.write(str(l))
				file.write('\n')
	def details4():	
		with open('Feedback no fdbflag.csv', 'w', newline='') as file:
			for l in r4:
				file.write(str(l))
				file.write('\n')
	def details5():	
		with open('Feedback no costflag.csv', 'w', newline='') as file:
			for l in r5:
				file.write(str(l))
				file.write('\n')



	def run1():
		Monitor.ShipsApplication(r1)
	def run2():
		UnknowSentFlag.unknowremarks()
	def run3():
		RemarksWithoutFeedbacksMonitor.ShipsApplication(RemarksWithoutFeedbacksMonitor.nofdblistF())



	MonitorWindow = tk.Tk()
	MonitorWindow.title("Feedback Monitor")



	label1 = tk.Label(MonitorWindow, text  = 'Class D without remarks: ')
	label2 = tk.Label(MonitorWindow, text  = 'Remarks with unknow state: ')
	label3 = tk.Label(MonitorWindow, text  = 'Sent remarks without feedbacks: ')
	label4 = tk.Label(MonitorWindow, text  = 'Feedback flag left: ')
	label5 = tk.Label(MonitorWindow, text  = 'Cost flag left: ')

	r1 = ClDNoRem()
	r2 = unknowstateremarks()
	r3 = NoFdbRem()
	r4 = FdbFlagLeft()
	r5 = CostFlagLeft()
	labelr1 = tk.Label(MonitorWindow, text  = len(r1))
	labelr2 = tk.Label(MonitorWindow, text  = len(r2))
	labelr3 = tk.Label(MonitorWindow, text  = len(r3))
	labelr4 = tk.Label(MonitorWindow, text  = len(r4))
	labelr5 = tk.Label(MonitorWindow, text  = len(r5))


	button1 = tk.Button(MonitorWindow, text = 'Details',command = details1)
	button2 = tk.Button(MonitorWindow, text = 'Details',command = details2)
	button3 = tk.Button(MonitorWindow, text = 'Details',command = details3)
	button4 = tk.Button(MonitorWindow, text = 'Details',command = details4)
	button5 = tk.Button(MonitorWindow, text = 'Details',command = details5)

	button1s = tk.Button(MonitorWindow, text = 'Run Software',command = run1)
	button2s = tk.Button(MonitorWindow, text = 'Run Software',command = run2)
	button3s = tk.Button(MonitorWindow, text = 'Run Software',command = run3)
	label4s = tk.Label(MonitorWindow, text = 'Soft in Overmind')
	label5s = tk.Label(MonitorWindow, text = 'Soft in Overmind')

	label1.grid(row=0,column=0)
	label2.grid(row=1,column=0)
	label3.grid(row=2,column=0)
	label4.grid(row=3,column=0)
	label5.grid(row=4,column=0)
	labelr1.grid(row=0,column=1)
	labelr2.grid(row=1,column=1)
	labelr3.grid(row=2,column=1)
	labelr4.grid(row=3,column=1)
	labelr5.grid(row=4,column=1)
	button1.grid(row=0,column=2)
	button2.grid(row=1,column=2)
	button3.grid(row=2,column=2)
	button4.grid(row=3,column=2)
	button5.grid(row=4,column=2)
	button1s.grid(row=0,column=3)
	button2s.grid(row=1,column=3)
	button3s.grid(row=2,column=3)
	label4s.grid(row=3,column=3)
	label5s.grid(row=4,column=3)

	MonitorWindow.mainloop()
	
runprogram()