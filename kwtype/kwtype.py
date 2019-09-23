import psycopg2
import tkinter as tk
import tkinter.ttk as ttk
from tqdm import tqdm
import pandas.io.sql as sqlio
import pandas as pd
import numpy as np

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



class kw_type_window:
    def __init__(self,connD):
        print('init')
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
        self.deviceslist["columns"] = ("device", "maker", "newmomodel", "oldmodel",'newtype','oldtype','kW')

        self.devicelabel = tk.Label(mainframe, text = "DEVICENAME")


        self.makercbox = ttk.Combobox(mainframe, text="",
                                             width=30,
                                             state="readonly")

        self.modelcbox = ttk.Combobox(mainframe, text="",
                                      width=30,
                                      state="readonly")

        self.typelabel = tk.Label(mainframe, text="TYPE")




        self.congigurewidgets()

        self.widgetsgridmanager(mainframe)





        mainwindow.mainloop()


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

        self.deviceslist.heading("newtype", text = 'newtype',anchor=tk.W)
        self.deviceslist.column("newtype", width=100, minwidth=50, stretch=tk.NO)

        self.deviceslist.heading("oldtype", text = 'oldtype',anchor=tk.W)
        self.deviceslist.column("oldtype", width=100, minwidth=50, stretch=tk.NO)

        self.deviceslist.heading("kW", text = 'kW',anchor=tk.W)
        self.deviceslist.column("kW", width=100, minwidth=50, stretch=tk.NO)

        self.makercbox.configure(values = column(self.makerlist,1))
        self.modelcbox.bind("<<ComboboxSelected>>", modelcbsel)

        self.makercbox.bind("<<ComboboxSelected>>", makerscbsel)


    def updatewidgets(self,shipname):
        'Ubdate widgets and data'
        self.deviceslist.delete(*self.deviceslist.get_children())
        self.tempdframe = self.maindframe[self.maindframe['shipname'] == shipname]
        self.devleftlabel.configure(text = 'Left: {}(on ship: {})'.format(self.maindframe['shipname'].size,self.tempdframe['shipname'].size))
        print(self.tempdframe)
        for line in self.tempdframe.values:
            self.deviceslist.insert('', 'end', text=line[0], values=(line[2], line[3], line[4], line[5], line[7], line[6],line[8]))


    def widgetsgridmanager(self,mainframe):
        'Grid manager for widgets'
        mainframe.pack(expand = True, fill = tk.BOTH)

        self.filterlisboxtype.grid(row = 0, column = 0, columnspan = 5)
        self.devleftlabel.grid(row=1, column=1,columnspan = 2)
        self.deviceslist.grid(row = 2, column = 0, columnspan = 5, padx = 50)
        self.devicelabel.grid(row = 3,column = 0)
        self.makercbox.grid(row = 3, column = 1)
        self.modelcbox.grid(row = 3, column = 2)
        self.typelabel.grid(row = 3, column = 3)

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
        return list(q_run(connD,querry))

    def getmodels(self,parentid):
        querry = "select id, name ,type from main_models where parent = {} order by name".format(parentid)
        return list(q_run(connD,querry))






if __name__ == '__main__':
    connD = ['testuser','info','192.168.10.243']
    kw_type_window(connD)