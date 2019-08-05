import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
import psycopg2
import datetime as dt
import numpy as np
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_agg import FigureCanvasAgg
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import io

# username = 'testuser'
# password = 'info'
# host = 'localhost'
# connD = [username,password,host]
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
    def __init__(self,ids,connD,GUI,VSG):
        def trendresults(devid):
            def gettrendresults():
                if VSG == False:
                    querry ="select ml.raport_number,max(ml.value),max(ml.date),dev.name from measurements_low as ml"\
                            " left join devices as dev on ml.id = dev.id" \
                            " left join points pts on ml.id = pts.id and ml.point = pts.point"\
                            " where ml.id =" + str(devid) + " and ml.type = 'RMS' and ml.value != -1 and ml.date > now() - interval '2 years' and pts.visible = true group by ml.raport_number,dev.name order by max(ml.date) desc"
                else:
                    querry = "select ml.raport_number,max(ml.value),max(ml.date),dev.name from measurements_low as ml" \
                             " left join devices as dev on ml.id = dev.id" \
                             " left join points pts on ml.id = pts.id and ml.point = pts.point" \
                             " where ml.id =" + str(
                        devid) + " and ml.unit = 'VSG' and ml.value != -1 and  ml.date > now() - interval '2 years' and pts.visible = true group by ml.raport_number,dev.name order by max(ml.date) desc"

                return q_run(connD, querry)
            dates = list()
            vals = list()
            reps = list()
            names = list()
            dates.clear()
            vals.clear()
            reps.clear()
            names.clear()
            for line in gettrendresults():
                dates.append(line[2].strftime('%m/%d/%Y'))
                vals.append(line[1])
                reps.append(line[0])
                names.append(line[3])
            x = [dt.datetime.strptime(d, '%m/%d/%Y').date() for d in dates]
            y = vals
            z = reps
            n = names
            ans = [x, y, z,n]
            return ans
        def draw(x,y,a,name,ylim):
            a.plot(x, y,marker='o', label=str(name[0]))
            a.set_frame_on(False)
            a.yaxis.grid( linewidth='0.5')
            a.legend(loc='lower center',bbox_to_anchor=(0.5,-0.35), fontsize = 'x-large', ncol=3,frameon=False)#

            a.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
            a.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y-%m"))



            if  max(y) > ylim:

                ylim = max(y)*1.2


            a.set_ylim(0,ylim)
            f.autofmt_xdate()
            return f,ylim
        def details(VALS,id_,name):
            VALS = list(map(list, zip(*VALS)))
            LL = (len(VALS))
            detailFrame = tk.Frame(self.wdw, bd=1, relief=SUNKEN)
            nameLabel = tk.Label(detailFrame, text=str(name)).grid(column = 0, row = 0)
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
            button1 = tk.Button(detailFrame, text='Details', command=lambda: calldatasheet(self,id_,name))
            button1.grid(column = LL+1,row=0,rowspan = 3)
        def calldatasheet(parentclass,id_,name):
            datasheet(ids,parentclass,id_,self,name,connD,GUI,VSG)
        self.imgdata = io.BytesIO()
        self.wdw  = tk.Tk()
        self.wdw.title("Trend Chart")

        f = Figure(figsize=(12, 4), dpi=100)

        a = f.add_subplot(1, 1, 1)
        canvas = FigureCanvasTkAgg(f, self.wdw)
        toolbar = NavigationToolbar2Tk(canvas, self.wdw)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        VALS =list()
        ylim = 0
        for i in ids:
            VALS = trendresults(i)
            self.f,ylim = draw(VALS[0],VALS[1],a,VALS[3],ylim)
            querry = "select name from devices where id = " + str(i)
            name = list(q_run(connD,querry))[0][0]
            details(VALS,i,name)

        self.f.savefig(self.imgdata, format='png')
        if GUI == True:
            self.wdw.mainloop()
        if GUI == False:
            self.wdw.withdraw()

    def giveimage(self):
        return(self.imgdata)

class ValRMSwindow():
    def updateRMS(self,_id_,parentclass,grandparentclass,id_,chartframe,connD,ids,GUI):
        querry = "UPDATE measurements_low set value = " + str(self.Val.get("1.0", END)) + " where _id_ = " + str(_id_)
        q_run(connD, querry)
        grandparentclass.quit()
        self.window.destroy()
        querry = "select name from devices where id = " + str(id_)
        name = list(q_run(connD, querry))[0][0]
        datasheet(ids,chartframe,id_,chartframe,name,connD,GUI,self.VSG)
    def __init__(self, connD, parentclass, _id_,grandparentclass,id_,chartframe,ids,GUI,VSG):
        self.VSG = VSG
        self.window = tk.Tk()
        self.window.title("CHANGE RMS")
        self.Val = tk.Text(self.window, height=1, width=12)
        querry = "select value,devices.name, ml.raport_number, ml.point "\
                "from measurements_low as ml left join devices on ml.id = devices.id   where _id_ = " + str(_id_)
        ans = list(q_run(connD, querry))
        value = ans[0][0]
        self.Name = tk.Label(self.window, text = ans[0][1])
        self.RN = tk.Label(self.window, text=ans[0][2])
        self.Point = tk.Label(self.window, text=ans[0][3])
        self.Val.insert(END, ans[0][0])
        self.okbut = tk.Button(self.window, text='UPDATE', command=lambda:self.updateRMS(_id_,self,grandparentclass,id_,chartframe,connD,ids,GUI), width=12)
        self.Name.pack(side=TOP)
        self.RN.pack(side = TOP)
        self.Point.pack(side=TOP)
        self.Val.pack(side=TOP)
        self.okbut.pack(side=TOP)
        self.window.mainloop()
class measBut:
    def changeWindow(self,_id_):
        pass
    def __init__(self,dsFrame,r,c,val,_id_,parentclass,id_,chartframe,connD,ids,GUI,VSG):
        self._id = _id_
        self.lab = tk.Button(dsFrame,text = str(val),command = lambda : ValRMSwindow(connD,self,_id_,parentclass,id_,chartframe,ids,GUI,VSG), width = 15)
        #command = lambda ue=self.user_entry, pe=self.pass_entry: self.logging_in(ue, pe))
        #self.lab.bind("<ButtonRelease-1>",changeWindow(self._id))
        self.lab.grid(row=r, column=c)
class datasheet:
    def quit(self):
        self.DSW.destroy()
    def refresh (self,ids,parentclass,connD,GUI):
        parentclass.wdw.destroy()
        self.quit()
        trendchart(ids,connD,GUI,self.VSG)
        # try:chartwindow.mainloop()
        # except: print('No chartwindow')
    def __init__(self,ids,parentclass,id_,chartframe,name,connD,GUI,VSG):
        self.VSG = VSG
        self.DSW = tk.Tk()
        self.DSW.title("Datasheet")
        if VSG == False:
            querry = """select ml.raport_number,ml.point, ml.value,ml.date,dev.name, ml._id_ from measurements_low as ml
                        left join devices as dev on ml.id = dev.id
                        left join points as pt on ml.id = pt.id and ml.point = pt.point
                        where ml.id = """ +str(id_) +   """ and ml.type = 'RMS' and ml.value != -1 and pt.visible = True and  ml.date > now() - interval '2 years'
                        group by ml.raport_number,ml.point, dev.name,ml.value,ml.date ,pt.sort , ml._id_
                        order by ml.date ,pt.sort  """
        else:
            querry = """select ml.raport_number,ml.point,max(ml.value),ml.date,dev.name, ml._id_,ml.type from measurements_low as ml
                        left join devices as dev on ml.id = dev.id
                        left join points as pt on ml.id = pt.id and ml.point = pt.point
                        where ml.id = {} and ml.unit = 'VSG' and ml.value != -1 and pt.visible = True and  ml.date > now() - interval '2 years'
                        group by ml.raport_number,ml.point, dev.name,ml.date ,pt.sort , ml._id_,ml.type
                        order by ml.date ,pt.sort  """.format(str(id_))
        dsd = q_run(connD,querry)
        RapList = list()
        PointList = list()
        for line in dsd:
            if line[0] not in RapList:
                RapList.append(line[0])
            if line[1] not in PointList:
                PointList.append(line[1])
        namelabel = tk.Label(self.DSW, text=str(name)).pack()
        dsFrame = tk.Frame(self.DSW)
        c =0
        for line in RapList:
            c+=1
            tk.Label(dsFrame, text = line).grid(row = 0, column = c)
            r = 0
            for line2 in PointList:
                r +=1
                tk.Label(dsFrame, text=line2).grid(row=r, column=0)
                for seekVal in dsd:
                    if str(line) == str(seekVal[0]) and str(line2) == str(seekVal[1]):
                        x = measBut(dsFrame,r,c,seekVal[2],seekVal[5],self,id_,chartframe,connD,ids,GUI,self.VSG)
        dsFrame.pack()
        okbutton = tk.Button(self.DSW,text = 'Reload Chart', command = lambda:self.refresh(ids,parentclass,connD,GUI)).pack()
        self.DSW.mainloop()

#trendchart(['19337','19338'], ['testuser','info','192.168.10.243'],True,False)