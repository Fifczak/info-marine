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

username = 'testuser'
password = 'info'
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

measlist = list()

def Harvester():
	class DataFrame(object):
		def __init__(self):
			self.id = ''
			self.rn = ''
			self.measdate = ''
			self.point = ''
			self.rms = ''
			self.env = ''

	def Harvest():
		def checkpointsno(start):
			a = 1
			while (worksheet.cell(start + a, 7).value) != '':
				a += 1
			return a

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
		progress_bar = ttk.Progressbar(pbars,orient = 'horizontal',lengt = 286, mode = 'determinate')

		progress_bar['maximum'] =(ysize)
		progress_bar.pack(side = TOP)
		x=-1
		for row in range(ysize):
			x+=1
			progress_bar['value'] = x
			progress_bar.update()

			if (worksheet.cell(x, 0).value).isnumeric() == True:
				for radj in range(1,checkpointsno(x)):
					if (worksheet.cell(x + radj, 8).value) != '':
						rms = DataFrame()
						rms.id = (worksheet.cell(x, 0).value)
						rms.rn = (worksheet.cell(0, 8).value)
						rms.measdate = ((str(datetime.datetime(*xlrd.xldate_as_tuple(worksheet.cell(x , 8).value, workbook.datemode))))[:10])
						rms.point = (worksheet.cell(x +radj, 7).value)
						rms.rms = (worksheet.cell(x + radj, 8).value)
						measlist.append(rms)
					if (worksheet.cell(x + radj, 9).value) != '':
						env = DataFrame()
						env.id = (worksheet.cell(x, 0).value)
						env.rn = (worksheet.cell(0, 8).value)
						env.measdate = (
						(str(datetime.datetime(*xlrd.xldate_as_tuple(worksheet.cell(x, 8).value, workbook.datemode))))[
						:10])
						env.point = (worksheet.cell(x + radj, 7).value)
						env.env = (worksheet.cell(x + radj, 9).value)
						measlist.append(env)

		progress_bar['maximum'] = len(measlist)
		x=0
		for item in measlist:
			x+=1
			progress_bar['value'] = x
			progress_bar.update()
			if item.rms != '':

				querry = "INSERT INTO MEASUREMENTS_LOW (id, raport_number,point,type,unit,date,value)" \
						 " VALUES(" + str(item.id) + ",'" + str(item.rn) + "','" + str(item.point) +"','"\
						 "RMS','[mm/s]','" + str(item.measdate) + "'," + str(item.rms) +")"
				q_run(connD,querry)
				

			if item.env !='':
				querry = "INSERT INTO MEASUREMENTS_LOW (id, raport_number,point,type,unit,date,value)" \
						 " VALUES(" + str(item.id) + ",'" + str(item.rn) + "','" + str(item.point) + "','" \
																									 "envelope P-K','[m/s2]','" + str(
					item.measdate) + "'," + str(item.env) + ")"
				q_run(connD, querry)

	Harvest()
Harvester()

