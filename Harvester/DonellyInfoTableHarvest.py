import datetime
import xlrd
from tqdm import tqdm
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter import Tk
from tkinter import filedialog
import psycopg2
import re
username = 'filipb'
password = '@infomarine'
host = '192.168.10.243'
connD = [username,password,host]

def column(matrix, i):
    return [row[i] for row in matrix]

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

def getDOnellydata():
	class DataFrame(object):
		def __init__(self):
			self.id = ''
			self.PMS = ''
			self.kW = ''
			self.RPM = ''
			self.info = ''
			self.model = ''

	Tk().withdraw()
	file = filedialog.askopenfilename()
	workbook = xlrd.open_workbook(file)
	worksheet = workbook.sheet_by_index(0)
	xsize = worksheet.ncols
	ysize = worksheet.nrows


	dframelist = list()
	x = 1
	for row in range(ysize-2):
		x += 1



		y = 0
		for row in range(xsize-1):
			y += 1
			if ((worksheet.cell(x, 1).value)) != '':
				dframe = DataFrame()
				dframe.id = worksheet.cell(x, 2).value
				dframe.PMS = worksheet.cell(x, 3).value
				dframe.kW = worksheet.cell(x, 5).value
				dframe.RPM = worksheet.cell(x, 6).value
				#dframe.info = worksheet.cell(x, 6).value
				dframe.model = worksheet.cell(x, 12).value
				dframelist.append(dframe)
				break
	for item in tqdm(dframelist):
		try:
			querry = "update devices set PMS = '" + str(item.PMS) + "' where id = '" + str(int(item.id)) + "'"
			q_run(connD,querry)
		except:
			pass
		try:
			querry = "update devices set model = '" + str(item.model) + "' where id = '" + str(int(item.id)) + "'"
			q_run(connD,querry)
		except:
			pass
		try:
			querry = "update devices set kw = '" + str(item.kW) + "' where id = '" + str(int(item.id)) + "'"
			q_run(connD,querry)
		except:
			pass

		try:
			querry = "update devices set rpm = '" + str(item.RPM) + "' where id = '" + str(int(item.id)) + "'"
			q_run(connD,querry)
		except:
			pass


		#print(querry)
		# if str(item.info).strip() != '':
		# 	querry = "select info from devices where id = '" + str(int(item.id)) + "'"
		# 	print(querry)
		# 	# try:info = list(q_run(connD,querry))[0][0]
		# 	# except:info = ''
		# 	if str(info).strip() != '':infostr = str(info) + chr(10) + str(item.info).strip()
		# 	else:infostr = str(item.info).strip()
		# 	querry = "update devices set info = '" + str(infostr) +  "' where id = '" + str(int(item.id)) + "'"
		# 	# q_run(connD,querry)
		# 	print(querry)



def getMakersModels():
	class DataFrame(object):
		def __init__(self):
			self.maker = ''
			self.model = ''

	Tk().withdraw()
	file = filedialog.askopenfilename()
	workbook = xlrd.open_workbook(file)
	worksheet = workbook.sheet_by_index(0)
	xsize = worksheet.ncols
	ysize = worksheet.nrows
	dframelist = list()
	x = 1
	for row in range(ysize-2):
		x += 1
		y = 0
		for row in range(xsize-1):
			y += 1
			if ((worksheet.cell(x, 1).value)) != '':
				if ((worksheet.cell(x, 7).value)) != '-' and ((worksheet.cell(x, 8).value)) != '-':
					dframe = DataFrame()
					dframe.maker = worksheet.cell(x, 11).value
					dframe.model = worksheet.cell(x, 12).value
					if dframe not in dframelist: dframelist.append(dframe)
					break
	modellist = list()
	makerslist = list()
	modellistcheck = list()
	for item in dframelist:
		if item.maker not in makerslist:
			makerslist.append(item.maker)
		if item.model not in modellistcheck:
			modellistcheck.append(item.model)
			modellist.append([item.model,item.maker])

	querry = "select name from main_models where parent is null"
	DBmakers = list(q_run(connD,querry))

	for item in tqdm(makerslist):
		if item not in column(DBmakers,0):
			querry = "insert into main_models (parent,name) VALUES (null,'" + str(item) + "')"
			q_run(connD,querry)
		else:
			print('Maker exist')

	querry = "select name from main_models where parent is not null"
	DBmodels = list(q_run(connD,querry))

	for item in tqdm(modellist):
		if item[0] not in column(DBmodels,0):
			try:
				querry = "insert into main_models (parent,name) VALUES ((select id from main_models where name ='" + str(item[1]) + "'),'" + str(item[0]) + "')"

				q_run(connD,querry)
			except:
				print('Empty model ? Something wrong')
		else:
			print('Model exist')



def putintervals():

	class device():
		def __init__(self):
			self.id = ''
			self.interval = ''

	Tk().withdraw()
	file = filedialog.askopenfilename()
	workbook = xlrd.open_workbook(file)
	worksheet = workbook.sheet_by_index(0)
	xsize = worksheet.ncols
	ysize = worksheet.nrows


	dframelist = list()
	x = 0
	for row in range(ysize-2):
		x += 1
		y = 0
		for row in range(xsize-1):
			y += 1
			if ((worksheet.cell(x, 1).value)) != '':
				dframe = device()
				dframe.id = worksheet.cell(x, 2).value
				dframe.interval = worksheet.cell(x,13).value
				dframelist.append(dframe)
				break

	for item in dframelist:
		if item.interval != '':
			if item.interval == '3 month' or item.interval == '3 Month': item.interval = '3 months'
			querry = "update devices set cbm_interval = '{}' where id = {}".format(item.interval, int(item.id))
			q_run(connD,querry)
			if item.interval == '1 month' or item.interval == '1 Month':
				querry = "update devices set CM = 'True' where id = {}".format(int(item.id))
				q_run(connD,querry)
		else:
			querry = "update devices set cbm_interval = '2 years' where id = {}".format(int(item.id))
			q_run(connD,querry)
putintervals()