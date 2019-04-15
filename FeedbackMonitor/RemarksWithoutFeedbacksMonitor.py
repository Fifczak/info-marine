from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk

# from ttk import *
from pathlib import Path
import psycopg2
import csv

host = '192.168.8.125'
username = 'filipb'
password = '@infomarine'
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


#
def nofdblistF():


    querry = """ select rem.id, dev.name, rem.raport_number, main.name,main.id,rem.remark
	from remarks as rem
	left join feedbacks as fdb on rem.id = fdb.id and rem.raport_number = fdb.raport_number
	left join devices as dev on rem.id = dev.id
	left join main as main on dev.parent = main.id
	where rem.sended = True and fdb.feedback is null and dev.name is not null
	group by  rem.id , dev.name, rem.raport_number,main.name,rem.name,main.id,rem.remark  order by main.name,rem.raport_number,rem.name  """
    nofdblist = q_run(connD, querry)




    # DO WYZUCENIA PO TESTACH
    with open('C:\Overmind\Sent remarks without feedbacks.csv', 'w', newline='') as file:
        for l in nofdblist:
            file.write(str(l))
            file.write('\n')




    return list(nofdblist)


def ShipsApplication(nofdblist):
    def LoadRaportList(shipid):
        class frame_rem:
            def __init__(self, measCframe, devname, rn, id, parent,remarkstr):
                self.parent = parent
                self.rn = rn
                self.id = id
                self.name = tk.Label(measCframe, text=str(devname))
                self.remarkfield = tk.Text(measCframe, width=50, height=5)
                self.remarkfield.insert(INSERT,remarkstr)
                self.textfield = tk.Text(measCframe, width=50, height=5)
                self.name.pack(side=LEFT)
                self.remarkfield.pack(side=LEFT)
                self.textfield.pack(side=LEFT)
                self.var = tk.IntVar()
                self.check = ttk.Checkbutton(measCframe, text='Not sent', variable = self.var)
                self.check.pack(side=LEFT)
                self.var2 = tk.IntVar()
                self.check2 = ttk.Checkbutton(measCframe, text='No remark', variable = self.var2)
                self.check2.pack(side=LEFT)



                measCframe.pack(side=TOP, fill=tk.BOTH, expand=True)

        def selectreport(evt):
            def upload():
                for line in remlist:
                    if line.textfield.get("1.0", END).strip() != '':

                        try:
                            querry = "select date from measurements_low where id = " + str(
                                line.id) + " and raport_number = '" + str(line.rn) + "' limit 1"

                            measdate = str(q_run(connD, querry)[0][0])

                            querry = "INSERT INTO FEEDBACKS(id,raport_number,feedback,parent,documentdate) VALUES (" + str(
                                line.id) + ",'" + str(line.rn) + "','" + str(
                                (line.textfield.get("1.0", END)).strip()) + "'," + str(line.parent) + ",'" + str(
                                measdate) + "')"

                            q_run(connD, querry)
                        except:
                            querry = "INSERT INTO FEEDBACKS(id,raport_number,feedback,parent) VALUES (" + str(
                                line.id) + ",'" + str(line.rn) + "','" + str(
                                (line.textfield.get("1.0", END)).strip()) + "'," + str(line.parent) +  ")"
                            q_run(connD, querry)

                    if line.var.get() == 1:
                        querry = "UPDATE remarks SET sended = False where id = '" +str(line.id)+"' and raport_number = '" +str(line.rn)+ "'"
                        q_run(connD, querry)

                    if line.var2.get() == 1:
                        querry = "DELETE FROM remarks WHERE id = '" + str(
                            line.id) + "' and raport_number = '" + str(line.rn) + "'"
                        q_run(connD, querry)



                root2.destroy()
                ShipsApplication(nofdblistF())

            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)
            nrrap = RapList[index]

            ###
            devices = list()
            chList = list()
            for line in nofdblist:
                if str(line[2]).strip() == str(nrrap):
                    if line[1] not in chList:
                        chList.append(line[1])
                        strip = [line[1], line[2], line[0], line[4],line[5]]
                        devices.append(strip)

            try:
                for widget in measBframe.winfo_children():
                    widget.destroy()
            except:
                pass
            MASTERmeasframe.pack(side=TOP, anchor=S)
            measBframe.pack(side=TOP)

            UploadButton = Button(measBframe, text='Upload and refresh', command=upload)
            UploadButton.pack()
            remlist = list()
            backRemList = list()
            for i in devices:
                measCframe = tk.Frame(measBframe, height=2, bd=1, relief=SUNKEN)
                X = frame_rem(measCframe, i[0], i[1], i[2], i[3],i[4])
                # X = make_frame_rem(measCframe,i)
                remlist.append(X)

        RapList = list()
        for line in nofdblist:
            if str(line[4]).strip() == str(shipid).strip():
                if str(line[2]) not in RapList:
                    RapList.append(line[2])

        RapList.sort()
        Raportlist.delete(0, END)
        for line in RapList:
            Raportlist.insert(END, line)
        Raportlist.bind('<<ListboxSelect>>', selectreport)

    def LoadShipsList():
        def selectship(evt):
            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)
            id_ = shList[index][1]
            LoadRaportList(id_)
            Raportlist.pack(side=LEFT, anchor=N)

        shList = list()
        tryList = list()
        for line in nofdblist:
            if str(line[3]) not in tryList:
                tryList.append(str(line[3]))
                strip = [line[3], line[4]]
                shList.append(strip)
        shList.sort()
        for line in shList:
            Shiplist.insert(END, line[0])
        Shiplist.bind('<Double-Button>', selectship)

    root2 = Tk()
    root2.title("Remarks")

    Shiplist = tk.Listbox(root2)
    Shiplist.config(width=20)
    Shiplist.pack(side=LEFT, anchor=N)

    Raportlist = tk.Listbox(root2)
    Raportlist.config(width=15)

    LoadShipsList()

    MASTERmeasframe = Frame(root2, width=300, height=300)

    measBframe = Canvas(MASTERmeasframe)  # ,yscrollcommand=rapmeasscrol.set,scrollregion=(0,0,500,500))

    root2.mainloop()



ShipsApplication(nofdblistF())