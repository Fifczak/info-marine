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
username = 'testuser'
password = 'info'
host = 'localhost'
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



###jakies stare nieznormalizowane formatki

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
def putbearings():


	class point():
		def __init__(self):
			self.id = ''
			self.point = ''
			self.bearing = ''
			self.seal = ''
			self.add = ''

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
				dframe = point()
				dframe.id = worksheet.cell(x, 1).value
				dframe.point = worksheet.cell(x, 3).value
				dframe.bearing = worksheet.cell(x, 4).value
				dframe.seal = worksheet.cell(x,5).value
				dframe.add = worksheet.cell(x, 6).value
				if str(dframe.point).strip() != '' and str(dframe.bearing).strip() != '':
					dframelist.append(dframe)
					break
	for item in tqdm(dframelist):
		try:
			item.bearing = int(item.bearing)
		except:
			item.bearing = str(item.bearing)
		#querry = "update bearings set bearing = '{}', seal = '{}', additional = '{}' where id = {} and point = '{}'".format((item.bearing),item.seal,item.add,int(item.id),item.point)
		querry = "INSERT INTO BEARINGS (id,point,bearing,seal,additional,greasing) values ({},'{}','{}','{}','{}','True')".format(int(item.id),item.point,item.bearing,item.seal,item.add)

		try:
			q_run(connD,querry)
		except:
			('SOMEERROR')
def putdrivenby():


	class dev():
		def __init__(self):
			self.id = ''
			self.drivenby = ''

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
			dframe = dev()
			dframe.id = worksheet.cell(x, 3).value
			dframe.drivenby = worksheet.cell(x, 4).value
			dframelist.append(dframe)
			break
	for item in tqdm(dframelist):

		querry = "update devices set drivenby = {} where id = {} ".format(int(item.drivenby),int(item.id))
		#print(querry)
		q_run(connD,querry)
def puttypesKW():


	class dev():
		def __init__(self):
			self.id = ''
			self.type = ''
			self.kW = ''


	Tk().withdraw()
	file = filedialog.askopenfilename()
	workbook = xlrd.open_workbook(file)
	worksheet = workbook.sheet_by_index(0)
	xsize = worksheet.ncols
	ysize = worksheet.nrows


	dframelist = list()
	x = -1
	for row in range(ysize-2):
		x += 1
		y = 0
		for row in range(xsize-1):
			y += 1
			dframe = dev()
			dframe.id = worksheet.cell(x, 0).value
			dframe.type = worksheet.cell(x, 2).value
			dframe.kW = worksheet.cell(x, 3).value
			dframelist.append(dframe)
			break
	for item in (dframelist):

		querry = "update devices set type = '{}', kw = '{}' where id = {} ".format(item.type,item.kW,int(item.id))
		print(querry)
		q_run(connD,querry)


### NIBY JUZ NA DOCELOWE FORMATKI

def update_bearings_via_point():


	class point():
		def __init__(self):
			self.id = ''
			self.point = ''
			self.bearing = ''
			self.seal = ''
			self.add = ''
			self.visible = ''

	Tk().withdraw()
	file = filedialog.askopenfilename()
	workbook = xlrd.open_workbook(file)
	worksheet = workbook.sheet_by_index(0)
	xsize = worksheet.ncols
	ysize = worksheet.nrows


	dframelist = list()
	x = 0
	for row in range(ysize-1):
		x += 1
		y = 0
		for col in range(xsize-1):
			y += 1
			if ((worksheet.cell(x, 1).value)) != '':
				dframe = point()
				dframe.id = worksheet.cell(x, 0).value
				dframe.point = worksheet.cell(x, 3).value
				dframe.bearing = worksheet.cell(x, 4).value
				dframe.seal = worksheet.cell(x,5).value
				dframe.add = worksheet.cell(x, 6).value
				dframe.visible = worksheet.cell(x, 7).value

				if str(dframe.point).strip() != '':
					dframelist.append(dframe)
					break
	for item in tqdm(dframelist):
		try:
			item.bearing = int(item.bearing)
		except:
			item.bearing = str(item.bearing)

		querry = "SELECT * FROM BEARINGS WHERE ID = {} AND POINT = '{}'".format(int(item.id),item.point)
		if len(q_run(connD,querry)) == 0:
			querry = "INSERT INTO BEARINGS (id,point,bearing,seal,additional) values ({},'{}','{}','{}','{}')".format(int(item.id),item.point,item.bearing,item.seal,item.add )
		else:
			querry = "update bearings set bearing = '{}', seal = '{}', additional = '{}' where id = {} and point = '{}'".format((item.bearing),item.seal,item.add,int(item.id),item.point)

		try:

			q_run(connD,querry)
		except:
			('Bearings update/insert errot')

		querry = "UPDATE points set visible = '{}' where id = {} and point = '{}'".format(item.visible,int(item.id),item.point)
		try:
			#print(querry)
			q_run(connD, querry)
		except:
			('Point visible errot')
def updatedevicesdata():
	class Device(object):
		def __init__(self):
			self.id = ''
			self.name = ''
			self.PMS = ''
			self.drivenby = ''
			self.kW = ''
			self.RPM = ''
			self.type = ''
			self.standardfkey = ''
			self.interval = ''
			self.cm = ''
			self.model = ''

	Tk().withdraw()
	file = filedialog.askopenfilename()
	workbook = xlrd.open_workbook(file)
	worksheet = workbook.sheet_by_index(0)
	xsize = worksheet.ncols
	ysize = worksheet.nrows


	dframelist = list()
	x = 0
	for row in range(ysize-1):
		x += 1
		y = 0
		for row in range(xsize-1):
			y += 1
			if ((worksheet.cell(x, 1).value)) != '':
				dframe = Device()
				dframe.PMS = worksheet.cell(x, 0).value
				if str(dframe.PMS) == 'None': dframe.PMS = '-'
				dframe.id = int(worksheet.cell(x, 1).value)
				dframe.name = (worksheet.cell(x, 2).value)
				try:
					dframe.drivenby = int(worksheet.cell(x,3).value)
				except:
					dframe.drivenby = 0
				try:
					dframe.kW = float(worksheet.cell(x, 4).value)
				except:
					dframe.kW = '0'
				try:
					dframe.RPM = int(worksheet.cell(x, 5).value)
				except:
					dframe.RPM = 0
				dframe.type = worksheet.cell(x, 6).value
				dframe.standardfkey =int( worksheet.cell(x, 7).value)
				dframe.info = worksheet.cell(x, 16).value
				dframe.interval = worksheet.cell(x, 11).value
				dframe.cm = worksheet.cell(x, 12).value

				dframe.model = worksheet.cell(x, 14).value

				if str(dframe.cm) == 'true': dframe.cm = 'True'
				if str(dframe.cm) == 'false': dframe.cm = 'False'
				dframelist.append(dframe)



				break
	for item in tqdm(dframelist):
		if str(item.RPM) == '0': item.RPM = ''
		querry = "update devices set name = '{}', pms = '{}',drivenby = {},kw = {},rpm = '{}',type = '{}',standard_fkey='{}',norm=(select standard from standards where id = {}),info='{}',cbm_interval = '{}',cm = {} where id = {}".format(\
			item.name,item.PMS,item.drivenby,item.kW,item.RPM,item.type,item.standardfkey,item.standardfkey,item.info,item.interval, item.cm,item.id)
		print(querry)
		q_run(connD, querry)

		if str(item.model).strip() != '':
			querry = "update devices set model = '{}', model_fkey = (select id from main_models where name = '{}' limit 1) where id = {}".format(\
				item.model,item.model,item.id)
			print(querry)
			q_run(connD,querry)
def LoadMakersModels():
	class MMFrame(object):
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
	x = 0
	for row in range(ysize-1):
		x += 1
		y = 0
		for row in range(xsize-1):
			y += 1
			if ((worksheet.cell(x, 1).value)) != '':
				if ((worksheet.cell(x, 13).value)) != '' and ((worksheet.cell(x, 14).value)) != '':
					dframe = MMFrame()
					dframe.maker = worksheet.cell(x, 13).value
					dframe.model = worksheet.cell(x, 14).value
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
def crosstablebyid():
	class Device(object):
		def __init__(self):
			self.id = ''
			self.nameindevice = ''


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

				dframe = Device()
				dframe.id = int(worksheet.cell(x, 0).value)
				dframe.nameindevice = (worksheet.cell(x, 1).value)
				dframelist.append(dframe)
				break
	for item in tqdm(dframelist):
		querry = "select id from crosstable where id = {}".format(item.id)
		if len(q_run(connD, querry)) == 0:
			querry = "INSERT into crosstable(parent,nameindevice,id) VALUES ((select parent from devices where id = {} limit 1),'{}',{})".format(\
				item.id,item.nameindevice,item.id)
		else:
			querry = "update crosstable set nameindevice = '{}' where id = {}".format(\
				item.nameindevice,item.id)
		#print(querry)
		q_run(connD, querry)

def mccard():
	class Device(object):
		def __init__(self):
			self.id = ''
			self.rhs = ''
			self.rpm = ''



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
				try:
					dframe = Device()
					dframe.id = int(worksheet.cell(x, 0).value)
					dframe.rhs = (worksheet.cell(x, 1).value)
					if str(dframe.rhs).strip() == '': dframe.rhs = '-'
					dframe.rpm = (worksheet.cell(x, 2).value)
					if str(dframe.rpm).strip() == '': dframe.rpm = '-'
					dframelist.append(dframe)
					break
				except:
					#print('No int in col A')
					break
	for item in tqdm(dframelist):
		querry = "INSERT INTO mcdata (id, raport_number, mcremark, documentdate) values ({},'2166-2019','{}','2019-08-30')".format(item.id,"RHs: {}{}RPM: {}".format(item.rhs,chr(10),item.rpm))
		q_run(connD,querry)


while 0 == 0:
	t = input(
		"[1]Update bearings via point" + chr(10) + "[2]Load Makers/Models" + chr(10) + "[3]Update devices data" + chr(
			10) + "[4]Update crosstable nameindevice by id" + chr(10))
	if str(t) == '1':
		update_bearings_via_point()
	if str(t) == '2':
		LoadMakersModels()
	if str(t) == '3':
		updatedevicesdata()
	if str(t) == '4':
		crosstablebyid()
	if str(t) == '5':
		mccard()
