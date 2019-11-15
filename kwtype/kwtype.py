import psycopg2
import tkinter as tk
import tkinter.ttk as ttk
from tqdm import tqdm
import pandas.io.sql as sqlio
import pandas as pd
import numpy as np
import csv

def q_run(connD, querry):
    username = connD[0]
    password = connD[1]
    host = connD[2]
    kport = "5432"
    kdb = "postgres"
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
        self.root = tk.Tk()
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
        self.var = tk.IntVar()
        self.checksave = tk.Checkbutton(self.root, text="Remember", variable=self.var)
        self.checksave.grid(row=3, column=2)
        self.sign_in_butt = tk.Button(self.root, text="Sign In", command=lambda ue=self.user_entry, pe=self.pass_entry: self.logging_in(ue, pe))
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
            kw_type_window(connD)


class kw_type_window:
    def __init__(self,connD):

        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)
        pd.set_option('max_colwidth', -1)
        self.connD = connD
        self.conn = psycopg2.connect(
            "host='{}' port={} dbname='{}' user={} password={}".format(connD[2], '5432', 'postgres', connD[0], connD[1]))
        self.maindframe = self.loadmainquerry()
        self.makerlist = self.getmakers()

        mainwindow = tk.Tk()
        mainwindow.title("Fast kw and type check")
        mainframe = tk.Frame(mainwindow, bd=1, relief=tk.SUNKEN)

        self.filterlisboxtype = ttk.Combobox(mainframe, text="",
                                                width =50,
                                             state="readonly")
        self.devleftlabel = tk.Label(mainframe,text = 'Left: {}(on ship: XX)'.format(self.maindframe['shipname'].size))
        self.deviceslist = ttk.Treeview(mainframe,height = 40)
        self.deviceslist["columns"] = ("device", "maker", "newmomodel",'newtype', "oldmodel",'oldtype','kW')


        self.devicelabel = tk.Label(mainframe, text = "DEVICENAME")
        self.idlabel = tk.Label(mainframe, text = "ID")

        self.makercbox = ttk.Combobox(mainframe, text="",
                                             width=30,
                                             state="readonly")

        self.modelcbox = ttk.Combobox(mainframe, text="",
                                      width=30,
                                      state="readonly")

        self.typelabel = tk.Label(mainframe, text="TYPE")
        self.kwentry = tk.Text(mainframe, width = 6, height = 1)
        self.updatebutton = tk.Button(mainframe, text = "Update", width = 10, height = 5, command = self.updatedevice)


        self.congigurewidgets()

        self.widgetsgridmanager(mainframe)
        mainwindow.mainloop()

    def updatedevice(self):
        ix = [self.modelcbox.current()][0]
        modelid = (column(self.modellist, 0))[ix]


        maker = self.makercbox.get()
        model = (column(self.modellist, 1))[ix]
        _type = (column(self.modellist, 2))[ix]

        kw = self.kwentry.get("1.0",tk.END).strip()
        devid = self.idlabel.cget("text")

        query = "UPDATE devices set model_fkey = {}, kw = '{}' where id = {} ".format(modelid,kw,devid)
        q_run(self.connD,query)

        test  = self.maindframe.loc[self.maindframe['devid'] == devid]
        idx  = test.index[0]

        self.maindframe.at[idx,'maker'] = maker
        self.maindframe.at[idx, 'newmodel'] =  model
        self.maindframe.at[idx, 'newtype'] =  _type
        self.maindframe.at[idx, 'kw'] =  kw
        shipname = self.filterlisboxtype.get()
        self.updatewidgets(shipname)


    def congigurewidgets(self):
        'Method to start configure widgets'
        def cbsel(evt):
            shipname = evt.widget.get()
            self.updatewidgets(shipname)

        def makerscbsel(evt):
            cbindex = evt.widget.current()
            self.modellist = (self.getmodels(self.makerlist[cbindex][0]))
            self.modelcbox.configure(values=column(self.modellist, 1))

            try:
                self.modelcbox.current(0)
                self.typelabel.configure(text=column(self.modellist, 2)[0])
            except:
                print('No models on that maker')

        def modelcbsel(evt):
            cbindex = evt.widget.current()
            self.typelabel.configure(text=column(self.modellist, 2)[cbindex])

        def deviceclick(evt):
            self.device_details_label(self.deviceslist.item(self.deviceslist.focus()))



        self.filterlisboxtype.bind("<<ComboboxSelected>>", cbsel)
        self.filterlisboxtype.configure(values = self.maindframe['shipname'].unique().tolist())


        self.deviceslist.heading("#0", text = 'IMID',anchor=tk.W)
        self.deviceslist.column("#0", width=60, minwidth=60, stretch=tk.NO)

        self.deviceslist.heading("device", text = 'device',anchor=tk.W)
        self.deviceslist.column("device", width=200, minwidth=50, stretch=tk.NO)

        self.deviceslist.heading("maker", text = 'maker' ,anchor=tk.W)
        self.deviceslist.column("maker", width=200, minwidth=50, stretch=tk.NO)

        self.deviceslist.heading("newmomodel", text = 'newmomodel',anchor=tk.W)
        self.deviceslist.column("newmomodel", width=100, minwidth=50, stretch=tk.NO)

        self.deviceslist.heading("oldmodel", text = 'oldmodel',anchor=tk.W)
        self.deviceslist.column("oldmodel", width=100, minwidth=50, stretch=tk.NO)
        #self.deviceslist.column("oldmodel", width=100, minwidth=50, stretch=tk.NO)


        self.deviceslist.heading("oldtype", text = 'oldtype',anchor=tk.W)
        self.deviceslist.column("oldtype", width=100, minwidth=50, stretch=tk.NO)

        self.deviceslist.heading("newtype", text = 'newtype',anchor=tk.W)
        self.deviceslist.column("newtype", width=100, minwidth=50, stretch=tk.NO)


        self.deviceslist.heading("kW", text = 'kW',anchor=tk.W)
        self.deviceslist.column("kW", width=100, minwidth=50, stretch=tk.NO)

        self.makercbox.configure(values = column(self.makerlist,1))
        self.modelcbox.bind("<<ComboboxSelected>>", modelcbsel)

        self.makercbox.bind("<<ComboboxSelected>>", makerscbsel)

        self.deviceslist.bind("<<TreeviewSelect>>", deviceclick)

    def updatewidgets(self,shipname):
        'Ubdate widgets and data'
        self.deviceslist.delete(*self.deviceslist.get_children())
        self.tempdframe = self.maindframe[self.maindframe['shipname'] == shipname]
        self.devleftlabel.configure(text = 'Left: {}(on ship: {})'.format(self.maindframe['shipname'].size,self.tempdframe['shipname'].size))
        for line in self.tempdframe.values:
            self.deviceslist.insert('', 'end', text=line[0], values=(line[2], line[3], line[4], line[7], line[5], line[6],line[8]))


    def widgetsgridmanager(self,mainframe):
        'Grid manager for widgets'
        mainframe.pack(expand = True, fill = tk.BOTH)

        self.filterlisboxtype.grid(row = 0, column = 0, columnspan = 5)
        self.devleftlabel.grid(row=1, column=1,columnspan = 2)
        self.deviceslist.grid(row = 2, column = 0, columnspan = 5, padx = 50)
        self.devicelabel.grid(row = 3,column = 0)
        self.idlabel.grid(row=3, column=1)
        self.updatebutton.grid(row = 4, column = 2, rowspan = 5)
        tk.Label(mainframe, text="Maker:").grid(row = 4, column = 0)
        self.makercbox.grid(row = 4, column = 1)
        tk.Label(mainframe, text="Maker:").grid(row=5, column=0)
        self.modelcbox.grid(row = 5, column = 1)
        tk.Label(mainframe, text="Type:").grid(row=6, column=0)
        self.typelabel.grid(row = 6, column = 1)
        tk.Label(mainframe, text="kW:").grid(row=7, column=0)
        self.kwentry.grid(row = 7, column = 1)

    def loadmainquerry(self):
        'Method to load missing elements querry'
        querry = """
        select dev.id as devid,main.name as shipname,dev.name as devname, mm2.name as maker, mm.name as newmodel,dev.model as oldmodel,
        dev.type as oldtype, mm.type as newtype, dev.kw
        from devices dev
        left join main on dev.parent = main.id
        left join main_models mm on dev.model_fkey = mm.id
        left join main_models mm2 on mm.parent = mm2.id
        where (mm2.name is null or mm.name is null or mm.type is null or dev.kw is null) and main.cbm = True
        order by main.name, dev.id
        """

        return sqlio.read_sql_query(querry, self.conn)


    def getmakers(self):
        querry = "select id,name from main_models where parent is null order by name"
        return list(q_run(self.connD,querry))

    def getmodels(self,parentid):
        querry = "select id, name ,type from main_models where parent = {} order by name".format(parentid)
        return list(q_run(self.connD,querry))


    def device_details_label(self,devdict):
        self.idlabel.configure(text=(devdict['text']))
        self.devicelabel.configure(text=(devdict['values'][0]))
        self.kwentry.delete("1.0",tk.END)
        self.kwentry.insert(tk.INSERT,devdict['values'][6])
        # print(devdict['text'])
        # print(devdict['values'][0])



if __name__ == '__main__':
    LogApplication()