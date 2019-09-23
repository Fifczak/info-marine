import psycopg2
import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
import csv
import pandas as pd

from tkinter.filedialog import askopenfilename
import tkinter as tkk
from tkinter import Tk
from tkinter import filedialog
#from tkinter import filedialog
from tqdm import tqdm
import xlrd
from tkinter import messagebox
from tkinter import simpledialog

host = '192.168.10.243'
#host = 'localhost'
devlist = list()
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
        connD = [user_get, pass_get, host]


        querry = "SELECT current_user"
        usercheck = ''

        usercheck = q_run(connD, querry)  # PYINSTALLER ma problemy gdzies tu
        if usercheck != '':
            self.root.destroy()
            StructWindow(connD,None)
class device:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.model = ''
        self.type = ''
        self.kw = ''
        self.rpm = ''
        self.pms = ''
        self.info = ''
        self.norm = ''
        self.drivenby = ''
        self.meas_condition = ''
        self.interval_type = ''
        self.interval_length = ''
        self.ignore_reminder = ''
        self.ignore_reminder_to = ''
        self.points = list()
        self.ctname = ''
class ctdev:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.nameindevice = ''
class Checkpointsframe(tk.Frame):
    'NIE DZIAŁA. JAKO ODDZIELNY MODUŁ WSZYTKO OK, WKLEJONY TUTAJ POKAZUJE GŁUPOTY'
    def __init__(self, pointspool):
        window = tk.Tk()
        tk.Frame.__init__(self, window)
        self.buttons = dict() #number to button widget
        self.createWidgets(window,pointspool)
        window.mainloop()

    def returnnewpointlist(self):
        self.ptslist = list()
        for n in range(self.rg):
            print(self.vars[n].get(),self.buttons[n].cget('text'))
            # if self.vars[n].get() == 1:
            #     self.ptslist.append(self.buttons[n].cget('text'))

        # print(self.ptslist)

    def createWidgets(self, window,pointspool):
        self.vars = []
        self.rg = len(pointspool)
        for n in range(self.rg):
            self.var = tk.IntVar(value = 1)
            self.vars.append(self.var)

        for n in range(self.rg):
            button = tk.Checkbutton(
                window,
                variable=self.vars[n],text = pointspool[n])
            button.pack(side = TOP)
            self.buttons[n] = button

        tk.Button(window, text='Accept', command=self.returnnewpointlist).pack(side=TOP)
class devicetypechosewindow:

    def __init__(self,parentframe,):
        self.parentframe = parentframe

        self.devtypewindow = tk.Tk()
        self.devtypewindow.title("Device type")
        self.sortbutton = Button(self.devtypewindow, text='Empty',command=lambda: self.insertdevice('empty'))
        self.sortbutton.pack(side=TOP, anchor=W)
        self.sortbutton = Button(self.devtypewindow, text='Horizontal motor',command=lambda: self.insertdevice('hormot'))
        self.sortbutton.pack(side=TOP, anchor=W)

        self.sortbutton = Button(self.devtypewindow, text='Horizontal pump',command=lambda: self.insertdevice('horpp'))
        self.sortbutton.pack(side=TOP, anchor=W)
        self.sortbutton = Button(self.devtypewindow, text='Vertical motor',command=lambda: self.insertdevice('vermot'))
        self.sortbutton.pack(side=TOP, anchor=W)
        self.sortbutton = Button(self.devtypewindow, text='Vertical pump',command=lambda: self.insertdevice('verpp'))
        self.sortbutton.pack(side=TOP, anchor=W)
        self.sortbutton = Button(self.devtypewindow, text='Separator',command=lambda: self.insertdevice('sep'))
        self.sortbutton.pack(side=TOP, anchor=W)
        self.sortbutton = Button(self.devtypewindow, text='Diesel Engine',command=lambda: self.insertdevice('dg'))
        self.sortbutton.pack(side=TOP, anchor=W)
        self.sortbutton = Button(self.devtypewindow, text='Alternator',command=lambda: self.insertdevice('ae'))
        self.sortbutton.pack(side=TOP, anchor=W)
        self.sortbutton = Button(self.devtypewindow, text='Main engine',command=lambda: self.insertdevice('me'))
        self.sortbutton.pack(side=TOP, anchor=W)
        self.sortbutton = Button(self.devtypewindow, text='Cargo turbine',command=lambda: self.insertdevice('ct'))
        self.sortbutton.pack(side=TOP, anchor=W)

        self.devtypewindow.mainloop()

    def uploadnewdevice(self):
        'method to upload new device to database'

    def insertdevice(self,type):
        if str(type).strip() == 'empty':
            newname = simpledialog.askstring("Add device", "Device name:")
            if str(newname).strip() != '' and  str(newname).strip() != 'None':
                querry = "insert into devices (parent,name) values ({},'{}') ".format(self.parentframe.shipid, newname)
                q_run(self.parentframe.connD, querry)
                querry = "select max(id) from devices"
                newid = list(q_run(self.parentframe.connD, querry))[0][0]
        else:
            pointspool = list()
            if str(type).strip() == 'hormot':
                pointspool = ['H1', 'V1', 'H2', 'V2', 'A2']
                type = 'el.motor'
                inval = 'el. motor'
            elif str(type).strip() == 'horpp':
                pointspool = ['H3', 'V3', 'H4', 'V4']
                type = 'Pump'
                inval = 'pump'
            elif str(type).strip() == 'vermot':
                pointspool = ['H1', 'HH1', 'H2', 'HH2', 'A2']
                type = 'el.motor'
                inval = 'el. motor'
            elif str(type).strip() == 'verpp':
                pointspool = ['H3', 'HH3', 'H4', 'HH4']
                type = 'Pump'
                inval = 'pump'
            elif str(type).strip() == 'sep':
                pointspool = ['H3','HH3','H4','HH4','Foot H1','Foot HH1', 'Foot V1','Top H7']
                type = 'Separator'
                inval = 'Separator'
            elif str(type).strip() == 'dg':
                pointspool = ['NDE top H','NDE frame H','H1','H2','H3','H4','H5','H6','H7','DE top H','DE frame H']
                type = 'Diesel engine'
                inval = 'DG'
            elif str(type).strip() == 'ae':
                pointspool = ['De foot','H1','A1 for H1','V1','A1','A1 for V1','H2','A2 for H2','V2','A2 for V2','NDE foot']
                type = 'None'
                inval = 'Alternator'
            elif str(type).strip() == 'me':
                pointspool = ['C1','C2','C3','C4','C5','C6','2.3A for H1','Top 3.3 H','Top 3.3 V','Top 3.3 A','Top 3.2 H','Top 3.2 V','Top 3.1 H','Top 3.1 V','Top 3.1 A','2.1A for H7','H1','H2','H3','H4','H5','H6','H7','Found 1.1 H','Found 1.2 H','Found 1.3 H']
                type = 'Pump'
                inval = 'Main Engine'
            elif str(type).strip() == 'ct':
                pointspool = ['H1', 'HH1', 'H2', 'HH2','H3','HH3','H4','HH4','H5','HH5']
                type = 'Cargo turbine'
                inval = 'Cargo turbine'


            #TODO: NIE DZIALA. MOZE ZROBIC JAKOS INNACZEJ :/
            # ckpfr = Checkpointsframe(pointspool)
            # print('HAHAHAHAH')

            newname = simpledialog.askstring("Add device", "Device name:", initialvalue=inval)
            if str(newname).strip() != '' and  str(newname).strip() != 'None':
                querry = "insert into devices (parent,name,type) values ({},'{}','{}') ".format(self.parentframe.shipid, newname,type)
                q_run(self.parentframe.connD, querry)
                querry = "select max(id) from devices"
                newid = list(q_run(self.parentframe.connD, querry))[0][0]
                i=0
                for item in pointspool:
                    i +=1
                    querry = "INSERT INTO POINTS(id,point,sort,visible) VALUES({},'{}',{},True)".format(newid,item,i)
                    q_run(self.parentframe.connD, querry)


        self.parentframe.reloadquerry(self.parentframe.structuresort, self.parentframe.shipid, self.parentframe.connD, False)
class PointComboboxObject:
    def callback(self, event=None):
        self.changecapt(self.showvalue,self.var.get(),self.sort)
        self.showvalue = self.var.get()
    def changecapt(self,oldval,newval,oR):
        clickBearing = (self.parentclass.CombBearingList[oR].showvalue)  ## MOJE AKTUALNE
        clickSealBearing = (self.parentclass.CombBearingSealList[oR].showvalue)
        clickAddBearing = (self.parentclass.CombBearingAddList[oR].showvalue)
        clickVisibleBearing = (self.parentclass.CombVisibleList[oR].showvalue)
        nR = -1
        for line in self.parentclass.CombPointList:
            nR+=1
            if line.showvalue == newval:
                line.cbox.delete(0, END)
                line.cbox.insert(0, oldval)
                line.showvalue = oldval
                clickRingBearing = (self.parentclass.CombBearingList[nR].showvalue)  ## bearing w tym ktory ma ten sam point
                clickRingBearingSeal = (self.parentclass.CombBearingSealList[nR].showvalue)
                clickRingBearingAdd = (self.parentclass.CombBearingAddList[nR].showvalue)
                clickRingVisibleBearing = (self.parentclass.CombVisibleList[nR].showvalue)
                self.parentclass.CombBearingList[nR].cbox.delete(0, END) #delete w tym ktory ma ten sam point
                self.parentclass.CombBearingList[nR].cbox.insert(0, clickBearing)
                self.parentclass.CombBearingList[nR].showvalue = clickBearing
                self.parentclass.CombBearingSealList[nR].cbox.delete(0, END)
                self.parentclass.CombBearingSealList[nR].cbox.insert(0, clickSealBearing)
                self.parentclass.CombBearingSealList[nR].showvalue = clickSealBearing
                self.parentclass.CombBearingAddList[nR].cbox.delete(0, END)
                self.parentclass.CombBearingAddList[nR].cbox.insert(0, clickAddBearing)
                self.parentclass.CombBearingAddList[nR].showvalue = clickAddBearing
                self.parentclass.CombVisibleList[nR].cbox.delete(0, END)
                self.parentclass.CombVisibleList[nR].cbox.insert(0, clickVisibleBearing)
                self.parentclass.CombVisibleList[nR].showvalue = clickVisibleBearing
                self.parentclass.CombBearingList[oR].cbox.delete(0, END)  # delete w wybranym
                self.parentclass.CombBearingList[oR].cbox.insert(0, clickRingBearing)
                self.parentclass.CombBearingList[oR].showvalue = clickRingBearing
                self.parentclass.CombBearingSealList[oR].cbox.delete(0, END)
                self.parentclass.CombBearingSealList[oR].cbox.insert(0, clickRingBearingSeal)
                self.parentclass.CombBearingSealList[oR].showvalue = clickRingBearingSeal
                self.parentclass.CombBearingAddList[oR].cbox.delete(0, END)
                self.parentclass.CombBearingAddList[oR].cbox.insert(0, clickRingBearingAdd)
                self.parentclass.CombBearingAddList[oR].showvalue = clickRingBearingAdd
                self.parentclass.CombVisibleList[oR].cbox.delete(0, END)
                self.parentclass.CombVisibleList[oR].cbox.insert(0, clickRingVisibleBearing)
                self.parentclass.CombVisibleList[oR].showvalue = clickRingVisibleBearing
    def __init__(self,parentframe,inlist,c,parentClass):
        self.parentclass = parentClass
        self.sort = c-1

        self.showvalue = str(inlist[c-1])

        self.valueslist = list()
        self.var = tk.StringVar()
        self.cbox = ttk.Combobox(parentframe, textvariable=self.var, values=inlist)
        self.cbox.grid(row=c, column=1)
        self.cbox.bind('<<ComboboxSelected>>',self.callback)
        self.cbox.insert(0, inlist[c-1])

        self.cbox.configure(values=inlist)
class BearingComboboxObject:
    def callback(self, event=None):
        self.showvalue = self.var.get()
    def __init__(self,parentframe,bearing,c,col,inlist2):
        self.showvalue = str(bearing)
        self.valueslist = list()
        self.var = tk.StringVar()
        self.cbox = ttk.Combobox(parentframe, textvariable=self.var)
        self.cbox.grid(row=c, column=col)
        self.cbox.bind('<<ComboboxSelected>>', self.callback)
        self.cbox.insert(0, str(bearing))
        self.cbox.configure(values=inlist2)
class DragDropListbox(tk.Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """
    def __init__(self, master, **kw):
        kw['selectmode'] = tk.SINGLE
        tk.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)


    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            color = self.itemcget(i, "background")
            color2 = self.itemcget(i, "fg")
            self.delete(i)
            self.insert(i+1, x)
            self.itemconfig(i + 1, background=color, fg = color2)

            self.curIndex = i

        if i > self.curIndex:
            x = self.get(i)
            color = self.itemcget(i, "background")
            color2 = self.itemcget(i, "fg")
            self.delete(i)
            self.insert(i-1, x)
            self.itemconfig(i-1, background=color, fg = color2)
            self.curIndex = i
class chosedevicewindow():
    def __init__(self,connD,shipid,listbox):
        def insertdevice():
            name = ships[cbox.current()]
            id = ids[cbox.current()]
            try:
                idx = listbox.curselection()[0]
            except:
                idx = 0
            listbox.insert(idx+1,'{}@{}'.format(name,id)  )

        self.devwindow = tk.Tk()
        self.devwindow.title("Structure")

        label = tk.Label(self.devwindow,text = 'Chose device')
        label.grid(row=0, column = 0)

        querry = "select name,id from devices where parent = {} order by name".format(shipid)
        ans = list(q_run(connD,querry))
        ships = column(ans,0)
        ids = column(ans, 1)
        self.var = tk.StringVar()
        cbox = ttk.Combobox(self.devwindow, textvariable=self.var, values=ships,state="readonly",width = 50)
        cbox.grid(row = 0, column = 1)


        addbut = tk.Button(self.devwindow,text = 'Add device', command = insertdevice).grid(row = 1, column = 0)


        self.devwindow.mainloop()
class TypeModelWindow():
    def ok(self):
        if str(self.modelentry.get()).strip() != '':
            querry = "insert into main_models (parent,name,type) values ({},'{}','{}')".format(self.makerid,self.modelentry.get(),self.cbox.get())
            (q_run(self.connD, querry))
            self.typewindow.destroy()

            querry = "select id,name from main_models where parent is null and name <> '' and name <> ' ' order by name"
            ans = list(q_run(self.connD, querry))
            self.parentframe.makers = column(ans, 1)
            self.parentframe.makersids = column(ans, 0)
            self.parentframe.cbox.config(values=self.parentframe.makers)

            self.parentframe.cbox.current(0)

            querry = "select id,name,type from main_models where parent = {} order by name".format(self.parentframe.makersids[0])
            ans = list(q_run(self.connD, querry))
            self.parentframe.models = column(ans, 1)
            self.parentframe.modelsids = column(ans, 0)
            self.parentframe.types = column(ans, 2)
            self.parentframe.cbox2.config(values=self.parentframe.models)

            self.parentframe.cbox2.current(0)
            self.parentframe.typelabel.config(text=self.parentframe.types)


            #self.parentframe.devwindow.destroy()
            #ModelMakerWindow(self.connD)
        else:
            messagebox.showinfo("Error", 'Model empty')
    def __init__(self,connD,makerid,parentframe):
        self.makerid = makerid
        self.connD = connD
        self.parentframe = parentframe
        self.typewindow = tk.Tk()
        self.typewindow.title("Model / Type")
        label = tk.Label(self.typewindow, text='Model')
        label.grid(row=0, column=0)

        self.modelentry = tk.Entry(self.typewindow, width=50)
        self.modelentry.grid(row=0, column=1)
        label = tk.Label(self.typewindow, text='Type:')
        label.grid(row=1, column=0)
        self.var = tk.StringVar()

        querry = "select type from devices where type is distinct from null and type <> '' group by type order by type"
        ans = list(q_run(connD, querry))
        self.types = column(ans, 0)
        self.var = tk.StringVar()


        self.cbox = ttk.Combobox(self.typewindow, textvariable=self.var,values = self.types, width=50)
        self.cbox.grid(row=1, column=1)




        #addbut = tk.Button(self.typewindow, text='Add device', command=insertdevice).grid(row=2, column=0)

        okbut = tk.Button(self.typewindow, text='Add model', command = self.ok)
        okbut.grid(row=2, column=1)


        self.typewindow.mainloop()
class ModelMakerWindow():
    def accept(self):
        self.parentframe.lab_model_e.configure(text = self.cbox2.get())
        self.parentframe.lab_type_e.delete(0, END)
        self.parentframe.lab_type_e.insert(0, str(self.typelabel.cget("text")))

    def maker_change(self,event):
        idx = self.cbox.current()
        querry = "select id,name,type from main_models where parent = {} order by name".format(self.makersids[idx])
        ans = list(q_run(self.connD, querry))
        self.models = column(ans, 1)
        self.modelsids = column(ans, 0)
        self.types = column(ans, 2)
        self.cbox2.config(values=self.models)
        try:
            self.cbox2.current(0)
            self.typelabel.config(text = self.types[0])
        except:
            self.cbox2.config(text = ' ')
            self.typelabel.config(text=' ')
    def model_change(self,event):
        idx = self.cbox2.current()
        self.typelabel.config(text = self.types[idx])
    def addmaker(self):
        maker = simpledialog.askstring("Add maker", "Enter maker name:")
        if str(maker).strip() != '':
            querry = "INSERT INTO main_models (name) VALUES ('{}')".format(maker)
            q_run(self.connD, querry)
            querry = "select id,name from main_models where parent is null and name <> '' and name <> ' ' order by name"
            ans = list(q_run(self.connD, querry))
            self.makers = column(ans, 1)
            self.makersids = column(ans, 0)
            self.cbox.config(values = self.makers)

            self.cbox.current(0)

            querry = "select id,name,type from main_models where parent = {} order by name".format(self.makersids[0])
            ans = list(q_run(self.connD, querry))
            self.models = column(ans, 1)
            self.modelsids = column(ans, 0)
            self.types = column(ans, 2)
            self.cbox2.config(values=self.models)

        else:
            messagebox.showinfo("Error", 'Maker empty')
    def addmodel(self):
        idx = self.cbox.current()
        if str(self.makersids[idx]).strip() != '':
            TypeModelWindow(self.connD, self.makersids[idx],self)
        else:
            messagebox.showinfo("Error", 'Chose maker')
    def __init__(self,connD,parentframe):
        self.connD = connD
        self.parentframe = parentframe
        self.devwindow = tk.Tk()
        self.devwindow.title("Structure")
        label = tk.Label(self.devwindow, text='Maker')
        label.grid(row=0, column=0)
        querry = "select id,name from main_models where parent is null and name <> '' and name <> ' ' order by name"
        ans = list(q_run(connD, querry))
        self.makers = column(ans, 1)
        self.makersids = column(ans, 0)
        self.var = tk.StringVar()
        self.cbox = ttk.Combobox(self.devwindow, textvariable=self.var, values=self.makers, state="readonly", width=50)
        self.cbox.bind('<<ComboboxSelected>>', self.maker_change)
        self.cbox.grid(row=0, column=1)
        self.cbox.current(0)


        querry = "select id,name,type from main_models where parent = {} order by name".format(self.makersids[0])
        ans = list(q_run(self.connD, querry))
        models = column(ans, 1)
        modelsids = column(ans, 0)
        self.types = column(ans, 2)



        label = tk.Label(self.devwindow, text='Model')
        label.grid(row=1, column=0)
        self.var2 = tk.StringVar()

        self.cbox2 = ttk.Combobox(self.devwindow, textvariable=self.var2, state="readonly",values=models, width=50)
        self.cbox2.grid(row=1, column=1)
        self.cbox2.bind('<<ComboboxSelected>>', self.model_change)
        label2 = tk.Label(self.devwindow, text = 'Type: ')
        label2.grid(row = 2, column = 0)
        self.typelabel= tk.Label(self.devwindow, text = '-')
        self.typelabel.grid(row = 2, column =1 )


        addmakerbut = tk.Button(self.devwindow, text='Add maker', command = self.addmaker)
        addmakerbut.grid(row=0, column=2)
        addmodelbut = tk.Button(self.devwindow, text='Add model', command = self.addmodel)
        addmodelbut.grid(row=1, column=2)

        addmakerbut = tk.Button(self.devwindow, text='Change model', command=self.accept)
        addmakerbut.grid(row=3, column=1)

        self.devwindow.mainloop()
class StructWindow:
    class CrosstableFrame:
        'off'
        def searchinlist(self):
            for i, listbox_entry in enumerate(self.deviceslistbox.get(0, END)):
                if str(self.searchen.get()).strip() != '':
                    listboxname = (listbox_entry[listbox_entry.rfind('NAME:'):listbox_entry.rfind('ID:')]).strip()
                    if str(self.searchen.get()).strip().upper() in str(listboxname).upper():
                        self.deviceslistbox.itemconfig(i, bg='green')
                    else:
                        self.deviceslistbox.itemconfig(i, bg='white')
                else:
                    self.deviceslistbox.itemconfig(i, bg='white')

        def namesort(self):
            self.st = 'namesort'
            querry = """
            select dev.id,cr.nameindevice,dev.name
            from devices dev
            left join crosstable cr on cr.id = dev.id
            left join ds_structure dss on cast(dev.id as text) = dss.id
            where dev.parent = {}
            order by dev.name
            """.format(self.shipid)
            ans = q_run(self.connD,querry)
            self.devdata = list()
            self.devdata = list()
            self.devdata.clear()
            for item in ans:
                self.devdata.append(item)
            self.loaddevices('namesort')
        def crossnamesort(self):
            self.st = 'crossnamesort'
            querry = """
            select dev.id,cr.nameindevice,dev.name
            from devices dev
            left join crosstable cr on cr.id = dev.id
            left join ds_structure dss on cast(dev.id as text) = dss.id
            where dev.parent = {}
            order by cr.nameindevice,dev.name
            """.format(self.shipid)
            ans = q_run(self.connD,querry)
            self.devdata = list()
            self.devdata = list()
            self.devdata.clear()
            for item in ans:
                self.devdata.append(item)
            self.loaddevices('crossnamesort')
        def structuresort(self):
            self.st = 'structuresort'
            querry = """
            select dev.id,cr.nameindevice,dev.name
            from devices dev
            left join crosstable cr on cr.id = dev.id
            left join ds_structure dss on cast(dev.id as text) = dss.id
            where dev.parent = {}
            order by dss.sort,dev.name
            """.format(self.shipid)
            ans = q_run(self.connD,querry)
            self.devdata = list()
            self.devdata = list()
            self.devdata.clear()
            for item in ans:
                self.devdata.append(item)
            self.loaddevices('structuresort')
        def loaddevices(self,sorttype):
            self.deviceslistbox.delete(0, END)
            devlist.clear()
            for line in self.devdata:
                dev = ctdev()
                if str(sorttype) == 'namesort':
                    self.deviceslistbox.insert(END, 'NAME: {} ID: {} NAMEINDEVICE: {} '.format(line[2],line[0],line[1]))
                if str(sorttype) == 'crossnamesort':
                    self.deviceslistbox.insert(END, 'NAMEINDEVICE: {} NAME: {} ID: {}'.format(line[1],line[2],line[0]))
                if str(sorttype) == 'structuresort':
                    self.deviceslistbox.insert(END, 'NAME: {} ID: {} NAMEINDEVICE: {} '.format(line[2],line[0],line[1]))
                dev.id = str(line[0])
                dev.nameindevice = str(line[1])
                dev.name = str(line[2])
                devlist.append(dev)
            self.deviceslistbox.pack(fill=BOTH, expand = 1)

        def __init__(self,parent,shipid,connD):
            def getdetails(evt):
                w = evt.widget
                w = evt.widget
                index = int(w.curselection()[0])
                devname = w.get(index)
                id = self.devdata[index][0]
                nameindevice = self.devdata[index][1]
                newnameindevice = simpledialog.askstring("Change routename","New crosstable name:", initialvalue= nameindevice)

                if str(newnameindevice).strip() != '' and str(newnameindevice) != 'None':

                    querry = ("update crosstable set nameindevice = '{}' where id = {} returning *".format(newnameindevice,id))
                    if len(q_run(connD,querry)) == 0:
                        querry = ("INSERT INTO crosstable(parent,nameindevice,id) VALUES ({},'{}',{})".format(shipid,
                            newnameindevice, id))
                        q_run(connD, querry)
                    else:
                        querry = ("update crosstable set nameindevice = '{}' where id = {}".format(
                            newnameindevice, id))
                        q_run(connD, querry)


                if self.st == 'namesort':
                    self.namesort()
                elif self.st == 'crossnamesort':
                    self.crossnamesort()
                elif self.st == 'structuresort':
                    self.structuresort()


            self.connD = connD
            self.shipid = shipid
            self.searchen = Entry(parent)
            self.searchen.pack(side = TOP, anchor = W)
            self.searchbutton = Button(parent,text = 'Search', command = lambda: self.searchinlist())
            self.searchbutton.pack(side = TOP, anchor = W)
            self.sortbutton1 = Button(parent,text = 'Name sort', command = self.namesort )
            self.sortbutton1.pack(side = TOP, anchor = W)
            self.sortbutton2 = Button(parent,text = 'Crosstable sort', command = self.crossnamesort)
            self.sortbutton2.pack(side = TOP, anchor = W)
            self.sortbutton3 = Button(parent,text = 'Structure sort', command = self.structuresort )
            self.sortbutton3.pack(side = TOP, anchor = W)
            self.deviceslistbox = Listbox(parent, exportselection=False)
            self.deviceslistbox.config(width=0)
            self.detailframe = Frame(parent)
            self.detailframe.pack(side=RIGHT, anchor=W, fill=BOTH, expand = 1)
            self.structuresort()
            self.deviceslistbox.bind('<Double-Button>', getdetails)
            parent.pack(side=LEFT)
    class DevicesFrame:
        def clonedevice(self):
            if str(self.lab_model_e.cget("text")) == 'None':
                model = ''
            else:
                model = self.lab_model_e.cget("text")
            interval = "{} {}".format(self.lab_interval_length_e.get(), self.lab_interval_type_e.get())
            if str(self.lab_kw_e.get()) == 'None':
                kw = '0'
            else:
                kw = self.lab_kw_e.get()
            ignorerminderto = self.ig_rem_to_e.get()
            if str(ignorerminderto) == 'None':
                ignorerminderto = 'Null'
            else:
                ignorerminderto = "'{}'".format(ignorerminderto)

            drivenby = 0

            querry = """INSERT INTO devices (parent,name,model, model_fkey ,
            type,kw,rpm,pms,info,norm,standard_fkey,drivenby,meas_condition,
            cm,cbm_interval,ignore_reminder,ignore_reminder_to)
            VALUES ({},'{}','{}',(select id from main_models where name = '{}' limit 1),'{}',{},'{}','{}','{}','{}',(select id from standards where standard ='{}' limit 1),'{}','{}','{}','{}','{}',{})"""\
                .format(self.shipid,'{}-CLONED'.format(self.lab_name_e.get()),model,model, self.lab_type_e.get(),kw,
                        self.lab_rpm_e.get(), self.lab_pms_e.get(),self.lab_info_e.get("1.0", END),self.lab_norm_e.get(),self.lab_norm_e.get(),drivenby,self.lab_meas_condition_e.get(),
                        self.lab_cm_e.get(),interval,self.ig_rem_e.get(),ignorerminderto)

            q_run(self.connD, querry)

            querry = """SELECT id FROM devices WHERE parent = {} and name = '{}' and model = '{}' 
            and model_fkey = (select id from main_models where name = '{}' limit 1) and
            type = '{}' and kw = '{}' and rpm = '{}' and pms = '{}' and info = '{}' and 
            norm = '{}' and standard_fkey = (select id from standards where standard ='{}' limit 1) and drivenby = '{}'
             and meas_condition = '{}'"""\
                .format(self.shipid,'{}-CLONED'.format(self.lab_name_e.get()),model,model, self.lab_type_e.get(),kw,
                        self.lab_rpm_e.get(), self.lab_pms_e.get(),self.lab_info_e.get("1.0", END),self.lab_norm_e.get(),self.lab_norm_e.get(),drivenby,self.lab_meas_condition_e.get(),
                        self.lab_cm_e.get(),interval,self.ig_rem_e.get(),ignorerminderto)

            newdevid = list(q_run(self.connD, querry))[0][0]

            for line in self.pointlist:
                querry = "insert into points(id, point,sort, visible) values({},'{}','{}',True)"\
                    .format(newdevid,line[0],line[1])
                q_run(self.connD, querry)

            self.reloadquerry(self.structuresort, self.shipid, self.connD, False)
        def searchinlist(self):
            for i, listbox_entry in enumerate(self.deviceslistbox.get(0, END)):
                if str(self.searchen.get()).strip() != '':
                    listboxname = (listbox_entry[0:listbox_entry.rfind('@')]).strip()
                    if str(self.searchen.get()).strip().upper() in str(listboxname).upper():
                        self.deviceslistbox.itemconfig(i, bg = 'green')
                    else:
                        self.deviceslistbox.itemconfig(i, bg='white')
                else:
                    self.deviceslistbox.itemconfig(i, bg='white')
        def insertdevice(self):
            newname = simpledialog.askstring("Add maker", "Enter maker name:")
            if str(newname).strip() != '':
                querry = "insert into devices (parent,name) values ({},'{}')".format(self.shipid,newname)
                q_run(self.connD, querry)
                self.reloadquerry(self.structuresort, self.shipid, self.connD, False)
        def reloadquerry(self,structuresort,shipid,connD,chagesort):
            if chagesort == False:
                if structuresort == True: structuresort = False
                else: structuresort = True
            if structuresort == True:
                querry = """select dev.id, dev.name,mm.name,dev.type,kw,rpm,pms,info,st.standard,drivenby, meas_condition,cm,(public.im_extract(dev.cbm_interval))[1] as interval_type,(public.im_extract(dev.cbm_interval))[2] as interval_len,dev.ignore_reminder, dev.ignore_reminder_to,ct.nameindevice
                            from devices dev
                            left join ds_structure dss on cast(dev.id as text) = dss.id
                            left join main_models mm on dev.model_fkey = mm.id
                            left join standards st on dev.standard_fkey = st.id
                            left join crosstable ct on dev.id = ct.id
                            where dev.parent ={}
                            order by dss.sort""".format(str(shipid))
                ans = q_run(connD, querry)

                self.structuresort = False
            else:
                querry = """select dev.id, dev.name,mm.name,dev.type,kw,rpm,pms,info,st.standard,drivenby, meas_condition,cm,(public.im_extract(dev.cbm_interval))[1] as interval_type,(public.im_extract(dev.cbm_interval))[2] as interval_len,dev.ignore_reminder, dev.ignore_reminder_to,ct.nameindevice
                            from devices dev
                            left join ds_structure dss on cast(dev.id as text) = dss.id
                            left join main_models mm on dev.model_fkey = mm.id
                            left join standards st on dev.standard_fkey = st.id
                            left join crosstable ct on dev.id = ct.id
                            where dev.parent ={}
                            order by dev.name""".format(str(shipid))
                ans= q_run(connD, querry)
                self.structuresort = True
            self.devdata = list()
            self.devdata.clear()
            for item in ans:
                self.devdata.append(item)


            self.loaddevices()
        def loaddevices(self):
            self.deviceslistbox.delete(0, END)
            idlist = list()
            devlist.clear()
            for line in self.devdata:
                self.dev = device()
                self.deviceslistbox.insert(END, '{} @ {}'.format(line[1],line[0]))
                self.dev.id = str(line[0])
                idlist.append(str(line[0]))
                self.dev.name = str(line[1])
                self.dev.model = str(line[2])
                self.dev.type = str(line[3])
                self.dev.kw = str(line[4])
                self.dev.rpm = str(line[5])
                self.dev.pms = str(line[6])
                self.dev.info = str(line[7])
                self.dev.norm = str(line[8])
                self.dev.drivenby = str(line[9])
                self.dev.meas_condition = str(line[10])
                self.dev.cm = str(line[11])
                self.dev.ctname = str(line[16])


                if str(line[12]) == '1' : self.dev.interval_type = "Day"
                elif str(line[12]) == '2' : self.dev.interval_type = "Week"
                elif str(line[12]) == '3' : self.dev.interval_type = "Month"
                elif str(line[12]) == '4': self.dev.interval_type = "Year"
                self.dev.interval_length = line[13]


                self.dev.ignore_reminder = str(line[14])
                self.dev.ignore_reminder_to = str(line[15])

                devlist.append(self.dev)

            self.deviceslistbox.pack(fill=BOTH, expand = 1)
            if str(self.master.selid) != 'None':
                try:
                    idx = idlist.index(self.master.selid)
                except:
                    print('No id', self.master.selid)
                    idx = 0
                self.deviceslistbox.select_set(idx)
                self.deviceslistbox.see(idx)

            #self.deviceslistbox.event_generate('<Double-Button>')
        def showmodelframe(self):
            ModelMakerWindow(self.connD,self)

        def fillstandarddetailsframe(self,id):
            querry = """select standard,informations,envflag
                limit_1_name, round(limit_1_value,1),
                limit_2_name, round(limit_2_value,1),
                limit_3_name, round(limit_3_value,1),
                limit_4_name, round(limit_4_value,1)
                from standards where id = 
                (select standard_fkey from devices where id = {} limit 1) limit 1""".format(id)
            try:
                standard = list(q_run(self.connD,querry))[0]
            except:
                standard = ['None','None','None','None','None','None','None','None','None','None']
            workframe = self.standarddetailsframe

            workframe.n1 = tk.Label(workframe, text = standard[2])
            workframe.n1.grid(row = 0, column = 0)
            workframe.n2 = tk.Label(workframe, text = standard[4])
            workframe.n2.grid(row = 1, column = 0)
            workframe.n3 = tk.Label(workframe, text = standard[6])
            workframe.n3.grid(row = 2, column = 0)
            workframe.n4 = tk.Label(workframe, text = standard[8])
            workframe.n4.grid(row = 3, column = 0)


            workframe.v1 = tk.Label(workframe, text = standard[3])
            workframe.v1.grid(row = 0, column = 1)
            workframe.v2 = tk.Label(workframe, text = standard[5])
            workframe.v2.grid(row = 1, column = 1)
            workframe.v3 = tk.Label(workframe, text = standard[7])
            workframe.v3.grid(row = 2, column = 1)
            workframe.v4 = tk.Label(workframe, text = standard[9])
            workframe.v4.grid(row = 3, column = 1)

            workframe.standardinfo = tk.Text(workframe,height = 10, width = 35)
            workframe.standardinfo.insert('1.0', standard[1])
            workframe.standardinfo.config(state=DISABLED)
            workframe.standardinfo.grid(row=0, column=3,rowspan = 4)


        def changestandardetail(self,standardname):
            querry = """select standard,informations,envflag
                limit_1_name, round(limit_1_value,1),
                limit_2_name, round(limit_2_value,1),
                limit_3_name, round(limit_3_value,1),
                limit_4_name, round(limit_4_value,1)
                from standards where standard =  '{}' limit 1""".format(standardname)
            standard = list(q_run(self.connD,querry))[0]
            print(standard)

            self.standarddetailsframe.n1.config(text=standard[2])
            self.standarddetailsframe.n2.config(text=standard[4])
            self.standarddetailsframe.n3.config(text=standard[6])
            self.standarddetailsframe.n4.config(text=standard[8])

            self.standarddetailsframe.v1.config(text=standard[3])
            self.standarddetailsframe.v2.config(text=standard[5])
            self.standarddetailsframe.v3.config(text=standard[7])
            self.standarddetailsframe.v4.config(text=standard[9])

            self.standarddetailsframe.standardinfo.config(state=NORMAL)
            self.standarddetailsframe.standardinfo.delete('1.0', END)
            self.standarddetailsframe.standardinfo.insert('1.0', standard[1])
            self.standarddetailsframe.standardinfo.config(state=DISABLED)



        def makedeviceswindow(self, line, id,connD):
            def changestandardetail(evt):
                self.changestandardetail(self.lab_norm_e.get())
            if str(line.id).strip() == str(id).strip():
                querry = "select point, sort, visible from points where id = {} order by sort".format(line.id)
                self.pointlist = (q_run(connD, querry))

                self.id = str(line.id)
                self.clonebutton = tk.Button(self.detailframe, text="Clone device", command=self.clonedevice)
                self.clonebutton.grid(row=0, column=1)
                self.title = tk.Label(self.detailframe, text='Id: ' + str(self.id))
                self.title.grid(row=0, column=2)
                self.lab_name_l = tk.Label(self.detailframe, text="Name").grid(row=2, column=1)
                self.lab_name_e = tk.Entry(self.detailframe, width=50)
                self.lab_name_e.grid(row=2, column=2)
                self.lab_name_e.insert(0, str(line.name))

                self.lab_ct_name = tk.Label(self.detailframe, text="Crosstable name").grid(row=3, column=1)
                self.lab_ct = tk.Entry(self.detailframe, width=50)
                self.lab_ct.grid(row=3, column=2)
                self.lab_ct.insert(0, str(line.ctname))

                self.lab_model_l = tk.Label(self.detailframe, text="Model").grid(row=4, column=1)
                self.lab_model_e = tk.Button(self.detailframe, width=40, command=self.showmodelframe)
                self.lab_model_e.grid(row=4, column=2)
                self.lab_model_e.configure(text=str(line.model))
                self.lab_type_l = tk.Label(self.detailframe, text="Type").grid(row=5, column=1)
                self.lab_type_e = tk.Entry(self.detailframe, text="", width=50)
                self.lab_type_e.grid(row=5, column=2)
                self.lab_type_e.insert(0, str(line.type))
                self.lab_kw_l = tk.Label(self.detailframe, text="kW").grid(row=6, column=1)
                self.lab_kw_e = tk.Entry(self.detailframe, text="", width=50)
                self.lab_kw_e.grid(row=6, column=2)
                self.lab_kw_e.insert(0, str(line.kw))
                self.lab_rpm_l = tk.Label(self.detailframe, text="rpm").grid(row=7, column=1)
                self.lab_rpm_e = tk.Entry(self.detailframe, text="", width=50)
                self.lab_rpm_e.grid(row=7, column=2)
                self.lab_rpm_e.insert(0, str(line.rpm))
                self.lab_pms_l = tk.Label(self.detailframe, text="PMS").grid(row=8, column=1)
                self.lab_pms_e = tk.Entry(self.detailframe, text="", width=50)
                self.lab_pms_e.grid(row=8, column=2)
                self.lab_pms_e.insert(0, str(line.pms))
                self.lab_info_l = tk.Label(self.detailframe, text="Info").grid(row=9, column=1)
                self.lab_info_e = tk.Text(self.detailframe, width=38, height=10)
                self.lab_info_e.grid(row=9, column=2)
                self.lab_info_e.insert('1.0', str(line.info))
                self.lab_norm_l = tk.Label(self.detailframe, text="Standard").grid(row=10, column=1)

                self.standardlist = list(q_run(connD, "select standard,id from standards order by standard"))
                standards = column(self.standardlist, 0)

                self.lab_norm_e = ttk.Combobox(self.detailframe, text="", values=standards, width=45, state="readonly")
                self.lab_norm_e.bind('<<ComboboxSelected>>',changestandardetail)
                self.lab_norm_e.grid(row=10, column=2)
                try:
                    sidx = standards.index(str(line.norm))
                    self.lab_norm_e.current(sidx)
                except:
                    self.lab_norm_e.insert(0, 'Chose standard')

                # try:
                self.standarddetailsframe = tk.Frame(self.detailframe, height=2, bd=1, relief=SUNKEN)
                self.fillstandarddetailsframe(line.id)
                self.standarddetailsframe.grid(row = 11,column =1, columnspan = 2)
                # except:
                #     print('No standard')


                self.lab_drivenby_l = tk.Label(self.detailframe, text="Drivenby").grid(row=12, column=1)
                self.lab_drivenby_e = tk.Entry(self.detailframe, text="", width=50)
                self.lab_drivenby_e.grid(row=12, column=2)
                self.lab_drivenby_e.insert(0, str(line.drivenby))
                self.lab_meas_condition_l = tk.Label(self.detailframe, text="Meas condition").grid(row=13, column=1)
                self.lab_meas_condition_e = tk.Entry(self.detailframe, text="", width=50)
                self.lab_meas_condition_e.grid(row=13, column=2)
                self.lab_meas_condition_e.insert(0, str(line.meas_condition))
                self.lab_cm_l = tk.Label(self.detailframe, text="CM").grid(row=14, column=1)
                self.lab_cm_e = ttk.Combobox(self.detailframe, text="", values=["True", "False"], width=45,
                                             state="readonly")
                self.lab_cm_e.grid(row=14, column=2)

                sidx = ["True", "False"].index(str(line.cm))
                self.lab_cm_e.current(sidx)

                self.lab_interval_type_l = tk.Label(self.detailframe, text="Interval type").grid(row=15, column=1)
                self.lab_interval_type_e = ttk.Combobox(self.detailframe, text="",
                                                        values=["Day", "Week", "Month", "Year"], width=45,
                                                        state="readonly")
                self.lab_interval_type_e.grid(row=15, column=2)

                sidx = ["Day", "Week", "Month", "Year"].index(str(line.interval_type))
                self.lab_interval_type_e.current(sidx)

                self.lab_interval_length_l = tk.Label(self.detailframe, text="Interval_length").grid(row=16, column=1)
                self.lab_interval_length_e = tk.Entry(self.detailframe, text="", width=50)
                self.lab_interval_length_e.grid(row=16, column=2)
                self.lab_interval_length_e.insert(0, str(line.interval_length))

                self.ig_rem = tk.Label(self.detailframe, text="Ignore reminder always").grid(row=17, column=1)
                self.ig_rem_e = ttk.Combobox(self.detailframe, text="", values=["True", "False"], width=45,
                                             state="readonly")
                self.ig_rem_e.grid(row=17, column=2)
                if str(line.ignore_reminder).strip() == 'None': line.ignore_reminder = 'False'
                sidx = ["True", "False"].index(str(line.ignore_reminder))
                self.ig_rem_e.current(sidx)

                self.ig_rem_to = tk.Label(self.detailframe, text="Ignore reminder to").grid(row=18, column=1)
                self.ig_rem_to_e = tk.Entry(self.detailframe, text="", width=50)
                self.ig_rem_to_e.grid(row=18, column=2)
                self.ig_rem_to_e.insert(0, str(line.ignore_reminder_to))

                self.updatebut = tk.Button(self.detailframe, text="Update device data", command=self.updatedevice)
                self.updatebut.grid(row=19, column=2)

        def updatedevice(self):
            if str(self.lab_model_e.cget("text")) == 'None':
                model = ''
            else:
                model = self.lab_model_e.cget("text")

            interval = "{} {}".format(self.lab_interval_length_e.get(), self.lab_interval_type_e.get())

            if str(self.lab_kw_e.get()) == 'None':kw = '0'
            else: kw = self.lab_kw_e.get()

            if str(self.lab_drivenby_e.get()) == 'None':drivenby = '0'
            else: drivenby = self.lab_drivenby_e.get()

            ignorerminderto = self.ig_rem_to_e.get()
            if str(ignorerminderto) == 'None': ignorerminderto = 'Null'
            else: ignorerminderto = "'{}'".format(ignorerminderto)

            querry = """
            UPDATE devices 
            SET name = '{}', model = '{}', model_fkey = (select id from main_models where name = '{}' limit 1), type ='{}',
            kw = '{}', rpm = '{}', PMS = '{}', Info = '{}', norm = '{}', standard_fkey = (select id from standards where standard ='{}' limit 1),
            drivenby = '{}', meas_condition = '{}', cm = '{}', cbm_interval = '{}', ignore_reminder = {},ignore_reminder_to = {} where id = {}
            """.format(self.lab_name_e.get(), model, model, self.lab_type_e.get(), kw,
                  self.lab_rpm_e.get(), self.lab_pms_e.get(), \
                  self.lab_info_e.get("1.0",END), self.lab_norm_e.get(), self.lab_norm_e.get(), drivenby,
                  self.lab_meas_condition_e.get(), \
                  self.lab_cm_e.get(), interval,self.ig_rem_e.get(),ignorerminderto,self.id)
            q_run(self.connD,querry)

            querry = """select id from crosstable where id = {}""".format(self.id)
            if len(q_run(self.connD,querry)) == 0:
                querry = """INSERT INTO crosstable(parent,nameindevice,id) VALUES({},'{}',{})""".format(self.shipid,self.lab_ct.get(),self.id)
            else:
                querry = """UPDATE crosstable SET nameindevice = '{}' where id = {}""".format(self.lab_ct.get(),
                                                                                                self.id)
            q_run(self.connD, querry)
            self.reloadquerry(self.structuresort, self.shipid, self.connD,False)
        def __init__(self,parent,shipid,connD,selid,master):
            def getdetails(evt):
                w = evt.widget
                index = int(w.curselection()[0])
                tempdevname = w.get(index)
                devname, id = tempdevname.split('@')
                for widget in self.detailframe.winfo_children():
                    widget.destroy()
                for line in devlist:
                    self.makedeviceswindow(line,id,connD)

                try:
                    master.selid = id.strip()
                except:
                    master.selid = None
            self.master = master
            self.connD = connD
            self.shipid = shipid
            self.structuresort = True
            self.searchen = Entry(parent)
            self.searchen.pack(side = TOP, anchor = W)
            self.searchbutton = Button(parent,text = 'Search', command = lambda: self.searchinlist())
            self.searchbutton.pack(side = TOP, anchor = W)
            self.sortbutton = Button(parent,text = 'Change sort', command = lambda: self.reloadquerry(self.structuresort,shipid,connD,True))
            self.sortbutton.pack(side = TOP, anchor = W)
            self.sortbutton = Button(parent,text = 'Add device', command = lambda: devicetypechosewindow(self))#self.insertdevice())
            self.sortbutton.pack(side = TOP, anchor = W)

            self.deviceslistbox = Listbox(parent, exportselection=False)
            self.deviceslistbox.config(width=0)
            self.detailframe = Frame(parent)
            self.detailframe.pack(side=RIGHT, anchor=W, fill=BOTH, expand = 1)
            self.reloadquerry(self.structuresort,shipid,connD,False)
            self.deviceslistbox.bind('<Double-Button>', getdetails)

            if selid != None:
                self.loaddevices()
                for line in devlist:
                    self.makedeviceswindow(line, selid, connD)


            parent.pack(side=LEFT)
    class PointsFrame:
        def searchinlist(self):
            for i, listbox_entry in enumerate(self.deviceslistbox.get(0, END)):
                if str(self.searchen.get()).strip() != '':
                    listboxname = (listbox_entry).strip()
                    if str(self.searchen.get()).strip().upper() in str(listboxname).upper():
                        self.deviceslistbox.itemconfig(i, bg = 'green')
                    else:
                        self.deviceslistbox.itemconfig(i, bg='white')
                else:
                    self.deviceslistbox.itemconfig(i, bg='white')
        def AddPoint(self):

            querry = "select max(sort) from points where id = {}".format(self.devid)
            maxsort = list(q_run(self.connD, querry))[0][0]

            if str(maxsort).strip() =='None':	maxsort = 0

            querry = "insert into points(id,point,sort,visible) values ({},(select max(_id_)+1 from points),{}, True)".format(self.devid,maxsort+1)

            q_run(self.connD, querry)
            self.reloadquerry(self.structuresort, self.shipid, self.connD, False)
            self.makecontrols(self.devid, self.connD)
        def UploadPoints(self):
            testlist = list()
            testlist.clear()
            for i in self.CombPointList:
                testlist.append(i.cbox.get())
            if (any(testlist.count(x) > 1 for x in testlist)) == True:
                messagebox.showinfo("Brak", 'Uplooad aborted. Duplicate point names')
            else:

                querry = "select sort,_id_ from points where id = {} order by sort".format(self.devid)
                pointsort = q_run(self.connD, querry)
                ccp = 0
                for ax, line in pointsort:
                    ccp += 1
                    querry = "update points set sort = {} where _id_ = {}".format(ccp, line)
                    q_run(self.connD, querry)
                counter = -1
                for i in tqdm(self.CombPointList):
                    counter +=1
                    point = i.cbox.get()
                    bearing = self.CombBearingList[counter].showvalue
                    if str(bearing) == 'None': bearing = 'Null'
                    else:bearing = "'{}'".format(bearing)
                    seal = self.CombBearingSealList[counter].showvalue
                    if str(seal) == 'None': seal = 'Null'
                    else:seal = "'{}'".format(seal)
                    add = self.CombBearingAddList[counter].showvalue
                    if str(add) == 'None': add = 'Null'
                    else:add = "'{}'".format(add)
                    visible = self.CombVisibleList[counter].showvalue
                    if self.CombVisibleList[counter].showvalue == 'None':self.CombVisibleList[counter].showvalue = 'False'

                    try:
                        querry = "select point from points where sort = {} and id = {}".format( counter+1,self.devid)
                        temppoint = list(q_run(self.connD, querry))[0][0]
                        #print(querry)
                    except:
                        temppoint = 'NONE'

                    if temppoint != 'NONE':
                        querry = "update points set point = 'TEMPCHANGE' where point = '{}' and id = {}".format(point,self.devid)
                        q_run(self.connD, querry)
                        #print(querry)




                    querry = "update points set point = '{}',visible = '{}' where sort = {} and id = {}".format(point,self.CombVisibleList[counter].showvalue, counter+1,self.devid)
                    q_run(self.connD, querry)
                    #print(querry)



                    if temppoint != 'NONE':
                        querry = "update points set point = '{}' where point = 'TEMPCHANGE' and id = {}".format(temppoint,self.devid)
                        q_run(self.connD, querry)
                        #print(querry)


                    if point != i.showvalue:
                        querry = "update measurements_low set point = '{}' where point = '{}' and id = {}".format(point,i.showvalue,self.devid)
                        q_run(self.connD, querry)
                        #print(querry)
                    querry1 = "update bearings set bearing ={}, seal = {}, additional = {} where id = {} and point = '{}' " \
                             "returning bearing,seal,additional ".format(bearing,seal,add,self.devid,point)
                    updates = q_run(self.connD,querry1)
                    #print(querry1)
                    if len(updates) == 0:
                        querry = "INSERT INTO bearings (id,point,bearing,seal,additional)" \
                                 " VALUES ({},'{}',{},{},{}) ".format(self.devid,point,bearing,seal,add)
                        q_run(self.connD, querry)
                        #print(querry)
                    else:
                        querry = "update bearings set bearing ={}, seal = {}, additional = {} where id = {} and point = '{}' " \
                                  .format(bearing, seal, add, self.devid, point)
                        q_run(self.connD, querry)
                        #print(querry)
                self.reloadquerry(self.structuresort, self.shipid, self.connD,False)
                self.makecontrols(self.devid, self.connD)
        def DeletePoint(self):

            point = (self.CombPointList[len(self.CombPointList)-1].showvalue)
            querry = "select * from measurements_low where id = {} and point = '{}' ".format(self.devid,point)
            if len(q_run(self.connD,querry)) == 0:
                querry = "delete from points where id ={} and point = '{}'".format(self.devid,point)
                q_run(self.connD,querry)
                self.reloadquerry(self.structuresort, self.shipid, self.connD, False)
                self.makecontrols(self.devid, self.connD)
            else:
                messagebox.showinfo("Brak", 'Delete not aviable, there are measurements for point {}'.format(point))
        def reloadquerry(self, structuresort, shipid, connD,chagesort):
            if chagesort == False:
                if structuresort == True: structuresort = False
                else: structuresort = True
            if structuresort == True:
                querry = """select dev.id, name, pts.point, bea.bearing,bea.seal,bea.additional, pts.sort,pts.visible
                        from devices dev 
                        left join points pts on pts.id = dev.id
                        left join bearings bea on pts.id = bea.id and pts.point = bea.point
                        left join ds_structure dss on cast(dev.id as text) = dss.id
                        where dev.parent = {}
                        order by dev.name,pts.sort""".format(str(shipid))
                ans = q_run(connD, querry)

                self.structuresort = False
            else:
                querry = """select dev.id, name, pts.point, bea.bearing,bea.seal,bea.additional, pts.sort,pts.visible
                        from devices dev 
                        left join points pts on pts.id = dev.id
                        left join bearings bea on pts.id = bea.id and pts.point = bea.point
                        left join ds_structure dss on cast(dev.id as text) = dss.id
                        where dev.parent = {}
                            order by dss.sort,pts.sort""".format(str(shipid))
                ans = q_run(connD, querry)

                self.structuresort = True
            self.devdata = list()
            self.devdata.clear()
            for item in ans:
                self.devdata.append(item)

            self.loadpoints()
        def loadpoints(self):
            self.deviceslistbox.delete(0, END)
            checkdevlist = list()
            idlist = list()
            checkdevlist.clear()
            devlist.clear()

            for line in self.devdata:
                dev = device()
                dev.id = str(line[0])
                dev.name = str(line[1])
                dev.point = str(line[2])
                dev.bearing = str(line[3])
                dev.seal = str(line[4])
                dev.additional = str(line[5])
                dev.sort = str(line[6])
                dev.visible = str(line[7])
                devlist.append(dev)
                if line[1] not in checkdevlist:
                    self.deviceslistbox.insert(END,'{}@{}'.format(line[1],line[0]))
                    checkdevlist.append(line[1])
                    idlist.append(str(line[0]))
            self.deviceslistbox.pack(fill=BOTH, expand = 1)
            if str(self.master.selid) != 'None':
                try:
                    idx = idlist.index(self.master.selid)
                except:
                    print('No id', self.master.selid)
                    idx = 0
                self.deviceslistbox.select_set(idx)
                self.deviceslistbox.see(idx)
        def makecontrols(self,devid,connD):
            self.devid = devid
            querry = "select name from devices where id = '{}' and parent = {}".format(devid,self.shipid)
            devname = list(q_run(connD,querry))[0][0]

            self.devlabel.config(text='{}(ID:{})'.format(devname,self.devid))



            querry = "select point,visible from points where id ={} order by sort".format(self.devid)
            pointslist = column(list(q_run(connD,querry)),0)
            querry ="select bearing from bearings_freq group by bearing order by bearing"
            bearingslist = column(list(q_run(connD, querry)), 0)
            querry ="select seal from bearings_seals  group by seal order by seal"
            seallist = column(list(q_run(connD, querry)), 0)
            querry ="select add from bearings_add group by add order by add"
            addlist = column(list(q_run(connD, querry)), 0)
            visiblelist = ['True','False']

            for widget in self.detailframe.winfo_children():
                widget.destroy()
            self.CombPointList = list()
            self.CombPointList.clear()
            self.CombBearingList = list()
            self.CombBearingList.clear()
            self.CombBearingSealList = list()
            self.CombBearingSealList.clear()
            self.CombBearingAddList = list()
            self.CombBearingAddList.clear()
            self.CombVisibleList = list()
            self.CombVisibleList.clear()
            c=0
            self.uploadbutton = tk.Button(self.detailframe,text = 'Upload points', command = self.UploadPoints)
            self.uploadbutton.grid(row = c, column = 0)
            tk.Label(self.detailframe, text = 'Point').grid(row = c, column = 1)
            tk.Label(self.detailframe, text = 'Bearing').grid(row = c, column = 2)
            tk.Label(self.detailframe, text = 'Seal').grid(row = c, column = 3)
            tk.Label(self.detailframe, text = 'Additional').grid(row = c, column = 4)
            tk.Label(self.detailframe, text = 'Visible').grid(row = c, column = 5)
            if len(pointslist)!= 0:
                for line in devlist:

                    if str(line.name) == str(devname):

                        c+=1
                        self.namelab = tk.Label(self.detailframe, text=str(line.sort))
                        self.namelab.grid(row=c, column=0)
                        self.CombPointList.append(PointComboboxObject(self.detailframe,pointslist,c,self))
                        self.CombBearingList.append(BearingComboboxObject(self.detailframe,line.bearing, c,2, bearingslist))
                        self.CombBearingSealList.append(
                            BearingComboboxObject(self.detailframe, line.seal, c, 3, seallist))
                        self.CombBearingAddList.append(BearingComboboxObject(self.detailframe, line.additional, c,4, addlist))
                        self.CombVisibleList.append(BearingComboboxObject(self.detailframe, line.visible, c, 5, visiblelist))



            self.addbutton = tk.Button(self.detailframe, text='Add point', command = self.AddPoint)
            self.addbutton.grid(row=c+1, column=0)

            self.delbutton = tk.Button(self.detailframe, text='Delete point', command = self.DeletePoint)
            self.delbutton.grid(row=c+1, column=1)
        def __init__(self, parent, shipid, connD,selid,master):
            def getdetails(evt):
                w = evt.widget
                index = int(w.curselection()[0])
                tempdevname = w.get(index)
                devname,id= tempdevname.split('@')
                self.devname = devname
                self.makecontrols(id,connD)
                try:
                    master.selid = (tempdevname.split('@'))[1].strip()
                except:
                    master.selid = None
            self.master = master
            self.connD = connD
            self.shipid = shipid
            self.structuresort = True
            self.searchen = Entry(parent)
            self.searchen.pack(side=TOP, anchor=W)
            self.searchbutton = Button(parent, text='Search', command=lambda: self.searchinlist())
            self.searchbutton.pack(side=TOP, anchor=W)
            self.sortbutton = Button(parent,text = 'Change sort', command = lambda: self.reloadquerry(self.structuresort,shipid,connD,True))
            self.sortbutton.pack(side = TOP, anchor = W)
            self.deviceslistbox = Listbox(parent, exportselection=False)
            self.deviceslistbox.config(width=0)
            self.devdetailframe = Frame(parent,borderwidth = 1)
            self.devlabel = tk.Label(self.devdetailframe)
            self.devlabel.pack()
            self.devdetailframe.pack(side=TOP, anchor=N)
            self.detailframe = Frame(parent,borderwidth = 1)
            self.detailframe.pack(side=RIGHT, anchor=W, fill=BOTH, expand = 1)
            self.reloadquerry(self.structuresort, shipid, connD,True)
            self.deviceslistbox.bind('<Double-Button>',getdetails )

            if selid != None:
                self.makecontrols(selid,connD)


            parent.pack(side=LEFT)
    class StructFrame:
        def searchinlist(self):
            for i, listbox_entry in enumerate(self.deviceslistbox.get(0, END)):
                if str(self.searchen.get()).strip() != '':
                    listboxname = (listbox_entry[0:listbox_entry.rfind('@')]).strip()
                    if str(self.searchen.get()).strip().upper() in str(listboxname).upper():
                        self.deviceslistbox.itemconfig(i, bg = 'green')
                    else:
                        self.deviceslistbox.itemconfig(i, bg='white')
                else:
                    self.deviceslistbox.itemconfig(i, bg='white')
        def reloadquerrys(self,shipid,connD):
            querry = """
            select dss.id, dev.name,dss.sort from ds_structure dss 
            left join devices dev on cast(dev.id as text) = dss.id
            where dss.parent = {} order by dss.sort
            """.format(shipid)

            self.devlist = list(q_run(connD,querry))
            self.loaddevices()
        def loaddevices(self):
            idlist = list()
            for line in self.devlist:
                if str(line[1]) != 'None':
                    self.deviceslistbox.insert(END, '{}@{}'.format(line[1],line[0]) )
                else:
                    if str(line[2])[-5:] == '00.00':
                        self.deviceslistbox.insert(END, line[0])
                        self.deviceslistbox.itemconfig(END, fg='purple')
                    elif str(line[2])[-3:] == '.00':
                        self.deviceslistbox.insert(END, line[0])
                        self.deviceslistbox.itemconfig(END, fg='blue')
                idlist.append(line[0])
            self.deviceslistbox.pack(fill=BOTH, expand = 1)
            if str(self.master.selid) != 'None':
                try:
                    idx = idlist.index(self.master.selid)
                except:
                    print('No id', self.master.selid)
                    idx = 0
                self.deviceslistbox.select_set(idx)
                self.deviceslistbox.see(idx)

            savebutton = tk.Button(self.detailframe,text = 'Save structure')
            savebutton.config(command = self.savestruct)
            savebutton.pack(side=TOP, anchor=W)

            adddevicebutton = tk.Button(self.detailframe,text = 'Add device')
            adddevicebutton.config(command = self.adddevice)
            adddevicebutton.pack(side=TOP, anchor=W)

            addplaceebutton = tk.Button(self.detailframe,text = 'Add place')
            addplaceebutton.config(command = self.addplace)
            addplaceebutton.pack(side=TOP, anchor=W)

            addgroupbutton = tk.Button(self.detailframe,text = 'Add group')
            addgroupbutton.config(command = self.addgroup)
            addgroupbutton.pack(side=TOP, anchor=W)

            deletebutton = tk.Button(self.detailframe,text = 'Delete')
            deletebutton.config(command = self.delete)
            deletebutton.pack(side=TOP, anchor=W)
        def savestruct(self):
            class counter:
                def __init__(self):
                    self.lvl1 = 0
                    self.lvl2 = 0
                    self.lvl3 = 0
                def add(self,lvl):
                    if lvl == 1:
                        self.lvl1 += 1
                        self.lvl2 = 0
                        self.lvl3 = 0
                    if lvl == 2:
                        self.lvl2 += 1
                        self.lvl3 = 0
                    if lvl == 3:
                        self.lvl3 += 1

                    if len(str(self.lvl1)) == 1:strlvl1 = '0{}'.format(self.lvl1)
                    else:strlvl1 = str(self.lvl1)
                    if len(str(self.lvl2)) == 1:strlvl2 = '0{}'.format(self.lvl2)
                    else:strlvl2 = str(self.lvl2)
                    if len(str(self.lvl3)) == 1:strlvl3 = '0{}'.format(self.lvl3)
                    else:strlvl3 = str(self.lvl3)
                    cc = '{}.{}.{}'.format(strlvl1,strlvl2,strlvl3)
                    return cc
            i = -1
            dsstruct = list()
            dsstruct.clear()
            cc = counter()
            for item in enumerate(self.deviceslistbox.get(0, END)):
                i+=1
                color = self.deviceslistbox.itemcget(i, "fg")
                if str(color) == 'purple':
                    tup = [cc.add(1), item[1]]
                    dsstruct.append(tup)
                    pass
                elif str(color) == 'blue':
                    tup = [cc.add(2), item[1]]
                    dsstruct.append(tup)
                    pass
                else:
                    at = item[1].find('@')
                    tup = [cc.add(3), item[1][at+1:]]
                    dsstruct.append(tup)

            querry = "UPDATE ds_structure set parent = 999999 where parent = {}".format(self.shipid)
            q_run(self.connD, querry)
            try:
                for line in tqdm(dsstruct):
                    querry = "insert into ds_structure(parent,sort,id) values ({},'{}','{}')".format(self.shipid,line[0],line[1])
                    q_run(self.connD,querry)
                querry = "delete from ds_structure where parent = 999999"
                q_run(self.connD, querry)
            except:
                querry = "UPDATE ds_structure set parent = {} where parent = 999999".format(self.shipid)
                q_run(self.connD, querry)
        def adddevice(self):
            try:
                idx = self.deviceslistbox.curselection()[0]
            except:
                idx = 0
            chosedevicewindow(self.connD, self.shipid , self.deviceslistbox)
        def addplace(self):
            try:
                idx = self.deviceslistbox.curselection()[0]
            except:
                idx = 0
            place = simpledialog.askstring("Add place", "Enter place name:")
            self.deviceslistbox.insert(idx+1,  place)
            self.deviceslistbox.itemconfig(idx+1, fg='purple')
        def addgroup(self):
            try:
                idx = self.deviceslistbox.curselection()[0]
            except:
                idx = 0
            group = simpledialog.askstring("Add group", "Enter group name:")
            self.deviceslistbox.insert(idx+1, group)
            self.deviceslistbox.itemconfig(idx+1, fg='blue')
        def delete(self):
            try:
                idx = self.deviceslistbox.curselection()[0]
                self.deviceslistbox.delete(idx)
            except:
                idx = 0
        def changename(self,namestring,w,index):
            if '@' in namestring:
                nid = namestring.split('@')
                name = nid[0]
                id = nid[1]
            else:
                newname = simpledialog.askstring("Add device", "Device name:")
                if str(newname).strip() != 'None':
                    color = w.itemcget(index, 'fg')
                    w.delete(index)
                    w.insert(index, newname)
                    w.itemconfig(index, fg=color)

        def __init__(self,parent,shipid,connD,selid,master):
            def getdetails(evt):
                w = evt.widget
                index = int(w.curselection()[0])
                devname = w.get(index)
            def changename(evt):
                w = evt.widget
                index = int(w.curselection()[0])
                devname = w.get(index)
                self.changename(devname,w,index)
            def saveid(evt):
                w = evt.widget
                index = int(w.curselection()[0])
                devid= w.get(index)
                try:
                    master.selid = (devid.split('@'))[1]
                except:
                    master.selid = None
            self.master = master
            self.shipid = shipid
            self.connD= connD
            self.searchen = Entry(parent)
            self.searchen.pack(side=TOP, anchor=W)
            self.searchbutton = Button(parent, text='Search', command=lambda: self.searchinlist())
            self.searchbutton.pack(side=TOP, anchor=W)
            self.deviceslistbox = DragDropListbox(parent, exportselection=False)

            self.deviceslistbox.bind('<Double-Button-1>', changename)
            self.deviceslistbox.bind('<<ListboxSelect>>', saveid)
            self.deviceslistbox.config(width=0)
            self.detailframe = Frame(parent,borderwidth = 1)
            self.detailframe.pack(side=RIGHT, anchor=W, fill=BOTH, expand = 1)
            self.reloadquerrys(shipid,connD)
    class RightClick_Owners:
        def __init__(self, master,mframe):
            self.mframe = mframe
            self.master = master
            self.aMenu = Menu(master, tearoff=0)
            self.aMenu.add_command(label='Add owner', command=self.addowner)
            self.aMenu.add_command(label='Add ship', command=self.addship)
            self.tree_item = ''
        def addowner(self):
            ownername = simpledialog.askstring("Add owner:", "Enter owner name:")
            if str(ownername).strip() != '' and str(ownername).strip() != 'None':
                querry ="insert into main(parent,name) values(1,'{}')".format(ownername)
                q_run(self.mframe.connD,querry)
                self.mframe.putowners(self.mframe.Ownerlistbox)
        def addship(self):
            index = int(self.master.curselection()[0])
            ownername = self.master.get(index)
            shipname = simpledialog.askstring("Add ship", "Enter ship name for {} :".format(ownername))
            if str(shipname).strip() != '' and str(shipname).strip() != 'None':
                querry = """insert into main (parent,name,reporttype) 
                values((select id from main where name = '{}' limit 1),'{}',1)
                """.format(ownername,shipname)
                q_run(self.mframe.connD,querry)
                self.mframe.makeships(ownername)
        def popup(self, event):
            self.aMenu.post(event.x_root, event.y_root)
    class RightClick_Apps:
        def __init__(self, master, mframe):
            self.mframe = mframe
            self.master = master
            self.aMenu = Menu(master, tearoff=0)
            self.aMenu.add_command(label='Load struct from file', command=self.loadstruct)
            self.tree_item = ''
        def loadstructfromfile(self,shipid,connD,new):
            if new == True:
                lvl = '01'
            if new == False:
                querry = "select sort from ds_structure where parent = {} order by sort desc limit 1".format(shipid)
                maxsort = list(q_run(connD,querry))[0][0]
                maxlvl1sort = maxsort[:maxsort.index('.')]
                if len(str(int(maxlvl1sort) + 1)) == 1:
                    lvl = '0{}'.format(str(int(maxlvl1sort) + 1))
                else:
                    lvl = (str(int(maxlvl1sort) + 1))

            Tk().withdraw()
            file = filedialog.askopenfilename()
            devicesdataframe = pd.DataFrame(columns=['Nameinroute', 'Name', 'tempid', 'sort'])
            pointsdataframe = pd.DataFrame(columns=['devid', 'pointname', 'sort'])
            with open(file, newline='') as csvfile:
                spamreader = list(csv.reader(csvfile, delimiter='\t'))
                lc = -1
                tid = 1
                for row in spamreader:
                    lc += 1
                    if str(spamreader[lc][0]) == 'eDataIdLocation' and str(spamreader[lc][1]) == 'eTypeMachine':
                        pc = 1
                        if len(str(tid)) == 1:
                            stid = '0{}'.format(tid)
                        else:
                            stid = tid
                        sortct = '{}.01.{}'.format(lvl,stid)
                        devicesdataframe = devicesdataframe.append(
                            {'Nameinroute': spamreader[lc][2], 'Name': spamreader[lc][2], 'tempid': tid,
                             'sort': sortct}, ignore_index=True)

                        sortc = 1
                        while str(spamreader[lc + pc][1]) != 'eTypeMachine':
                            if (lc + pc) >= len(spamreader) - 1: break
                            if str(spamreader[lc + pc][0]) == 'eDataIdLocation' and str(
                                    spamreader[lc + pc][1]) == 'eTypePoint':
                                pointsdataframe = pointsdataframe.append(
                                    {'pointname': spamreader[lc + pc][2], 'devid': tid, 'sort': sortc},
                                    ignore_index=True)
                                sortc += 1
                            pc += 1
                        tid += 1
            MsgBox = tk.messagebox.askquestion('Crosstable',
                                               'Do you have crosstable file?(format xls, Column 1 - name in device, Column 2 - correct name)',
                                               icon='warning')
            if MsgBox == 'yes':
                Tk().withdraw()
                ctfile = filedialog.askopenfilename()
                workbook = xlrd.open_workbook(ctfile)
                worksheet = workbook.sheet_by_index(0)
                for row in range(worksheet.nrows):
                    devicesdataframe['Name'] = devicesdataframe['Name'].replace(worksheet.cell(row, 0).value,
                                                                                worksheet.cell(row, 1).value)
            else:
                pass
            querry = "insert into ds_structure (parent,id,sort) values({},'PLACE','{}.00.00');insert into ds_structure (parent,id,sort) values({},'GROUP','{}.01.00')".format(
                shipid, lvl, shipid, lvl)
            q_run(connD, querry)
            for line in tqdm(devicesdataframe.values):
                querry = "insert into devices (parent,name) values ({},'{}')".format(shipid, line[1])
                q_run(connD, querry)
                querry = "select max(id) from devices"
                newid = list(q_run(connD, querry))[0][0]
                querry = "insert into ds_structure (parent,id,sort) values({},'{}','{}'); insert into crosstable (parent,id,nameindevice) values({},'{}','{}')".format(
                    shipid, newid, line[3], shipid, newid, line[0])
                q_run(connD, querry)
                pointsedited = pointsdataframe.loc[pointsdataframe.devid == line[2]]
                pointsedited.loc[:, 'devid'].replace(line[2], newid, inplace=True)
                for line2 in pointsedited.values:
                    querry = "insert into points(id,point,sort,visible) values ({},'{}',{},'True')".format(line2[0],
                                                                                                           line2[1],
                                                                                                           line2[2])
                    q_run(connD, querry)
        def loadstruct(self):
            querry = "select * from ds_structure where parent = {}".format(self.mframe.shipid)
            try:
                if (len(list(q_run(self.mframe.connD,querry)))) == 0 :
                    self.loadstructfromfile(self.mframe.shipid,self.mframe.connD,True)
                else:
                    MsgBox = tk.messagebox.askquestion('Crosstable',
                                                       'Structure for that ship exists. Do you want to add new devices?',
                                                       icon='warning')
                    if MsgBox == 'yes':
                        self.loadstructfromfile(self.mframe.shipid, self.mframe.connD,False)
                messagebox.showinfo("Done", 'Upload done')
            except:
                messagebox.showinfo("Error", 'Upload error')
        def popup(self, event):
            self.aMenu.post(event.x_root, event.y_root)

    class RightClick_Ships:
        def __init__(self, master, mframe):
            self.mframe = mframe
            self.master = master
            self.index = '0'
            self.aMenu = Menu(master, tearoff=0)
            self.aMenu.add_command(label='Set CBM on', command=lambda: self.cmbon(self.index))
            self.aMenu.add_command(label='Set CBM off', command=lambda: self.cbmoff(self.index))
            self.tree_item = ''

        def cmbon(self,_id):
            query = """UPDATE main set cbm = True where id = {}""".format(self.mframe.ships[_id][1])
            self.mframe.Shiplistbox.itemconfig(_id, bg='green')
            q_run(self.mframe.connD, query)

        def cbmoff(self,_id):
            query = """UPDATE main set cbm = False where id = {}""".format(self.mframe.ships[_id][1])
            self.mframe.Shiplistbox.itemconfig(_id, bg='white')
            q_run(self.mframe.connD, query)


        def popup(self, event):
            w = event.widget
            self.index = int(w.curselection()[0])

            self.aMenu.post(event.x_root, event.y_root)

    def putowners(self,owlbox):
        owlbox.delete(0, END)
        querry = "select name,id from main where parent = 1 order by name"
        resultrr = q_run(self.connD, querry)
        for line in resultrr:
            owlbox.insert(END, line[0])
    def makeships(self,shipname):
        querry = "select name,id,cbm from main where parent =(select id from main where name = '" + str(
            shipname) + "' limit 1) order by name"

        self.ships = q_run(self.connD, querry)
        self.Shiplistbox.delete(0, 'end')
        for line in self.ships:
            self.Shiplistbox.insert(END, '{}(ID:{})'.format(line[0],line[1]))
            if str(line[2]) == 'True':
                self.Shiplistbox.itemconfig(END, bg='green')
    def __init__(self,connD,selid):
        def getships(evt):
            w = evt.widget
            index = int(w.curselection()[0])
            shipname = w.get(index)
            self.Applistbox.delete(0, 'end')
            self.Shiplistbox.delete(0, 'end')
            for widget in self.Workframe.winfo_children():
                widget.destroy()
            self.makeships(shipname)
        def getaps(evt):
            w = evt.widget
            index = int(w.curselection()[0])

            tempname = w.get(index)
            shipname = tempname[0:str(tempname).rfind('(ID:')]


            self.Applistbox.delete(0, 'end')
            for widget in self.Workframe.winfo_children():
                widget.destroy()

            querry = "(select id from main where name = '{}')".format(str(shipname))
            self.shipid = list(q_run(connD, querry))[0][0]
            self.Applistbox.delete(0, 'end')
            #self.Applistbox.insert(END, 'Crosstable')
            self.Applistbox.insert(END, 'Devices')
            self.Applistbox.insert(END, 'Points')
            self.Applistbox.insert(END, 'Structure')
        def makeframe(evt):
            w = evt.widget
            index = int(w.curselection()[0])
            framename = w.get(index)
            for widget in self.Workframe.winfo_children():
                widget.destroy()
            if str(framename) == 'Crosstable':
                self.CrosstableFrame(self.Workframe, self.shipid, connD)
            elif str(framename) == 'Devices':
                self.DevicesFrame(self.Workframe,self.shipid,connD,self.selid,self)
            elif str(framename) == 'Points':
                self.PointsFrame(self.Workframe, self.shipid, connD,self.selid,self)
            elif str(framename) == 'Structure':
                self.StructFrame(self.Workframe,self.shipid, connD,self.selid,self)
        self.selid = selid
        self.connD = connD
        self.shipid = ''
        self.stWindow = tk.Tk()
        self.stWindow.title("Structure")
        self.Ownerlistbox = Listbox(self.stWindow, exportselection=False)
        self.Ownerlistbox.config(width=0)
        self.Ownerlistbox.bind('<Double-Button>', getships)
        self.Ownerlistbox.bind('<Button-3>', self.RightClick_Owners(self.Ownerlistbox,self).popup)
        self.Shiplistbox = Listbox(self.stWindow, exportselection=False)
        self.Shiplistbox.config(width=0)
        self.shipid = ''
        self.Shiplistbox.bind('<Double-Button>', getaps)
        self.Shiplistbox.bind('<Button-3>', self.RightClick_Ships(self.Shiplistbox, self).popup)
        self.Applistbox = Listbox(self.stWindow, exportselection=False)
        self.Applistbox.config(width=0)
        self.Applistbox.bind('<Double-Button>',makeframe)
        self.Workframe = Frame(self.stWindow, borderwidth = 1)
        self.putowners(self.Ownerlistbox)
        self.Ownerlistbox.pack(side=LEFT, fill=BOTH)
        self.Shiplistbox.pack(side=LEFT, fill=BOTH)
        self.Applistbox.pack(side=LEFT, fill=BOTH)
        self.Applistbox.bind('<Button-3>', self.RightClick_Apps(self.Applistbox, self).popup)
        self.Workframe.pack(side=LEFT, fill=BOTH)
        self.stWindow.mainloop()



LogApplication()

