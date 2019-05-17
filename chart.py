import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import psycopg2
from tkinter import messagebox
import csv
import array as arr
import os

def createchart(host, username, password, id, rn):

	kport = "5432"
	kdb = "postgres"



	#cs = ' host="localhost",database="postgres", user= "postgres" , password="info" '
	cs = "dbname=%s user=%s password=%s host=%s port=%s"%(kdb,username,password,host,kport)
	conn = None
	conn = psycopg2.connect(str(cs))
	cur = conn.cursor()
	querry = "select point from measurements_low where id = " + str(id) + " and raport_number = '" + str(rn) + "' order by value desc limit 1;"
	cur.execute(querry)
	result = cur.fetchall()
	conn.commit()
	cur.close()	
	
	
	if host == 'localhost':
		querry = "select lo_export(measurements.chart, 'C:\\Overmind\\temp\\tempchart.csv') from measurements where id = " + str(id) + " and report_number = '" + str(rn) + "';"	
	if host == '192.168.8.125':
		servpath = r'/home/filip/Public/tempchart.csv'
		querry = "select lo_export(measurements.chart,'" + servpath + "') from measurements where id = '" + str(id) + "' and report_number = '" + str(rn) + "' and point = '"+ str(result[0][0]) +"';"	
		

	
	cur = conn.cursor()
	cur.execute(querry)
	result = cur.fetchall()
	conn.commit()
	cur.close()
	#os.remove(spath_)
	X = []
	Y = []
	if host == 'localhost':
		x = np.loadtxt(r'C:\\Overmind\\temp\\tempchart.csv')
	if host == '192.168.8.125':
		servpath = r'\\192.168.8.125\Public\tempchart.csv'
		x = np.loadtxt(servpath)
	tp = x[0]
	dt = x[1]
	x = x[2:]
	
	
	
	it = 0
	t =tp
	maxf = 0 
	if id == 17159 or id == 17161 or id == 17162 or id == 17163 or id == 17164 or id == 17165:
		maxf= 200
	if id == 17160 or id == 17166 or id == 17167 or id == 17168 or id == 17169 or id == 17170:
		maxf= 1000
	
	for i in x:
		if t < 4 :
			x[it] = 0
		if t > maxf :
			x[it] = 0
		it += 1
		t += dt
		Y.append(t)
	fig = plt.figure(figsize=(15, 6), dpi=80)
	plt.plot(Y,x,linewidth = 0.3)
	plt.xlabel('Frequency [Hz]')
	plt.ylabel('Velocity[mm/s]')
	#messagebox.showinfo("Title", maxf)
	#plt.title("THruster")
	axes = plt.gca()
	
	maxval = np.amax(x)
	maxcord = (np.argmax(x) + 1) * dt
	plt.plot([0, 1000], [maxval, maxval], lw=0.3, color = 'red')
	plt.plot([maxcord, maxcord], [maxval, maxval * 1.1], lw=0.3)
	axes.set_xlim([0,maxf])
	axes.set_ylim([0,maxval * 1.1])
	plt.savefig('C:\\overmind\\temp\\tempchart.png', dpi = 900, width = 1000)
	plt.show()
	
	# p = document.add_paragraph()
	# r = p.add_run()
	# r.add_picture('C:\\overmind\\Data\\Atlantis_thruster.jpg')
	# p.alignment = WD_ALIGN_PARAGRAPH.CENTER
	
	if host == 'localhost':
		os.remove('C:\\Overmind\\temp\\tempchart.csv')
	if host == '192.168.8.125':
		servpath = r'\\192.168.8.125\Public\tempchart.csv'
		os.remove(servpath)

	
createchart('192.168.8.125', 'filipb', '@infomarine', 17160, 'TEST-PYT')