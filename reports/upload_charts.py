import xlwings as xw

import psycopg2
import os
import pandas as pd
from math import sqrt

import numpy as np
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *
tk=Tk()


def lastRow(idx, workbook, col):
	""" Find the last row in the worksheet that contains data.

	idx: Specifies the worksheet to select. Starts counting from zero.

	workbook: Specifies the workbook

	col: The column in which to look for the last cell containing data.
	"""

	ws = workbook.sheets[idx]

	lwr_r_cell = ws.cells.last_cell		 # lower right cell
	lwr_row = lwr_r_cell.row			 # row of the lower right cell
	lwr_cell = ws.range((lwr_row, col))	 # change to your specified column

	if lwr_cell.value is None:
		lwr_cell = lwr_cell.end('up')	 # go up untill you hit a non-empty cell

	return lwr_cell.row

def column_string(n):
	string = ""
	while n > 0:
		n, remainder = divmod(n - 1, 26)
		string = chr(65 + remainder) + string
	return string

def prepare_and_upload(kuser,kpassword,khost,parent,setsno):
	kport = "5432"
	kdb = "postgres"


	#cs = ' host="localhost",database="postgres", user= "postgres" , password="info" '
	cs = "dbname=%s user=%s password=%s host=%s port=%s"%(kdb,kuser,kpassword,khost,kport)

	conn = None
	conn = psycopg2.connect(str(cs))
	#conn = psycopg2.connect(host="localhost",database="postgres", user= "postgres" , password="info")
	
	wb = xw.Book.caller()
	sht = xw.Book.caller().sheets[3]
	#x = int(sht.cells[0,0].value)
	
	k = 0
	progress=Progressbar(tk,orient=HORIZONTAL,length=200,mode='determinate')
	
	step = 100 / int(setsno)
	for i in range(int(setsno)):
		k += 1
		progress['value']= k * step
		tk.update_idletasks()
		progress.pack()
		colstr = column_string(k)
		lr = lastRow(3,wb,k)

		names = wb.sheets[3].range(colstr + ':' + colstr)[6:lr].value
		if khost == "localhost" :
			spath_ = 'C:\\overmind\\temp\\scores' + str(i) + '.csv'
			upath_ = 'C:\\overmind\\temp\\scores' + str(i) + '.csv'
		elif khost == "192.168.8.125":
			spath_ = r"\\192.168.8.125\Public\scores" + str(i) + ".csv"
			upath_ = r'/home/filip/Public/scores' + str(i) + '.csv'
		np.savetxt(spath_, [p for p in zip(names)], delimiter=',', fmt='%s')
		
		#names = wb.sheets[3].(column=1)[1:x].value
		#x = column_string(56)

		id = sht.cells[0,i].value
		point = sht.cells[1,i].value
		report_number = sht.cells[2,i].value
		date = sht.cells[5,i].value
		domain = sht.cells[3,i].value
		type = sht.cells[4,i].value
		typel = 'RMS'
		unit = '[mm/s]'
		chart = "lo_import('" + upath_ + "')"
		
		
		X = []
		Y = []
		x = np.loadtxt(spath_)

		
		xlen = int(len(x) - 2)			
		tp = x[0]
		dt = (x[1] / xlen)
		
		x = x[2:]
		Ex = 0

		it = 0
		t =tp
		
		for i in x:
			if id == 17159 or id == 17161 or id == 17162 or id == 17163 or id == 17164 or id == 17165 or id == 18137 or id == 18127 or id == 18129 or id == 18131 or id == 18133 or id == 18135 or id == 18100 or id ==18102 or id == 18104 or id == 18106 or id == 18108 or id == 18110 or id == 18112 or id == 18114 or id == 18116 or id == 18118 or id == 18120 or id == 18122:
				if t > 4 and t < 200:
					
					Ex += pow(x[it],2)
				
			elif id == 17160 or id == 17166 or id == 17167 or id == 17168 or id == 17169 or id == 17170 or id == 18138 or id == 18128 or id == 18130 or id == 18132 or id == 18134 or id == 18136 or id == 18101 or id == 18103 or id == 18105 or id == 18107 or id == 18109 or id == 18111 or id == 18113 or id == 18115 or id == 18117 or id == 18119 or id == 18121 or id == 18123:
				if t > 4 and t < 1000:
					Ex += pow(x[it],2)
			else:
				Ex += pow(round(x[it],2),2)
			it += 1
			t += dt

		Ex = round(sqrt(Ex),3)

		if Ex != 0 and Ex != 1:
			cur = conn.cursor()
			querry = "INSERT INTO measurements_low (parent, id, point, type, unit, date, value, raport_number) VALUES (" + str(parent) + "," + str(id) + ",'" + str(point) + "','" + str(typel) + "','" + str(unit) + "','" + str(date) + "'," + str(Ex) + ",'" + str(report_number) + "');"
			cur.execute(querry)
			conn.commit()
		
		cur = conn.cursor()
		querry = "INSERT INTO measurements (parent, id, point, report_number, date, domain, type, chart) VALUES (" + str(parent) + "," + str(id) + ",'" + str(point) + "','" + str(report_number) + "','" + str(date) + "','" + str(domain) + "','" + str(type) + "'," + str(chart) + ");"
		cur.execute(querry)
		conn.commit()
		
		
		os.remove(spath_)
		
		
