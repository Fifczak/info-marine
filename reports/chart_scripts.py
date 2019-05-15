import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import psycopg2
import datetime as dt

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg

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


def trendchart():

    querry = "select raport_number,max(value),max(date) from measurements_low where id = 5008 and type = 'RMS' group by raport_number order by raport_number desc"
    raports = q_run(connD, querry)
    dates = list()
    vals = list()
    for line in raports:

        dates.append(line[2].strftime('%m/%d/%Y'))
        vals.append(line[1])

    print(list(vals))
    print(list(dates))
    x = [dt.datetime.strptime(d, '%m/%d/%Y').date() for d in dates]
    y = vals

    chartwindow = tk.Tk()
    chartwindow.title("Trend Chart")
    chartcanvas = tk.Canvas(chartwindow,width=800, height=300)


    plt.plot(x, y)
    plt.gcf().autofmt_xdate()

    plt.savefig('trendchart.png', dpi=60, width=1000)
    gif1 = PhotoImage(file='trendchart.png')
    chartcanvas.create_image(50, 10, image=gif1, anchor=NW)


    chartcanvas.pack()






#control room
    controlframe = tk.Frame(chartwindow)
    Label(controlframe, text='CONTROL').pack()
    controlframe.pack()



    chartwindow.mainloop()


trendchart()

