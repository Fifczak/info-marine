from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk

#from ttk import *
from pathlib import Path
import psycopg2
import csv
host = '192.168.8.125'
username = 'filipb'
password =  '@infomarine'
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

# def Login(): TRZEBA ZROBIĆ LOGOWANIE
	# class LogApplication(Frame):
		# def __init__(self,master):
			# super(LogApplication, self).__init__(master)#Set __init__ to the master class
			# self.grid()
			# self.create_main()#Creates function
		# def create_main(self):
			# self.title = Label(self, text="Info Datasheet")#TITLE 
			# self.title.grid(row=0, column=2)
			# self.user_entry_label = Label(self, text="Username: ")#USERNAME LABEL
			# self.user_entry_label.grid(row=1, column=1)
			# self.user_entry = Entry(self, text="Username: ")  #USERNAME ENTRY BOX
			# self.user_entry.grid(row=1, column=2)
			# self.pass_entry_label = Label(self, text="Password: ")#PASSWORD LABEL
			# self.pass_entry_label.grid(row=2, column=1)
			# self.pass_entry = Entry(self, show="*")    #PASSWORD ENTRY BOX
			# self.pass_entry.grid(row=2, column=2)
			# try:
				# with open('log.csv') as csvfile:
					# openfile = csv.reader(csvfile, delimiter=' ')
					# p = -1
					# for lines in openfile:
						# p += 1
						# if p == 0:
							# self.user_entry.insert(0,str(lines[0]))
						# if p == 1:
							# self.pass_entry.insert(0,str(lines[0]))
			# except:
				# pass
			# self.var = IntVar()
			# self.checksave = Checkbutton(self, text="Remember", variable=self.var)      
			# self.checksave.grid(row=3, column=2)
			# self.sign_in_butt = Button(self, text="Sign In",command = self.logging_in)#SIGN IN BUTTON
			# self.sign_in_butt.grid(row=5, column=2)
		# def logging_in(self):
			# user_get = self.user_entry.get()#Retrieve Username
			# pass_get = self.pass_entry.get()#Retrieve Password
			# if bool(app.var.get()) == True:
				# config = Path('log.csv')
				# with open('log.csv', 'w', newline='') as csvfile:
					# filewriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
					# filewriter.writerow([user_get])
					# filewriter.writerow([pass_get])
			# connD = [user_get,pass_get,host]
			# querry = "SELECT id from main limit 1"
			# usercheck = ''
			# print(connD)
			# print(querry)
			# try:
			# usercheck =  q_run(connD,querry)
				
			# except:
				# pass
			# if usercheck:
				# root.destroy()
				# print(usercheck[0])	
				# querry = "select name,id from main where parent =1 order by name"
				# ownerlist = q_run(connD, querry)
				# querry = "select name,id,parent from main where parent <> 1 order by name"
				# shiplist = q_run(connD, querry)
				# ShipsApplication()
	# root = Tk()
	# root.title("Login")
	# root.geometry("200x120")
	# app = LogApplication(root)#The frame is inside the widgit
	# root.mainloop()#Keeps the window open/running

def ClDNoRem():
		def countLimit(standard,value):
					limSrt ='NOPE'
					for limNo in limits:
						if str(limNo[0]) == str(standard):
							if value <= float(limNo[3]): #IF LIM1
								limSrt = str(limNo[2])
								break
							else:
								if value <=float(limNo[5]): #IF LIM2
									limSrt = str(limNo[4])
									break
								else:
									if value <=float(limNo[7]): #IF LIM3
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
		limits = q_run(connD,querry)
		

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
		RemExistList =list()
		for line in remarksraportstemp:
			RemExistList.append(str(str(line[5]).strip() + '#' + str(line[2]).strip() + '##' + str(line[0]).strip()+'###'+str(line[1]).strip()+'####'+str(line[3]).strip()))
		p = -1
		reportlist1 = list()
		for line in measurements:
			p += 1
			lim = countLimit(line[3],line[2])

			if line[6] not in forbiden:
				if str(lim) == 'Cl. D' or str(lim) == 'V. III':
					#print(str(line[1]) + ' ' + str(line[5]) + ' ' + str(lim) + ' ' + str(line[3]) + ' ' + str(line[2]) )
					strip = str(str(line[7]).strip() + '#' + str(line[4]).strip() +'##'+ str(line[1]).strip()+'###'+str(line[0]).strip()+'####'+str(line[5]).strip())
					if not strip in reportlist1:
						reportlist1.append(strip)
						
		replist =  [item for item in reportlist1 if item not in RemExistList]
		print('Ilosc pomiarow w klasie D bez remarksa: ' + str(len(replist)))

		
		replist.sort()

		noRemList = list()

		for line in replist:
			hash1 = line.find( "#" )
			hash2 = line.find( "##" )
			hash3 = line.find( "###" )
			hash4 = line.find( "####" )
			shipid = line[:hash1]
			shipname = line[hash1+1:hash2]
			rn = line[hash2+2:hash3]
			devid = line[hash3+3:hash4]
			devname = line[hash4+4:]
			
			noRemStrip = [shipname,shipid,rn,devname,devid]
			noRemList.append(noRemStrip)
			
			
			
		return list(noRemList)
		
def ShipsApplication(ClDNoRemList):
	
	def LoadRaportList(shipid):
	
		class frame_rem:
		
			#def __init__(self):
				# name = tk.Label(self,text = str(rn)).pack(side = LEFT)
				#textfield = Text(measCframe,width=50,height=5)
				
			def __init__(self,measCframe,devname,rn,id,parent):
				self.parent = parent
				self.rn = rn
				self.id=id
				self.name = tk.Label(measCframe,text = str(devname))
				self.textfield = tk.Text(measCframe,width=50,height=5)
				self.name.pack(side = LEFT)
				querry = "select limit_4_value from standards where standard = (select norm from devices where id = " + str(id) + ")"
				limstr = round(float(q_run(connD,querry)[0][0]),1)
				
				self.limitF = tk.Label(measCframe,text = limstr)
				self.limitF.pack(side = LEFT)
				self.textfield.pack(side = LEFT)
				measCframe.pack(side = TOP, fill=tk.BOTH, expand=True)
		
		# def make_frame_rem(self,rn):
						
			# name = tk.Label(self,text = str(rn)).pack(side = LEFT)
			# textfield = tk.Text(self,width=50,height=5).pack(side = LEFT)
			# self.pack(side = TOP, fill=tk.BOTH, expand=True)		
	
		def selectreport(evt):
			def upload():
				for line in remlist:
					if line.textfield.get("1.0",END).strip() != '':

						querry = "select date from measurements_low where id = "+str(line.id)+" and raport_number = '"+str(line.rn)+"' limit 1"
						print(querry)
						measdate = str(q_run(connD, querry)[0][0])

						querry = "INSERT INTO REMARKS(id,raport_number,remark,parent,documentdate) VALUES (" +str(line.id)+",'" +str(line.rn)+ "','" +str((line.textfield.get("1.0",END)).strip())+ "'," + str(line.parent) +",'" + str(measdate) + "')"
						
						what = q_run(connD, querry)
				root2.destroy()
				ShipsApplication(ClDNoRem())
				
			w = evt.widget
			index = int(w.curselection()[0])
			value = w.get(index)
			nrrap= RapList[index]
			
			###
			devices = list()
			chList = list()
			for line in ClDNoRemList:
				if str(line[2]).strip() == str(nrrap):
					if line[3] not in chList:
						chList.append(line[3])
						strip = [line[3],line[2],line[4],line[1]]
						devices.append(strip)
			
			
			try:
				for widget in measBframe.winfo_children():
					widget.destroy()
			except:
				pass
			MASTERmeasframe.pack(side = TOP, anchor=S)
			measBframe.pack(side = TOP)

			UploadButton = Button(measBframe, text = 'Upload and refresh',command = upload)
			UploadButton.pack()
			remlist = list()
			backRemList = list()
			for i in devices:
				measCframe = tk.Frame(measBframe,height=2, bd=1, relief=SUNKEN)
				X = frame_rem(measCframe,i[0],i[1],i[2],i[3])
				#X = make_frame_rem(measCframe,i)
				remlist.append(X)

			

			
		RapList =  list()
		for line in ClDNoRemList:
			if str(line[1]).strip() == str(shipid).strip():
				if str(line[2]) not in RapList:
					RapList.append(line[2])
					
		RapList.sort()	
		Raportlist.delete(0, END)
		for line in RapList:
			Raportlist.insert(END,line)
		Raportlist.bind('<<ListboxSelect>>', selectreport)	
			
			
			
	def LoadShipsList():
		def selectship(evt):
			w = evt.widget
			index = int(w.curselection()[0])
			value = w.get(index)
			id_ = shList[index][1]
			LoadRaportList(id_)
			Raportlist.pack(side = LEFT, anchor=N)

			
			
			
		shList =  list()
		tryList = list()
		for line in ClDNoRemList:
			if str(line[1]) not in tryList:
				tryList.append(line[1])
				strip = [line[0], line[1]]
				shList.append(strip)
		shList.sort()	
		for line in shList:
			Shiplist.insert(END,line[0])
		Shiplist.bind('<Double-Button>' , selectship)
		
	root2 = Tk()
	root2.title("Remarks")
	

	Shiplist = tk.Listbox(root2)
	Shiplist.config(width=15)
	Shiplist.pack(side = LEFT, anchor=N)

	Raportlist = tk.Listbox(root2)
	Raportlist.config(width=15)
	
	LoadShipsList()
	
	
	MASTERmeasframe = Frame(root2,width=300,height=300)
	

	measBframe = Canvas(MASTERmeasframe)#,yscrollcommand=rapmeasscrol.set,scrollregion=(0,0,500,500))
	
	
	
	
	
	root2.mainloop()	




ClDNoRemList = ClDNoRem()

#print(list(ClDNoRemList))
ShipsApplication(ClDNoRemList)