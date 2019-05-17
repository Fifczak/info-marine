import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import psycopg2
from tkinter import messagebox
import csv
import array as arr
import os



def createchart(host, username, password, id, rn):
	connD = [username, password, host]
	def q_run(connD, querry):
		username = connD[0]
		password = connD[1]
		host = connD[2]
		kport = "5432"
		kdb = "postgres"
		# cs = ' host="localhost",database="postgres", user= "postgres" , password="info" '
		cs = "dbname=%s user=%s password=%s host=%s port=%s" % (kdb, username, password, host, kport)
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
	querry = "select chart from meascharts where id = '" + str(id) + "' and report_number = '" + str(
		rn) + "' and point = 'H1' and domain = 'FFT' and type = 'Env' ;"
	chartstr = q_run(connD, querry)[0][0]
	chartstrlist = chartstr.split(";")


	x = []
	Y = []
	for line in chartstrlist:
		x.append(float(line))
	tp = x[0]
	xlen = int(len(x) - 2)
	dt = (float(x[1]) / xlen)
	print(x[0])
	print(x[1])
	print(dt)


	x = x[2:]

	
	it = 0
	t =tp
	maxf = 800
	# if id == 17159 or id == 17161 or id == 17162 or id == 17163 or id == 17164 or id == 17165:
	# 	maxf= 200
	# if id == 17160 or id == 17166 or id == 17167 or id == 17168 or id == 17169 or id == 17170:
	# 	maxf= 1000


	for i in x:
		if t < 4 :
			x[it] = 0
		if t > maxf :
			x[it] = 0
		it += 1
		#print(t)
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
	print('MaxVal: ' + str(maxval))
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
	

	
createchart('192.168.10.243', 'testuser', 'info', 18116, '2009-2019')