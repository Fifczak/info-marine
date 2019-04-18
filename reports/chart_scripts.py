import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import psycopg2


import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg

username = 'testuser'
password = 'info'
host = 'localhost'
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

def trendchart():

    chartwindow = tk.Tk()
    chartwindow.title("Trend Chart")
    chartcanvas = tk.Canvas(chartwindow,width=800, height=300)

    fig = plt.figure(figsize=(12, 4))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot([1, 3, 2, 4, 1,1, 6 , 3 , 2])
    ax.set_ylabel('some numbers')
    plt.savefig('trendchart.png', dpi=60, width=100)
    gif1 = PhotoImage(file='trendchart.png')
    chartcanvas.create_image(50, 10, image=gif1, anchor=NW)


    chartcanvas.pack()






#control room
    controlframe = tk.Frame(chartwindow)
    Label(controlframe, text='CONTROL').pack()
    controlframe.pack()
    querry = "select raport_number from measurements_low where id = 5008 group by raport_number order by raport_number desc"
    raports = q_run(connD,querry)
    for line in raports:
        print(line)


    chartwindow.mainloop()


trendchart()

