import psycopg2
import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from tkinter.filedialog import askopenfilename
from tkinter import Tk
import csv
import matplotlib.pyplot as plt
import numpy as num
import tkinter as tkk
from tkinter import filedialog
from tqdm import tqdm
import pandas.io.sql as sqlio
import pandas as pd
import numpy as np


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)

#connD=['testuser','info','localhost']
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
def column(matrix, i):
    return [row[i] for row in matrix]

class LogApplication:
    def __init__(self):
        self.root = Tk()
        self.root.title("Log In")
        self.title = tk.Label(self.root, text="Info Datasheet")  # TITLE
        self.title.grid(row=0, column=2)
        self.user_entry_label = tk.Label(self.root, text="Username: ")  # USERNAME LABEL
        self.user_entry_label.grid(row=1, column=1)
        self.user_entry = tk.Entry(self.root, text="Username: ")  # USERNAME ENTRY BOX
        self.user_entry.grid(row=1, column=2)
        self.pass_entry_label = tk.Label(self.root, text="Password: ")  # PASSWORD LABEL
        self.pass_entry_label.grid(row=2, column=1)
        self.pass_entry = tk.Entry(self.root, show="*")  # PASSWORD ENTRY BOX
        self.pass_entry.grid(row=2, column=2)
        try:
            with open('C:\overmind\\temp\log.csv') as csvfile:
                openfile = csv.reader(csvfile, delimiter=' ')
                p = -1
                for lines in openfile:
                    p += 1
                    if p == 0:
                        self.user_entry.insert(0, str(lines[0]))
                    if p == 1:
                        self.pass_entry.insert(0, str(lines[0]))
        except:
            pass
        self.var = IntVar()
        self.checksave = tk.Checkbutton(self.root, text="Remember", variable=self.var)
        self.checksave.grid(row=3, column=2)
        self.sign_in_butt = Button(self.root, text="Sign In", command=lambda ue=self.user_entry, pe=self.pass_entry: self.logging_in(ue, pe))
        self.sign_in_butt.grid(row=5, column=2)
        self.root.mainloop()

    def logging_in(self,user_entry, pass_entry):
        user_get = user_entry.get()  # Retrieve Username
        pass_get = pass_entry.get()  # Retrieve Password
        if bool(self.var.get()) == True:
           # config = Path('C:\overmind\\temp\log.csv')
            with open('C:\overmind\\temp\log.csv', 'w+' ,newline='') as csvfile:
                filewriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                filewriter.writerow([user_get])
                filewriter.writerow([pass_get])
        connD = [user_get, pass_get, '192.168.10.243']


        querry = "SELECT current_user"
        usercheck = ''

        usercheck = q_run(connD, querry)  # PYINSTALLER ma problemy gdzies tu
        if usercheck != '':
            self.root.destroy()
            feedbackswindow(connD)

class feedbackswindow:
    def __init__(self,connD):
        self.connD = connD
        self. conn = psycopg2.connect(
            "host='{}' port={} dbname='{}' user={} password={}".format(self.connD[2], '5432', 'postgres', self.connD[0], self.connD[1]))
        self.getquerry()
        self.drawwindow()
    def getquerry(self):
        querry = """
        select dev.id,main.name as shipname, dev.name as devname,fdb.raport_number, rem.remark, rem.sended,
        fdb.feedback, fdb.fdbflag, fdb.costflag, fdb.price, fdb.low, fdb.high, dss.sort,
         rem._id_ as remid, fdb._id_ as fdbid,rem.documentdate as remdate,fdb.documentdate as fdbdate
        from feedbacks fdb
        left join remarks rem on fdb.id = rem.id and fdb.raport_number = rem.raport_number
        left join devices dev on fdb.id = dev.id
        left join ds_structure dss on cast(dev.id as text) = dss.id
        left join main on dev.parent = main.id
        order by fdb.raport_number
        """
        self.fdbdFrame = sqlio.read_sql_query(querry, self.conn)
        self.fdbdFrame['fdbflag'] = pd.Series(self.fdbdFrame['fdbflag'], dtype='Int64').fillna(0)
        self.fdbdFrame['costflag'] = pd.Series(self.fdbdFrame['costflag'], dtype='Int64').fillna(0)
        self.presentfeedbacks = self.fdbdFrame

        querry = "select lp,flagstr from fdbflags"
        self.fdbflagz = list()
        self.fdbflagz.append(('0', 'No flag'))
        for item in (list(q_run(self.connD, querry))):
            self.fdbflagz.append(item)

        querry = "select lp,flagstr from costflags"
        self.costflagz = list()
        self.costflagz.append(['0', 'No flag'])
        for item in (list(q_run(self.connD, querry))):
            self.costflagz.append(item)
    def fillfdblist(self, fdbdfr):
        self.feedbacklist.delete(0, 'end')
        #dflisted = fdbdfr.values.tolist()
        for row in fdbdfr.values:
            #print(row)
            ship = row[1]
            devname = row[2]
            raportno = row[3]
            liststring = "SHIP:{} DEVICE:{} REPORT_NUMBER:{}".format(ship,devname,raportno)


            self.feedbacklist.insert(END, liststring)
    def updatedateinlabels(self):
        index = self.feedbacklist.curselection()[0]
        _id_ = self.presentfeedbacks.iloc[index].loc['fdbid']
        rdate = self.fdbdFrame.loc[self.fdbdFrame.fdbid == int(_id_)]['remdate']
        fdate = self.fdbdFrame.loc[self.fdbdFrame.fdbid == int(_id_)]['fdbdate']
        self.remlabel.config(text='Remark {}'.format(np.array(rdate.values, dtype='datetime64[D]')[0]))
        self.fdblabel.config(text='Feedback {}'.format(np.array(fdate.values, dtype='datetime64[D]')[0]))
    def updatecolor(self):

        self.measurementsbeforetab.tag_configure('green', background='green')
        self.measurementsbeforetab.tag_configure('yellow', background='yellow')
        self.measurementsbeforetab.tag_configure('red', background='red')
        self.measurementsbeforetab.tag_configure('grey', background='grey')
        self.measurementsbeforetab.tag_configure('white', background='white')

        self.measurementsaftertab.tag_configure('green', background='green')
        self.measurementsaftertab.tag_configure('yellow', background='yellow')
        self.measurementsaftertab.tag_configure('red', background='red')
        self.measurementsaftertab.tag_configure('grey', background='grey')
        self.measurementsaftertab.tag_configure('white', background='white')

    def updatefdbmeas(self):
        if (int(self.var.get())) == 1:
            self.generatetrendvalues()
        else :
            self.measurementsbeforetab.delete(*self.measurementsbeforetab.get_children())
            self.measurementsaftertab.delete(*self.measurementsaftertab.get_children())
    def generatetrendvalues(self):
        def getmeasquerry():
            index = self.feedbacklist.curselection()[0]
            rn = self.presentfeedbacks.iloc[index].loc['raport_number']
            did = self.presentfeedbacks.iloc[index].loc['id']
            querry = """select mlrms.point, mlrms.raport_number as reportbefore ,round( cast(mlrms.value as numeric),3) as rmsbefore,round( cast(mlpk.value as numeric),3) as pkbefore,
             max(mlrms.date) as datebefore,
            mlrms2.raport_number as reportafter ,round( cast(mlrms2.value as numeric),3) as rmsafter ,round( cast(mlpk2.value as numeric),3) as pkafter, max(mlrms2.date) as dateafter
            from (select * from measurements_low where type = 'RMS') mlrms 
            left join (select * from measurements_low where type = 'envelope P-K') mlpk on mlrms.id = mlpk.id 
                                    and mlrms.raport_number = mlpk.raport_number and mlrms.point = mlpk.point
            left join points pts on mlrms.id =pts.id and mlrms.point = pts.point
            left join (select * from measurements_low where type = 'RMS' and raport_number = (select raport_number 
                                                                                            from measurements_low  
                                                                                            where parent = (select parent 
                                                                                                            from measurements_low 
                                                                                                            where raport_number = '{}'
                                                                                                            group by parent limit 1) 
                                                                                            and date > (select max (date) 
                                                                                                            from measurements_low 
                                                                                                            where raport_number = '{}')
                                                                                            and id = {}
                                                                                            group by raport_number
                                                                                            order by raport_number limit 1) ) mlrms2 on mlrms.point = mlrms2.point  and mlrms.id = mlrms2.id 
            left join (select * from measurements_low where type = 'envelope P-K' and raport_number = (select raport_number 
                                                                                            from measurements_low  
                                                                                            where parent = (select parent 
                                                                                                            from measurements_low 
                                                                                                            where raport_number = '{}'
                                                                                                            group by parent limit 1) 
                                                                                            and date > (select max (date) 
                                                                                                            from measurements_low 
                                                                                                            where raport_number = '{}')
                                                                                            and id = {}
                                                                                            group by raport_number
                                                                                            order by raport_number limit 1) ) mlpk2 on mlrms.point = mlpk2.point  and mlrms.id = mlpk2.id  
            where mlrms.id = {} and mlrms.raport_number = '{}'
            group by mlrms.point, reportbefore , rmsbefore, pkbefore,pts.sort,reportafter,rmsafter,pkafter
            order by pts.sort""".format(rn,rn,did,rn,rn,did,did,rn)
            self.measresults = sqlio.read_sql_query(querry, self.conn)
            self.measresults['blrms'] = None
            self.measresults['alrms'] = None
            self.measresults['rmstrend'] = None
            self.measresults['pktrend'] = None

            querry = """select limit_1_name, limit_1_value,
                                limit_2_name,limit_2_value,
                                limit_3_name,limit_3_value,
                                limit_4_name,limit_4_value
                        from
                            standards 
                        where id = (select standard_fkey 
                                    from devices 
                                    where id = {})""".format(did)
            self.standardlimits = sqlio.read_sql_query(querry, self.conn)

            cc = -1
            for item in self.measresults.values:
                cc += 1
                if self.measresults['rmsbefore'].iloc[cc] > self.standardlimits['limit_1_value'].iloc[0]:
                    self.measresults.at[cc,'blrms'] = self.standardlimits['limit_1_name'].values[0]
                if self.measresults['rmsbefore'].iloc[cc] > self.standardlimits['limit_2_value'].iloc[0]:
                    self.measresults.at[cc,'blrms'] = self.standardlimits['limit_2_name'].values[0]
                if self.measresults['rmsbefore'].iloc[cc] > self.standardlimits['limit_3_value'].iloc[0]:
                    self.measresults.at[cc, 'blrms'] = self.standardlimits['limit_3_name'].values[0]
                if self.measresults['rmsbefore'].iloc[cc] > self.standardlimits['limit_4_value'].iloc[0]:
                    self.measresults.at[cc,'blrms']= self.standardlimits['limit_4_name'].values[0]

                if self.measresults['rmsafter'].iloc[cc] > self.standardlimits['limit_1_value'].iloc[0]:
                    self.measresults.at[cc,'alrms'] = self.standardlimits['limit_1_name'].values[0]
                if self.measresults['rmsafter'].iloc[cc] > self.standardlimits['limit_2_value'].iloc[0]:
                    self.measresults.at[cc,'alrms'] = self.standardlimits['limit_2_name'].values[0]
                if self.measresults['rmsafter'].iloc[cc] > self.standardlimits['limit_3_value'].iloc[0]:
                    self.measresults.at[cc, 'alrms'] = self.standardlimits['limit_3_name'].values[0]
                if self.measresults['rmsafter'].iloc[cc] > self.standardlimits['limit_4_value'].iloc[0]:
                    self.measresults.at[cc,'alrms']= self.standardlimits['limit_4_name'].values[0]

                if self.measresults['rmsafter'].iloc[cc] > self.measresults['rmsbefore'].iloc[cc]:
                    self.measresults.at[cc, 'rmstrend'] = 'UP'
                else:
                    self.measresults.at[cc, 'rmstrend'] = 'DOWN'

                if self.measresults['pkafter'].iloc[cc] > self.measresults['pkbefore'].iloc[cc]:
                    self.measresults.at[cc, 'pktrend'] = 'UP'
                else:
                    self.measresults.at[cc, 'pktrend'] = 'DOWN'
        getmeasquerry()

        self.beforereportlabel.config(text=self.measresults['reportbefore'][0])
        self.beforedatelabel.config(text=self.measresults['datebefore'][0])
        self.afterreportlabel.config(text=self.measresults['reportafter'][0])
        self.afterdatelabel.config(text=self.measresults['dateafter'][0])

        self.measurementsbeforetab.delete(*self.measurementsbeforetab.get_children())
        self.measurementsaftertab.delete(*self.measurementsaftertab.get_children())
        for item in self.measresults.values:
            if self.chosecolortype.current() == 0:
                self.measurementsbeforetab.insert('', 'end', text=item[0], values=(item[2], item[3]),tags =('white'))
                self.measurementsaftertab.insert('', 'end', text=item[0], values=(item[6], item[7]),tags =('white'))
            elif self.chosecolortype.current() == 1:
                if str(item[11]) == 'UP':
                    self.measurementsbeforetab.insert('', 'end', text=item[0], values=(item[2], item[3]),tags =('red'))
                else:
                    self.measurementsbeforetab.insert('', 'end', text=item[0], values=(item[2], item[3]), tags=('green'))
                self.measurementsaftertab.insert('', 'end', text=item[0], values=(item[6], item[7]),tags =('white'))
            elif self.chosecolortype.current() == 2:
                if str(item[12]) == 'UP':
                    self.measurementsbeforetab.insert('', 'end', text=item[0], values=(item[2], item[3]),tags =('red'))
                else:
                    self.measurementsbeforetab.insert('', 'end', text=item[0], values=(item[2], item[3]), tags=('green'))
                self.measurementsaftertab.insert('', 'end', text=item[0], values=(item[6], item[7]),tags =('white'))
            elif self.chosecolortype.current() == 3:
                if str(item[9]) == 'Cl. A' or \
                    str(item[9]) == 'Cl. B':
                    self.measurementsbeforetab.insert('', 'end', text=item[0], values=(item[2], item[3]),tags =('green'))
                elif str(item[9]) == 'Cl. C':
                    self.measurementsbeforetab.insert('', 'end', text=item[0], values=(item[2], item[3]),
                                                      tags=('yellow'))
                elif str(item[9]) == 'Cl. D':
                    self.measurementsbeforetab.insert('', 'end', text=item[0], values=(item[2], item[3]),
                                                      tags=('red'))
                else:
                    self.measurementsbeforetab.insert('', 'end', text=item[0], values=(item[2], item[3]),
                                                      tags=('grey'))

                if str(item[10]) == 'Cl. A' or \
                    str(item[10]) == 'Cl. B':
                    self.measurementsaftertab.insert('', 'end', text=item[0], values=(item[2], item[3]),tags =('green'))
                elif str(item[10]) == 'Cl. C':
                    self.measurementsaftertab.insert('', 'end', text=item[0], values=(item[2], item[3]),
                                                      tags=('yellow'))
                elif str(item[10]) == 'Cl. D':
                    self.measurementsaftertab.insert('', 'end', text=item[0], values=(item[2], item[3]),
                                                      tags=('red'))
                else:
                    self.measurementsaftertab.insert('', 'end', text=item[0], values=(item[2], item[3]),
                                                      tags=('grey'))

        self.updatecolor()

    def drawwindow(self):
        def changefeedbackwindow(evt):
            dflisted = self.presentfeedbacks.values.tolist()
            self.updatefeedbackwindows(dflisted[self.feedbacklist.curselection()[0]])
            self.updatedateinlabels()
            self.updatefdbmeas()
        self.root = tk.Tk()
        self.root.title('Feedbacker')

        self.listframe = tk.Frame(self.root)
        self.fdbframe = tk.Frame(self.root)

        self.listfilterframe = tk.Frame(self.listframe)
        self.feedbacklist = tk.Listbox(self.listframe, width=0, exportselection=False)
        self.feedbacklist.bind('<<ListboxSelect>>', changefeedbackwindow)
        self.makefilterwindow(self.listfilterframe)
        self.fillfdblist(self.presentfeedbacks)

        self.makefeedbackwindow(self.fdbframe)

        self.listframe.pack(side=LEFT, fill=Y)
        self.fdbframe.pack(side=LEFT, fill=Y)

        self.listfilterframe.pack(side=TOP)
        self.feedbacklist.pack(side=TOP, fill=Y, expand=1)

        self.root.mainloop()
    def filterdframe(self,filtertype, filterdet):
        if str(filtertype) == 'None':
            self.presentfeedbacks = self.fdbdFrame
        elif str(filtertype) == 'Ship':
            self.presentfeedbacks = self.fdbdFrame.loc[self.fdbdFrame.shipname == str(filterdet)]
        elif str(filtertype) == 'Report':
            self.presentfeedbacks = self.fdbdFrame.loc[self.fdbdFrame.raport_number == str(filterdet)]
        elif str(filtertype) == 'Fdb flag':
            filterby = str(filterdet)[filterdet.index('(') + 1:filterdet.index(')')]
            if int(filterby) == 0:
                self.presentfeedbacks = self.fdbdFrame.loc[ \
                    (self.fdbdFrame.fdbflag == int(filterby)) | \
                    (pd.isnull(self.fdbdFrame.fdbflag))]
            else:
                self.presentfeedbacks = self.fdbdFrame.loc[self.fdbdFrame.fdbflag == int(filterby)]

        elif str(filtertype) == 'Cost flag':
            filterby = str(filterdet)[filterdet.index('(') + 1:filterdet.index(')')]
            if int(filterby) == 0:
                self.presentfeedbacks = self.fdbdFrame.loc[ \
                    (self.fdbdFrame.costflag == int(filterby)) | \
                    (pd.isnull(self.fdbdFrame.costflag))]
            else:
                self.presentfeedbacks = self.fdbdFrame.loc[self.fdbdFrame.costflag == int(filterby)]
        elif str(filtertype) == 'Cost calc. missing':
            self.presentfeedbacks = self.fdbdFrame.loc[
                self.fdbdFrame['price'].astype(str).str.contains(filterdet) == True]

        self.fillfdblist(self.presentfeedbacks)
    def makefilterwindow(self, frame):
        def boxtypechange(evt):
            getdetvalues(self.filterlisboxtype.get())
        def getdetvalues(filtertype):
            # print(str(filtertype))
            detlist = list()
            if str(filtertype) == 'None':
                detlist = ['All']
            elif str(filtertype) == 'Ship':
                querry = "select name from main where id in (select parent from feedbacks group by parent) order by name"
                detlist = column(list(q_run(self.connD, querry)), 0)
            elif str(filtertype) == 'Report':
                querry = "select raport_number from feedbacks group by raport_number order by raport_number desc"
                detlist = (column(list(q_run(self.connD, querry)), 0))
            elif str(filtertype) == 'Fdb flag':
                querry = "select flagstr,lp from fdbflags order by lp"
                detlist.append("(0)None")
                for item in list(q_run(self.connD, querry)):
                    detlist.append('({}){}'.format(item[1], item[0]))
            elif str(filtertype) == 'Cost flag':
                querry = "select flagstr,lp from costflags order by lp"
                detlist.append("(0)None")
                for item in list(q_run(self.connD, querry)):
                    detlist.append('({}){}'.format(item[1], item[0]))
            elif str(filtertype) == 'Missing':
                detlist = ['no kW', 'no TYPE', 'NO COST CASE']
            self.filterlisboxdet.config(values=detlist)
            self.filterlisboxdet.current(0)
        def boxdetailchange(evt):
            self.filterdframe(self.filterlisboxtype.get(), self.filterlisboxdet.get())

        def sortchange(evt):
            sortby(self.sortlist.get())
        def sortby(filterby):
            if filterby == 'Ship':
                filterby = 'shipname'
            elif filterby == 'Device':
                filterby = 'devname'
            elif filterby == 'Structure':
                filterby = 'sort'
            elif filterby == 'Report':
                filterby = 'raport_number'
            elif filterby == 'Fdb flag':
                filterby = 'fdbflag'
            elif filterby == 'Cost flag':
                filterby = 'costflag'

            self.presentfeedbacks = self.presentfeedbacks.sort_values(by=[filterby])
            self.fillfdblist(self.presentfeedbacks)

        self.label1 = tk.Label(frame, text='Filter by: ')
        self.filterlisboxtype = ttk.Combobox(frame, text="",
                                             values=["None", "Ship", "Report", "Fdb flag", "Cost flag", "Missing"],
                                             state="readonly")
        self.filterlisboxtype.bind('<<ComboboxSelected>>', boxtypechange)



        self.filterlisboxdet = ttk.Combobox(frame, text="", state="readonly")
        self.filterlisboxdet.bind('<<ComboboxSelected>>', boxdetailchange)




        self.label2 = tk.Label(frame, text='Sort by: ')
        self.sortlist = ttk.Combobox(frame, width=10,
                                     values=['Ship', 'Device', 'Structure', 'Report', 'Fdb flag', 'Cost flag'],
                                     state="readonly")
        self.sortlist.bind('<<ComboboxSelected>>', sortchange)

        self.label1.grid(row=0, column=0)
        self.filterlisboxtype.grid(row=0, column=1)
        self.filterlisboxdet.grid(row=0, column=2)
        self.label2.grid(row=1, column=0)
        self.sortlist.grid(row=1, column=1)
    def updatefeedbackwindows(self, fdbstrip):
        def updateheadlabel(fdbstrip):
            headtext = """
    Ship: {}
    Device: {}
    Report: {}
            """.format(fdbstrip[1], fdbstrip[2], fdbstrip[3])
            self.labelhead.config(text=headtext)

            self.remarktext.configure(state='normal')
            self.fdbtext.configure(state='normal')

            self.remarktext.delete('1.0', END)
            try:
                self.remarktext.insert(END, fdbstrip[4])
            except:
                self.remarktext.insert(END, '#ERROR: MISSING REMARK IN DB')
            self.fdbtext.delete('1.0', END)
            self.fdbtext.insert(END, fdbstrip[6])
            self.fdbflagstring.current(fdbstrip[7])
            self.costflagstring.current(fdbstrip[8])

            self.remarktext.configure(state='disabled')
            self.fdbtext.configure(state='disabled')

            self.pricetext.delete('1.0', END)
            self.priceval.delete('1.0', END)
            if str(fdbstrip[9]) != 'None':
                self.pricetext.insert(END, fdbstrip[9][0])
                self.priceval.insert(END, fdbstrip[9][1])

            self.lowtext.delete('1.0', END)
            self.lowval.delete('1.0', END)
            if str(fdbstrip[10]) != 'None':
                self.lowtext.insert(END, fdbstrip[10][0])
                self.lowval.insert(END, fdbstrip[10][1])

            self.hightext.delete('1.0', END)
            self.highval.delete('1.0', END)
            if str(fdbstrip[11]) != 'None':
                self.hightext.insert(END, fdbstrip[11][0])
                self.highval.insert(END, fdbstrip[11][1])

        updateheadlabel(fdbstrip)
    def makefeedbackwindow(self, frame):
        def setflags():
            def loadcost():#devid):

                devid = (list(self.fdbdFrame.loc[self.fdbdFrame.fdbid == _id_, 'id'])[0])
                querry = 'select kw,type from devices where id = {}'.format(devid)
                devkw, devtype = list(q_run(self.connD, querry))[0]

                querry = "select costflag,typ, kwrange[1],kwrange[2], price[1],price[2], low[1],low[2] , high[1],high[2]from costcases"
                costcases = list(q_run(self.connD, querry))
                for case in costcases: #iteracja po costcase
                    devcostflag = list(self.presentfeedbacks.loc[self.presentfeedbacks.fdbid == _id_,'costflag'])
                    if costflag== 0:
                        pricestr = ''
                        priceval = ''
                        lowstr = ''
                        lowval = ''
                        highstr = ''
                        highval = ''
                        querry = "update feedbacks set price = null, low = null, high = null where _id_ = {}".format(str(_id_))
                        break
                    elif len(devtype) == 0:
                        pricestr = 'no TYPE'
                        priceval = '?'
                        lowstr = 'no TYPE'
                        lowval = '?'
                        highstr = 'no TYPE'
                        highval = '?'
                        querry = """UPDATE feedbacks set
                            price = ARRAY['{}','{}'],
                            low  = ARRAY['{}','{}'],
                            high = ARRAY['{}','{}']
                            where _id_ = {}""".format(pricestr,priceval,lowstr,lowval,highstr,highval,_id_)




                    elif self.costflagstring.current() in column(costcases,0): #jest flaga w bazie
                        if  str(self.costflagstring.current()) == str(case[0]): #flaga sie zgadza
                            if str(devtype).strip() == str(case[1]).strip(): # tutaj typ
                                kw = (re.findall(r'\d+\.*\d*', str(devkw))[0])
                                if (float(kw) >= float(case[2]) and float(kw) <= float(case[3])) or (case[2] == 0 and case[3] == 0):
                                    pricestr = case[4]
                                    priceval = case[5]
                                    lowstr = case[6]
                                    lowval = case[7]
                                    highstr = case[8]
                                    highval = case[9]
                                    querry = """UPDATE feedbacks set
                                price = ARRAY['{}','{}'],
                                low  = ARRAY['{}','{}'],
                                high = ARRAY['{}','{}']
                                where _id_ = {}""".format(pricestr, priceval, lowstr, lowval, highstr,
                                                                         highval, _id_)
                                    break
                            else:
                                pricestr = 'NO COST CASE'
                                priceval = '?'
                                lowstr = 'NO COST CASE'
                                lowval = '?'
                                highstr = 'NO COST CASE'
                                highval = '?'
                                querry = """UPDATE feedbacks set
                            price = ARRAY['{}','{}'],
                            low  = ARRAY['{}','{}'],
                            high = ARRAY['{}','{}']
                            where _id_ = {}""".format(pricestr, priceval, lowstr, lowval, highstr,
                                                                 highval,_id_)


                q_run(self.connD, querry)
                self.getquerry()
                self.filterdframe(self.filterlisboxtype.get(), self.filterlisboxdet.get())
                self.fillfdblist(self.presentfeedbacks)
                dflisted = self.presentfeedbacks.values.tolist()
                self.updatefeedbackwindows(dflisted[index])
                self.feedbacklist.select_set(index)
                self.feedbacklist.see(index)
            index = self.feedbacklist.curselection()[0]
            fdbflag = self.fdbflagstring.current()
            costflag = self.costflagstring.current()
            _id_ = self.presentfeedbacks.iloc[index].loc['fdbid']
            if fdbflag == 0: fdbflag = 'Null'
            if costflag == 0: costflag = 'Null'
            querry = """UPDATE feedbacks set fdbflag = {},costflag = {}
                where _id_ = {}""".format(fdbflag, costflag, _id_)
            q_run(self.connD, querry)
            if str(fdbflag) == 'Null': fdbflag = 0
            if str(costflag) == 'Null': costflag = 0


            self.getquerry()
            self.filterdframe(self.filterlisboxtype.get(), self.filterlisboxdet.get())
            self.fillfdblist(self.presentfeedbacks)
            self.feedbacklist.select_set(index)
            self.feedbacklist.see(index)

            loadcost()
        def updatecosts():
            index = self.feedbacklist.curselection()[0]
            _id_ = self.presentfeedbacks.iloc[index].loc['fdbid']

            price0 = self.pricetext.get("1.0",END).strip()
            price1 = self.priceval.get("1.0",END).strip()
            low0 = self.lowtext.get("1.0",END).strip()
            low1 = self.lowval.get("1.0",END).strip()
            high0 =self.hightext.get("1.0",END).strip()
            high1 = self.highval.get("1.0",END).strip()


            querry = """UPDATE feedbacks set
                            price = ARRAY['{}','{}'],
                            low  = ARRAY['{}','{}'],
                            high = ARRAY['{}','{}']
                            where _id_ = {}""".format(
                                                price0, price1,
                                                low0, low1,
                                                high0, high1,
                                                _id_)

            q_run(self.connD, querry)
            #print(querry)
            self.getquerry()
            self.filterdframe(self.filterlisboxtype.get(), self.filterlisboxdet.get())
            self.fillfdblist(self.presentfeedbacks)
            self.feedbacklist.select_set(index)
            self.feedbacklist.see(index)
        def fillmeasframe():
            def updatecolorevt(evt):
                self.generatetrendvalues()
            self.var = tk.IntVar(value=0)
            self.checkbut1 = ttk.Checkbutton(self.measframe, text='Show measurements',
                                             variable=self.var, command = self.updatefdbmeas)


            self.colorvar = tk.IntVar(value=0)


            self.chosecolortype = ttk.Combobox(self.measframe, text="",
                                                 values=["None", "RMS trend", "ENV trend", "Limits"],
                                                 state="readonly")
            self.chosecolortype.current(0)
            self.chosecolortype.bind('<<ComboboxSelected>>',  updatecolorevt)

            self.beforereportlabel = tk.Label (self.measframe, text = "#")
            self.beforedatelabel = tk.Label (self.measframe, text = "#")
            self.afterreportlabel = tk.Label (self.measframe, text = "#")
            self.afterdatelabel = tk.Label (self.measframe, text = "#")


            self.measurementsbeforetab = ttk.Treeview(self.measframe)
            self.measurementsbeforetab["columns"] = ("rms", "pk",)

            self.measurementsaftertab = ttk.Treeview(self.measframe)
            self.measurementsaftertab["columns"] = ("rms", "pk",)




            self.measurementsbeforetab.column("#0",width = 100,minwidth =50, stretch = tk.NO)
            self.measurementsbeforetab.column("rms",width = 40,minwidth =40, stretch = tk.NO)
            self.measurementsbeforetab.column("pk", width=40, minwidth=40, stretch=tk.NO)


            self.measurementsaftertab.column("#0",width = 100,minwidth =50, stretch = tk.NO)
            self.measurementsaftertab.column("rms",width = 40,minwidth =40, stretch = tk.NO)
            self.measurementsaftertab.column("pk", width=40, minwidth=40, stretch=tk.NO)





            self.measurementsbeforetab.heading("#0", text = 'Point',anchor=tk.W)
            self.measurementsbeforetab.heading("rms", text='RMS', anchor=tk.W)
            self.measurementsbeforetab.heading("pk", text='env P-K', anchor=tk.W)


            self.measurementsaftertab.heading("#0", text = 'Point',anchor=tk.W)
            self.measurementsaftertab.heading("rms", text='RMS', anchor=tk.W)
            self.measurementsaftertab.heading("pk", text='env P-K', anchor=tk.W)



            self.checkbut1.grid(column = 0, row = 0, columnspan = 2)
            tk.Label(self.measframe, text = 'Color by :').grid(column=0, row=1, sticky = E )
            self.chosecolortype.grid(column=1, row=1, sticky = W )

            self.beforereportlabel.grid(column = 0, row = 2)
            self.beforedatelabel.grid(column = 0, row = 3)
            self.afterreportlabel.grid(column = 1, row = 2)
            self.afterdatelabel.grid(column = 1, row = 3)


            self.measurementsbeforetab.grid(column = 0, row = 4)
            self.measurementsaftertab.grid(column = 1, row = 4)
        headtext = """
    Ship: {}
    Device: {}
    Report: {}
            """.format('SHIPNAME', 'DEVICENAME', 'REPORTNO')
        self.labelhead = tk.Label(frame, text=headtext)
        self.remarktext = tk.Text(frame, height=10, width=50, wrap=WORD)
        self.fdbtext = tk.Text(frame, height=10, width=50, wrap=WORD)
        self.fdbflagstring = ttk.Combobox(frame, width=90, values=column(self.fdbflagz, 1), state="readonly")
        self.costflagstring = ttk.Combobox(frame, width=90, values=column(self.costflagz, 1), state="readonly")
        self.remarktext.configure(state='disabled')
        self.fdbtext.configure(state='disabled')
        self.setflagbut = tk.Button(frame, text='Update flags', command=setflags)

        self.pricetext = tk.Text(frame, height=1, width=30, wrap=WORD)
        self.priceval = tk.Text(frame, height=1, width=30, wrap=WORD)

        self.lowtext = tk.Text(frame, height=1, width=30, wrap=WORD)
        self.lowval = tk.Text(frame, height=1, width=30, wrap=WORD)

        self.hightext = tk.Text(frame, height=1, width=30, wrap=WORD)
        self.highval = tk.Text(frame, height=1, width=30, wrap=WORD)

        self.setcostbut = tk.Button(frame, text='Update costs', command=updatecosts)

        self.measframe = tk.Frame(frame)

        self.remlabel = tk.Label(frame, text='Remark')
        self.fdblabel = tk.Label(frame, text='Feedback')

        # Grid manager
        self.labelhead.grid(row=0, column=0, columnspan=2)

        self.remlabel.grid(row=1, column=0, columnspan=2)
        self.remarktext.grid(row=2, column=0, columnspan=2)

        self.fdblabel.grid(row=1, column=2)
        self.fdbtext.grid(row=2, column=2)
        tk.Label(frame, text='FDB flag').grid(row=3, column=0)
        self.fdbflagstring.grid(row=3, column=1,columnspan = 2)
        self.fdbflagstring.current(0)
        tk.Label(frame, text='Cost flag').grid(row=4, column=0)
        self.costflagstring.grid(row=4, column=1,columnspan = 2)
        self.costflagstring.current(0)
        self.setflagbut.grid(row=5, column=2, columnspan=2, rowspan=2)

        tk.Label(frame, text='Price of work done').grid(row=7, column=0)
        self.pricetext.grid(row=7, column=1)
        self.priceval.grid(row=7, column=2)

        tk.Label(frame, text='Lowest cost of damage').grid(row=8, column=0)
        self.lowtext.grid(row=8, column=1)
        self.lowval.grid(row=8, column=2)

        tk.Label(frame, text='Highest cost of damage').grid(row=9, column=0)
        self.hightext.grid(row=9, column=1)
        self.highval.grid(row=9, column=2)

        self.setcostbut.grid(row=10, column=2)

        self.measframe.grid(row = 11, column = 0, columnspan = 3)
        fillmeasframe()


if __name__ == '__main__' :
    LogApplication()
    #feedbackswindow(connD)