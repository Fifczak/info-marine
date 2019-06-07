import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import psycopg2
import datetime as dt

import numpy as np
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
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


class trendchart:
    def __init__(self):
        self.chartwindow = tk.Tk()
        self.chartwindow.title("Trend Chart")
        self.chartcanvas = tk.Canvas(self.chartwindow, width=800, height=300)
        self.controlframe = tk.Frame(self.chartwindow)
        Vals = self.trendresults()
        self.drawplot(Vals[0],Vals[1])
        self.chartwindow.mainloop()
    def trendresults(self):
        def gettrendresults():
            querry = "select raport_number,max(value),max(date) from measurements_low where id = 5008 and type = 'RMS' group by raport_number order by raport_number desc"
            return q_run(connD, querry)
        dates = list()
        vals = list()
        raps = list()
        for line in gettrendresults():
            dates.append(line[2].strftime('%m/%d/%Y'))
            vals.append(line[1])
            raps.append(line[0])
        x = [dt.datetime.strptime(d, '%m/%d/%Y').date() for d in dates]
        y = vals
        z = raps
        ans = [x,y,z]
        return ans
    def drawplot(self,x,y):
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.savefig('trendchart.png', dpi=60, width=1000)
        gif1 = PhotoImage(file='trendchart.png')

        self.chartcanvas.create_image(50, 10, image=gif1, anchor=NW)

        self.chartcanvas.pack()

    def trendlabels(self):
        for item in raports:
            Dlabel = tk.Label(self.controlframe, text=str(item[2].strftime('%m/%d/%Y'))).pack()
            Dlabel = tk.Label(self.controlframe, text=str(item[1])).pack()
        self.controlframe.pack()

        print('xxx')


class trendchart2:


    def __init__(self,wdw):

        def trendresults():
            def gettrendresults():
                querry = "select raport_number,max(value),max(date) from measurements_low where id = 5008 and type = 'RMS' group by raport_number order by raport_number desc"
                return q_run(connD, querry)

            dates = list()
            vals = list()
            reps = list()
            for line in gettrendresults():
                dates.append(line[2].strftime('%m/%d/%Y'))
                vals.append(line[1])
                reps.append(line[0])
            x = [dt.datetime.strptime(d, '%m/%d/%Y').date() for d in dates]
            y = vals
            z = reps
            ans = [x, y, z]
            return ans

        def draw(x,y):
            f = Figure(figsize=(10, 5), dpi=100)
            a = f.add_subplot(111)
            a.plot(x, y)
            f.autofmt_xdate()
            canvas = FigureCanvasTkAgg(f, wdw)

            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

            toolbar = NavigationToolbar2Tk(canvas, wdw)
            toolbar.update()
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        def details(VALS):
            VALS = list(map(list, zip(*VALS)))
            LL = (len(VALS))
            detailFrame = tk.Frame(wdw)
            detailFrame.pack()
            coll = -1
            for line in VALS:
                coll += 1
                datelabel = tk.Label(detailFrame, text=str(line[0]))
                replabel = tk.Label(detailFrame, text=str(line[2]))
                vallabel = tk.Label(detailFrame, text=str(line[1]))


                datelabel.grid(column = LL - coll, row = 0,pady=5, padx=5)
                replabel.grid(column = LL - coll, row = 1,pady=5, padx=5)
                vallabel.grid(column = LL - coll, row = 2,pady=5, padx=5)
            button1 = ttk.Button(wdw, text="Back to Home",
                                 command=lambda: controller.show_frame(StartPage))
            button1.pack()


        VALS = trendresults()
        draw(VALS[0],VALS[1])
        details(VALS)








chartwindow = tk.Tk()
chartwindow.title("Trend Chart")
trendchart2(chartwindow)
chartwindow.mainloop()


# class PageThree(tk.Frame):
#
# 	def __init__(self, parent, controller):
# 		tk.Frame.__init__(self, parent)
# 		label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
# 		label.pack(pady=10, padx=10)
#
# 		button1 = ttk.Button(self, text="Back to Home",
# 							 command=lambda: controller.show_frame(StartPage))
# 		button1.pack()
#
# 		f = Figure(figsize=(5, 5), dpi=100)
# 		a = f.add_subplot(111)
# 		a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])
#
# 		canvas = FigureCanvasTkAgg(f, self)
# 		canvas.draw()
# 		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
#
# 		toolbar = NavigationToolbar2Tk(canvas, self)
# 		toolbar.update()
# 		canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

