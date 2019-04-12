from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import psycopg2
import csv


import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg



host = '192.168.8.125'
username = 'gosiam'
password = 'infog'
connD = [username,password,host]

def draw_figure(canvas, figure, loc=(0, 0)):
		""" Draw a matplotlib figure onto a Tk canvas

		loc: location of top-left corner of figure on canvas in pixels.
		Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
		"""
		figure_canvas_agg = FigureCanvasAgg(figure)
		figure_canvas_agg.draw()
		figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
		figure_w, figure_h = int(figure_w), int(figure_h)
		photo = tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)

		# Position: convert from top-left anchor to center anchor
		canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)

		# Unfortunately, there's no accessor for the pointer to the native renderer
		tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

		# Return a handle which contains a reference to the photo object
		# which must be kept live or else the picture disappears
		return photo


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



class analyzer_frame:
	def generatechart(self):
		
		def chart():
			#### WYKRES
			DPFilter = 10
			badIters = DPFilter / self.CHiter
			self.X=[]
			for val in self.Xvals:
				self.X.append(float(val))
			self.Y = []
			ic = 0
			for val in self.Yvals:
				if ic <= badIters:
					self.Y.append(0)
				else:
					self.Y.append(float(val))
				ic +=1
			self.ax.plot(self.X, self.Y,linewidth = 0.3)
		def maxcursor():
			### MAX
			maxf = max(self.X)
			maxval = max(self.Y)
			maxcord = (self.Y.index(max(self.Y)) * self.CHiter)
			self.ax.plot([0, 800], [maxval, maxval], lw=0.3, color = 'red')
			self.ax.plot([maxcord, maxcord], [maxval, maxval * 1.1], lw=0.3)
		
		def onpick(event):
			thisline = event.artist
			xdata = thisline.get_xdata()
			ydata = thisline.get_ydata()
			print('onpick points:', xdata, ydata)

		w, h = 900, 700
		self.canvas = tk.Canvas(self.chartFrame, width=w, height=h)
		self.fig = plt.figure(figsize=(8, 6))
		
		
		
		
		#self.fig.set_canvas(self.canvas)
	
		
		self.ax = self.fig.add_subplot(111)
		self.ax.set_title('FFT Velocity')
		# JAKO SAMPEL # line, = ax.plot(xs, ys, 'o', picker=5)  # 5 points tolerance
		# self.ax = self.fig.add_axes([0, 0, 1, 1])
		#
		#self.fig.canvas.mpl_connect('pick_event', onpick)	
		

		if self.layers[0] == True:
			chart()
		# if self.layers[1] == True:
			# maxcursor()
		
		
		## CHYBA GENEROWANIE OGOLNIE
		self.fig_x, self.fig_y = 0, 0
		self.fig_photo = draw_figure(self.canvas,self.fig, loc=(self.fig_x, self.fig_y))
		self.fig_photo.width()
		self.fig_w, self.fig_h = self.fig_photo.width(), self.fig_photo.height()
		
		self.canvas.pack()

	def __init__(self,source,iid,irn,ipoint,itype):
		def layersVis():
			if self.layers[1] == True:
				self.layers[1] = False
			elif self.layers[1] == False:
				self.layers[1] = True
			self.canvas.destroy()			
			self.generatechart()
		if str(source) == 'database_inDS':
			self.rootAnalyzer = tk.Tk()
			self.rootAnalyzer.title("Analyzer")
			self.header = tk.Canvas(self.rootAnalyzer)
			self.id = iid
			self.rn = irn
			self.point = ipoint
			self.type = itype
			Lrn = tk.Label(self.header, text = str(self.rn) ).pack(side = TOP, anchor = W)
			querry = "select name from devices where id = " + str(self.id)
			Lname = tk.Label(self.header, text = q_run(connD, querry)[0][0] ).pack(side = TOP, anchor = W)
			self.Lpt = tk.Label(self.header, text = str(self.point) ).pack(side = TOP, anchor = W)
			self.Ltype = tk.Label(self.header, text = str(self.type) ).pack(side = TOP, anchor = W)
			chquerry = "select chart from meascharts where id = " +str(self.id)+ " and report_number = '"+str(self.rn)+"' and point = '"+str(self.point)+ "' and domain = 'FFT' and type = '"+str(self.type)+ "' limit 1" 
			self.header.pack()
			print(chquerry)
			chartstr = q_run(connD, chquerry)[0][0]
			chartlisttemp = chartstr.split(";")
			self.CHiter = float(chartlisttemp[0])
			self.CHend = float(chartlisttemp[1])
			self.Yvals = chartlisttemp[2:]
			self.Xvals = list()
			self.CHres = len(self.Yvals)
			self.CHstart = (float(self.CHend) / float(self.CHres))
			xval = self.CHstart
			for v in self.Yvals:
				self.Xvals.append(xval)
				xval += self.CHiter
			
			self.chartFrame = tk.Frame(self.rootAnalyzer)
			self.button1 = tk.Button(self.chartFrame,text = 'Show Max',command = layersVis).pack(anchor = NW)
			
			self.layers = [True,True] #chart, maxcursor
			self.generatechart()
			self.chartFrame.pack()
		self.rootAnalyzer.mainloop()

	
		pass
		
