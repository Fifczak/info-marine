from Analyzer import *


from functionsfromweb import *

import tkinter as tk

import tkinter as tk
from tkinter import *
from tkinter import ttk 


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


            Datasheet(connD)

class Datasheet(connD,parent):
	limits = list()

	def __init__(self):
		pass


	def loadquerrys():
		querry1 = "select raport_number from measurements_low where parent = " + str(parent) + " group by raport_number order by raport_number DESC "
		resultr = q_run(connD, querry1)
		querry2 = "SELECT dss.id, CASE WHEN dss.id ~E'^\\\d+$' THEN	(select name from devices where cast(devices.id as text)  =  dss.id limit 1) ELSE (select id from ds_structure where id  =  dss.id limit 1) END as sortint, dss.sort FROM ds_structure as dss where dss.parent = " + str(parent)
		results = q_run(connD, querry2)
		querry3 = """select ml.id, ml.raport_number, ml.point,  ml.value, ml2.value, dev.norm
						from measurements_low as ml 
						left join points as pts on ml.id = pts.id and ml.point = pts.point
						left join (select id,raport_number, point, value 
												from measurements_low where parent = '""" + str(parent) + """' and type = 'envelope P-K') as ml2 
												on ml.id=ml2.id and ml.raport_number = ml2.raport_number
												and ml.point = ml2.point 
						left join devices as dev on ml.id = dev.id
						where ml.parent =  """ + str(parent) + """ and ml.type = 'RMS' and ml.id <> 0 order by id, raport_number, sort"""
		resultm = q_run(connD, querry3)
		querry = "select id, raport_number, mcremark from mcdata where raport_number is not null and id is not null"
		resultmc = q_run(connD, querry)
		querry = "select id, raport_number, remark from remarks where raport_number is not null and id is not null"
		resultrem = q_run(connD, querry)
		querry = "select id, raport_number, feedback from feedbacks where raport_number is not null and id is not null"
		resultfed = q_run(connD, querry)
		querry = """select standard,
								limit_1_value,limit_1_name,
								limit_2_value,limit_2_name, 
								limit_3_value,limit_3_name,
								limit_4_value,limit_4_name,
							envflag
						from standards"""
		limits = q_run(connD,querry)
		
		return([resultr,results,resultm,resultmc,resultrem,resultfed,limits])
	def countLimit(standard,value):
		value = float(value)
		
		for limNo in limits:
			if str(limNo[0]) == standard:
				if value <= float(limNo[3]): #IF LIM1
					limStr = str(limNo[2])
					break
				else:
					if value <=float(limNo[5]): #IF LIM2
						limStr = str(limNo[4])
						break
					else:
						if value <=float(limNo[7]): #IF LIM3
							limStr = str(limNo[6])
							break
						else:
							limStr = str(limNo[8])
							break
		try:
			return limStr
		except:
			print('Limit count error')
	def onselect(evt):
		w = evt.widget
		index = int(w.curselection()[0])
		value = w.get(index)
		id_ = results[index][0]
		update_device_parameters(id_)
		replistc = list()
		replistc.clear()
		try:
			for widget in measBframe.winfo_children():
				widget.destroy()
		except:
			print('no MASTERmeasframe')



		measframe = Frame(measBframe)	
		
		if id_.isdigit() == True:
			querry = "select raport_number from measurements_low where id = " + id_ + " group by raport_number order by raport_number DESC"
			replistc = q_run(connD,querry)

		for i in replistc:
			make_frame_meas(Frame(measframe,height=2, bd=1, relief=SUNKEN),i , id_)



		measframe.pack()
	def onselect2(evt,id,rn):
		w = evt.widget
		index = int(w.curselection()[0])
		index += 1
		value = w.get(index)
		querry = "select point from points where id = " + str(id) + " and sort = " + str(index)
		point = q_run(connD,querry)[0][0]
		print(str(id))
		print(str(rn))
		print(str(point))
		
		analyzer_frame('database_inDS',str(id),str(rn),str(point),'Vel')
	def update_device_parameters(id_):
		querry = "select name, type, model from devices where id = " + str(id_) 
		devparams = q_run(connD, querry)
		devicename.configure(text = devparams[0][0])
		deviceid.configure(text = str(id_))
		devicetype.configure(text = devparams[0][1])
		devicemodel.configure(text = devparams[0][2])
	def make_frame_meas(self,reportno, id):
	
		try:
			for widget in self.winfo_children():
				widget.destroy()
		except:
			pass
			
		rButton = tk.Button(self)
		xcord = 0
		pointlist = tk.Listbox(self)
		pointlist.config(width=5)
		rmslist = tk.Listbox(self)
		rmslist.config(width=7)
		envlist = tk.Listbox(self)
		envlist.config(width=7)
		for x in resultm:
			if x[1] == reportno[0]:
				rButton.configure(text = reportno[0])
				if (str(x[0])).strip() == (str(id)).strip():
						#try:
						pointlist.insert(END,str(x[2]))
						rmslist.insert(END,round(float(x[3]),3))
						rmslist.bind('<Double-Button>' ,lambda event,id = x[0], rn = x[1] :onselect2(event,id,rn))
						#print(str(x[5]))
						limStr = countLimit(str(x[5]), x[3])
						#print((str(limStr)).strip()) 
						if (str(limStr)).strip() == 'Cl. D' or (str(limStr)).strip() == 'V. III' or (str(limStr)).strip() == 'V.III' or (str(limStr)).strip() == 'Out of limit':
							rmslist.itemconfig(END, bg='Red')
						elif (str(limStr)).strip() == 'Cl. C'or (str(limStr)).strip() == 'V. II' :
							rmslist.itemconfig(END, bg='Yellow')	
						elif (str(limStr)).strip() == 'Cl. B' or (str(limStr)).strip()  == 'Cl. A' or (str(limStr)).strip() == 'V. I' or (str(limStr)).strip() == 'V.I' or (str(limStr)).strip() == 'In limit': 
							rmslist.itemconfig(END, bg='Green')									
							
						# except:
							# rmslist.insert(END,'-')
						try:
							envlist.insert(END,round(float(x[4]),3))
						except:
							envlist.insert(END,'-')

						
		
		
		mcremark = tk.Text(self,height=10, width=20)
		remark = tk.Text(self,height=10, width=20)
		feedback = tk.Text(self,height=10, width=20)
		# for x in resultmc:
			# if (str(x[0])).strip() == (str(id)).strip():
				# if (str(x[1])).strip() == (str(reportno[0])).strip():
					# mcremark.insert(INSERT, x[2])
					# break
					
					
		for mcx in resultmc:
			if (str(mcx[0])).strip() == (str(id)).strip():
				if (str(mcx[1])).strip() == (str(reportno[0])).strip():
					mcremark.insert(INSERT, mcx[2])
					break	
		for x in resultrem:
			if (str(x[0])).strip() == (str(id)).strip():
				if (str(x[1])).strip() == (str(reportno[0])).strip():
					remark.insert(INSERT, x[2])
					break
		for fdx in resultfed:
			if (str(fdx[0])).strip() == (str(id)).strip():
				if (str(fdx[1])).strip() == (str(reportno[0])).strip():
					feedback.insert(INSERT, fdx[2])
					break
					
		rButton.pack()		
		pointlist.pack(side = LEFT)
		rmslist.pack(side = LEFT)
		envlist.pack(side = LEFT)
		mcremark.pack(side = LEFT)
		remark.pack(side = LEFT)
		feedback.pack(side = LEFT)
	
		self.pack(side = LEFT, fill=tk.BOTH, expand=True)
	def deviceslist(mylist):
		def lastrn(line0):
			for line3 in resultRS:
				for line2 in resultm:
					if str(line2[0]) == str(line0):
						if str(line3[0]).strip() == line2[1]:
							return line2[1]
		ycord = 0
		querry = "select raport_number from measurements_low where parent = " + str(parent)  + " group by raport_number order by raport_number DESC"
		resultRS = q_run(connD,querry)
		xcord = 0
		
		for line in results:
			limitStr = ''
			maxValList = list()
			lrn = lastrn(line[0])
			if line[0].isnumeric() == True:
				tempval = 0
				tempval2 = 0
				limStr = 'ERR'
				for x in resultm:
					if str(x[1]) == str(lrn) :
						if (str(x[0])).strip() == (str(line[0])).strip():
							if tempval < float(x[3]):
								tempval = float(x[3])
								limStr = countLimit(str(x[5]), x[3])
							try:
								if tempval2 < float(x[4]):
									tempval2 = float(x[4])
							except:
								pass
					
					
				mylist.insert(END, results[xcord][1] + '(' +str(lrn) + ':'+ str(limStr)+')')
	
				
			else:
				mylist.insert(END, results[xcord][1])
				mylist.itemconfig(END, bg='blue')
			xcord += 1
		mylist.bind('<<ListboxSelect>>', onselect)
		cs = mylist.curselection()
		devicesscrollbar.config( command = mylist.yview )
		mylist.pack( side = LEFT, fill = BOTH )

	inputdata=loadquerrys()
	resultr = inputdata[0]
	results = inputdata[1]
	resultm = inputdata[2]
	resultmc = inputdata[3]
	resultrem = inputdata[4]
	resultfed = inputdata[5]
	limits = inputdata[6]

	Fwindow = tk.Tk()
	Fwindow.title("Info Datasheet")
	devicesscrollbar = Scrollbar(Fwindow)
	devicesscrollbar.pack(side = LEFT, fill=Y )
	mylist = Listbox(Fwindow, yscrollcommand = devicesscrollbar.set )
	mylist.config(width=0)
	deviceslist(mylist)
	
	deviceframe = Frame(Fwindow)
	devicename = tk.Label(deviceframe, text = "Name")
	deviceid = tk.Label(deviceframe, text = "id")
	devicetype = tk.Label(deviceframe, text = "TYPE: ")
	devicemodel = tk.Label(deviceframe, text = "MODEL: ")
	deviceframe.pack(side = LEFT)
	deviceid.pack(side = TOP)
	devicename.pack(side = TOP)
	devicetype.pack(side = TOP)
	devicemodel.pack(side = TOP)
	MASTERmeasframe = Frame(Fwindow,width=300,height=300)
	MASTERmeasframe.pack(side = LEFT)
	rapmeasscrol = Scrollbar(MASTERmeasframe,orient = HORIZONTAL)
	rapmeasscrol.pack(side = BOTTOM, fill=X )
	measBframe = Canvas(MASTERmeasframe,xscrollcommand=rapmeasscrol.set,scrollregion=(0,0,500,500))
	rapmeasscrol.config(command=measBframe.xview)
	measBframe.pack(side = LEFT)
	
	Fwindow.mainloop()

	



	


