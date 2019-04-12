## HARVESTER BY FIFCZAK 2019
import datetime
import xlrd
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter import Tk
from tkinter import filedialog
import psycopg2
username = 'gosiam'
password = 'infog'
host = '192.168.8.125'
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

def Harvester():
	class DataFrame(object):
		def __init__(self):
			self.id = ''
			self.rn = ''
			self.rem = ''
			self.fed = ''
			self.rdate = ''
			self.fdate = ''
	def Harvest(Datasheet):
		Tk().withdraw()
		file = filedialog.askopenfilename()
		workbook = xlrd.open_workbook(file)
		worksheet = workbook.sheet_by_index(0)
		xsize = worksheet.ncols
		ysize = worksheet.nrows
		Nrap = int((xsize -8) /5 )
		x=0
		
		pbars = tk.Tk()
		pbars.title("Reading Marvib measurement file")
		progress_bar1 = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 286, mode = 'determinate')
		progress_bar2 = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 286, mode = 'determinate')
		progress_bar1['maximum'] =(Nrap)
		progress_bar1.pack(side = TOP)
		progress_bar2['maximum'] =(ysize)
		progress_bar2.pack(side = TOP)			
		for column in range(Nrap): # Tu szukamy raportów
			y=0
			progress_bar1['value'] = x
			progress_bar1.update()
			lastdater = ''
			lastdatef = ''
			for row in range(ysize):
				progress_bar2['value'] = y
				progress_bar2.update()
				if str(worksheet.cell_value(rowx=y, colx=0)).isdigit() == True:
					dFrame = DataFrame()
					if str(worksheet.cell_value(rowx=y+1, colx=((x*5)+8+3))) != '' or str(worksheet.cell_value(rowx=y+1, colx=((x*5)+8+4))) != '' :
						dFrame.rn = str((worksheet.cell(0,((x*5)+8))).value)
						dFrame.id = str(worksheet.cell(y,0).value)
						dFrame.rem = str(worksheet.cell(y+1,((x*5)+8)+3).value)
						dFrame.fed = str(worksheet.cell(y+1,((x*5)+8)+4).value)
						if str(worksheet.cell_value(rowx=y+1, colx=((x*5)+8+3))) != '':
							try:
								if str(worksheet.cell_value(rowx=y, colx=((x*5)+8+3))) == '':
									dFrame.rdate = (str(worksheet.cell_value(rowx=1, colx=((x*5)+8))[:10]))

								else:
									dFrame.rdate = datetime.datetime(*xlrd.xldate_as_tuple(worksheet.cell_value(rowx=y, colx=((x*5)+8+3)), workbook.datemode)) 
								try:
									querry = "SELECT id FROM REMARKS where id = " + str(dFrame.id) + " and raport_number = '" + str(dFrame.rn) + "'"
									try:
										cVal = q_run(connD,querry)[0][0]
									except:
										cVal = q_run(connD,querry)
									if str(cVal) == '' or cVal == [] :
										querry = """INSERT INTO REMARKS (id,raport_number,documentdate,remark) VALUES
										(""" + str(dFrame.id) + ",'"+str(dFrame.rn)+"','" + str(dFrame.rdate)[:10] + "','" + str(dFrame.rem)+"')"
										q_run(connD,querry)
										Uploaded.append('Succesfully uploaded remark: '+ str(dFrame.rn) + ' ' + str(dFrame.id))
								except:
									errorList.append('Error: run remark querrys in '+ str(dFrame.rn) + ' ' + str(dFrame.id))
							except:
								#errorList.append('Error: remark date in '+ str(dFrame.rn) + ' ' + str(dFrame.id))
								pass

								
								
								
								
								
								
								
								
						if str(worksheet.cell_value(rowx=y+1, colx=((x*5)+8+4))) != '':
							try:
								dFrame.fdate = datetime.datetime(*xlrd.xldate_as_tuple(worksheet.cell_value(rowx=y, colx=((x*5)+8+4)), workbook.datemode)) 
								lastdatef = dFrame.fdate
								
								try:
									querry = "SELECT id FROM feedbacks where id = " + str(dFrame.id) + " and raport_number = '" + str(dFrame.rn) + "'"
									try:
										cVal = q_run(connD,querry)[0][0]
									except:
										cVal = q_run(connD,querry)
									if str(cVal) == '' or cVal == [] :
										querry = """INSERT INTO feedbacks (id,raport_number,documentdate,feedback) VALUES
										(""" + str(dFrame.id) + ",'"+str(dFrame.rn)+"','" + str(dFrame.fdate)[:10] + "','" + str(dFrame.fed)+"')"
										q_run(connD,querry)
										Uploaded.append('Succesfully uploaded feedback: '+ str(dFrame.rn) + ' ' + str(dFrame.id))
								except:
									errorList.append('Error: run feedback querrys in '+ str(dFrame.rn) + ' ' + str(dFrame.id))	
							except:
								dFrame.fdate = lastdatef
								#errorList.append('Error: feedback date in '+ str(dFrame.rn) + ' ' + str(dFrame.id))


									
						try:
							DataSheet.append(dFrame)
						except:
							errorList.append('Error: no dFrame to append'+ str(dFrame.rn) + ' ' + str(dFrame.id))

					
					

									
					
					
				y += 1
			x +=1			
			

	errorList = list()
	DataSheet = list()
	Uploaded = list()
	Harvest(DataSheet)
	
	
	with open('Harvester_founds.csv', 'w', newline='') as file:
		for l in DataSheet:
			file.write(l.rn)
			file.write(' ')
			file.write((l.id))
			file.write('\n')
	
	with open('Harvester_uploads.csv', 'w', newline='') as file:
		for l in Uploaded:
			file.write(str(l))
			file.write('\n')
	
	with open('Harvester_errors.csv', 'w', newline='') as file:
		for l in errorList:
			file.write(str(l))
			file.write('\n')

Harvester()

