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

def Harvester():
	class DataFrame(object):
		def __init__(self):
			self.id = ''
			self.rn = ''
			self.measdate = ''
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
					print (worksheet.cell(x, 1).value)
					print (worksheet.cell(x +radj, 7).value)
					print('RMS')

			#dFrame.rn = str((worksheet.cell(0, ((x * 5) + 8))).value)




	Harvest()
Harvester()

