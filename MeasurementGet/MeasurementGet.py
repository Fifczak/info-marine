import psycopg2
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
import os
import os.path
import time
import numpy as np
import decimal
ctx = decimal.Context()
ctx.prec = 20
def float_to_str(f):
    """
    Convert the given float to a string,
    without resorting to scientific notation
    """
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')
username = 'testuser'
password = 'testuser'
host = '192.168.8.125'
connBASE = [username,password,host]
connTARGET = ['dbadmin','242QhpbS&9Fv','192.168.10.243']
#connTARGET = ['testuser','testuser','192.168.10.243']





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








def runmove():


    print(str(pw_new_in.get()))
    pbars = Tk()
    pbars.title("Rescuer")
    # ML
    labML = tk.Label(pbars, text="Measurements low").grid(row=0, column=0)
    MLVar = StringVar()
    MLVar.set('XXXXXX')
    countML = tk.Label(pbars, textvariable=MLVar).grid(row=0, column=1)
    MLProgress_bar = ttk.Progressbar(pbars, orient='horizontal', lengt=300, mode='determinate')

    # COPY
    labCOPYCHARTS = tk.Label(pbars, text="Copy Charts").grid(row=1, column=0)
    COPYCHARTSVar = StringVar()
    COPYCHARTSVar.set('XXXXXXXXX')
    countCOPYCHARTS= tk.Label(pbars, textvariable=COPYCHARTSVar).grid(row=1, column=1)
    COPYCHARTSProgress_bar = ttk.Progressbar(pbars, orient='horizontal', lengt=300, mode='determinate')

    # CONVERT
    labCONVERTCHARTS = tk.Label(pbars, text="Convert old charts").grid(row=2, column=0)
    CONVERTCHARTSVar = StringVar()
    CONVERTCHARTSVar.set('XXXXXXXXXX')
    countCONVERTCHARTS = tk.Label(pbars, textvariable=CONVERTCHARTSVar).grid(row=2, column=1)
    CONVERTCHARTSProgress_bar = ttk.Progressbar(pbars, orient='horizontal', lengt=300, mode='determinate')

    class measurements_low(object):
        def __init__(self):
            self.parent = list()
            self.id = list()
            self.point = list()
            self.raport_number = list()
            self.date = list()
            self.value = list()
            self.type = list()
            self.unit = list()

            def getVals(self):
                c = -1
                querryGET = "select parent, id, point, raport_number, date, value, type, unit from measurements_low where parent = " + str(pw_new_in.get())
                table = q_run(connBASE, querryGET)
                MLProgress_bar['maximum'] = len(table)
                MLProgress_bar.grid(row=0, column=2)
                for line in table:
                    c += 1
                    MLVar.set(str(c + 1) + ' / ' + str(len(table)))
                    MLProgress_bar['value'] = c + 1
                    MLProgress_bar.update()
                    if str(line[0]) == 'None':
                        self.parent.append('Null')
                    else:
                        self.parent.append("'" + str(line[0]) + "'")
                    if str(line[1]) == 'None':
                        self.id.append('Null')
                    else:
                        self.id.append("'" + str(line[1]) + "'")
                    if str(line[2]) == 'None':
                        self.point.append('Null')
                    else:
                        self.point.append("'" + str(line[2]) + "'")
                    if str(line[3]) == 'None':
                        self.raport_number.append('Null')
                    else:
                        self.raport_number.append("'" + str(line[3]) + "'")
                    if str(line[4]) == 'None':
                        self.date.append('Null')
                    else:
                        self.date.append("'" + str(line[4]) + "'")
                    if str(line[5]) == 'None':
                        self.value.append('Null')
                    else:
                        self.value.append("'" + str(line[5]) + "'")
                    if str(line[6]) == 'None':
                        self.type.append('Null')
                    else:
                        self.type.append(str("'" + str(line[6]) + "'"))
                    if str(line[7]) == 'None':
                        self.unit.append('Null')
                    else:
                        self.unit.append("'" + str(line[7]) + "'")

                    querryUP = "insert into measurements_low(parent, id, point, raport_number, date, value, type, unit) values(" \
                               + str(self.parent[c]) + "," + str(self.id[c]) + "," + str(self.point[c]) + "," \
                               + str(self.raport_number[c]) + "," + str(self.date[c]) + "," + str(self.value[c]) + "," \
                               + str(self.type[c]) + "," + str(self.unit[c]) + ")"
                    q_run(connTARGET, querryUP)

            getVals(self)

    class meascharts(object):
        def __init__(self):
            self.lp = list()
            self.shipid = list()
            self.id = list()
            self.point = list()
            self.report_number = list()
            self.date = list()
            self.domain = list()
            self.type = list()
            self.unit = list()
            self.chart = list()

            def getVals(self):
                c = -1
                querryGET = "select lp, shipid, id, point, report_number, date, domain, type, unit, chart from meascharts where shipid = " + str(pw_new_in.get())
                table = q_run(connBASE, querryGET)
                COPYCHARTSProgress_bar['maximum'] = len(table)
                COPYCHARTSProgress_bar.grid(row=1, column=2)
                for line in table:
                    c += 1
                    COPYCHARTSVar.set(str(c + 1) + ' / ' + str(len(table)))
                    COPYCHARTSProgress_bar['value'] = c + 1
                    COPYCHARTSProgress_bar.update()
                    self.lp.append(line[0])
                    if str(line[1]) == 'None':
                        self.shipid.append('Null')
                    else:
                        self.shipid.append(str(line[1]))
                    if str(line[2]) == 'None':
                        self.id.append('Null')
                    else:
                        self.id.append("'" + str(line[2]) + "'")
                    if str(line[3]) == 'None':
                        self.point.append('Null')
                    else:
                        self.point.append("'" + str(line[3]) + "'")
                    if str(line[4]) == 'None':
                        self.report_number.append('Null')
                    else:
                        self.report_number.append("'" + str(line[4]) + "'")
                    if str(line[5]) == 'None':
                        self.date.append('Null')
                    else:
                        self.date.append("'" + str(line[5]) + "'")
                    if str(line[6]) == 'None':
                        self.domain.append('Null')
                    else:
                        self.domain.append("'" + str(line[6]) + "'")
                    if str(line[7]) == 'None':
                        self.type.append('Null')
                    else:
                        self.type.append(str("'" + str(line[7]) + "'"))
                    if str(line[8]) == 'None':
                        self.unit.append('Null')
                    else:
                        self.unit.append("'" + str(line[8]) + "'")
                    if str(line[9]) == 'None':
                        self.chart.append('Null')
                    else:
                        self.chart.append("'" + str(line[9]) + "'")

                    querryUP = "insert into meascharts(lp, shipid, id, point, report_number, date, domain, type, unit, chart) values(" + str(
                        self.lp[c]) + "," + str(self.shipid[c]) + "," + str(self.id[c]) + "," + str(
                        self.point[c]) + "," + str(self.report_number[c]) + "," + str(self.date[c]) + "," + str(
                        self.domain[c]) + "," + str(self.type[c]) + "," + str(self.unit[c]) + "," + str(self.chart[c]) + ")"
                    q_run(connTARGET, querryUP)

            getVals(self)

    def convertcharts():
        querry = "select chart from measurements where parent = " + str(pw_new_in.get()) + " order by chart "

        chartlist = q_run(connBASE,querry)
        p=-1
        var = StringVar()
        var.set(p)

        CONVERTCHARTSProgress_bar['maximum'] = len(chartlist)
        CONVERTCHARTSProgress_bar.grid(row=2, column=2)
        for oid in chartlist:
            p += 1

            CONVERTCHARTSVar.set(str(p + 1) + ' / ' + str(len(chartlist)))
            CONVERTCHARTSProgress_bar['value'] = p + 1
            CONVERTCHARTSProgress_bar.update()



            CONVERTCHARTSProgress_bar['value'] = p+1
            CONVERTCHARTSProgress_bar.update()
            var.set(str(p) + ' / ' +str(len(chartlist)))
            querry = 'select parent, id, point, report_number, date, domain, type from measurements where chart ='  + str(oid[0])
            detailstab = q_run(connBASE,querry)
            parent_ = detailstab[0][0]
            id_ = detailstab[0][1]
            point_ = detailstab[0][2]
            reportno_ = detailstab[0][3]
            date_ = detailstab[0][4]
            domain_ = detailstab[0][5]
            type_ = detailstab[0][6]
            if host == 'localhost':
                querry = "select lo_export(measurements.chart,'C:\\overmind\\temp\oid" + str(oid[0]) +  ".csv') from measurements where chart = " + str(oid[0])
                q_run(connBASE,querry)
                paths = ("C:\\overmind\\temp\oid" + str(oid[0]) +  ".csv")
                while not os.path.exists(str(paths)):

                    time.sleep(1)
                try:
                    x = np.loadtxt(paths)
                    try:
                        x = ';'.join(map(str,x))
                    except:
                        x = ';'.join(x)

                    os.remove(paths)
                    querry = """insert into meascharts(shipid,id,point,report_number,date,domain,type,chart,unit) values
                                (""" + str(parent_) + "," + str(id_) + ",'" + str(point_) + "','" + str(reportno_) + "','" + str(date_) + "','" + str(domain_) + "','" + str(type_) + "','" + str(x) + "','[?]')"
                    q_run(connTARGET,querry)
                except:
                    print('Error, iter ' + str(p))
            else:

                querry = "select lo_export(measurements.chart,'/home/filip/Public/tempchart" + str(oid[0]) +  ".csv') from measurements where chart = " + str(oid[0])



                q_run(connBASE,querry)

                paths = (r"\\192.168.8.125\Public\tempchart" + str(oid[0]) + ".csv")
                while not os.path.exists(str(paths)):

                    time.sleep(1)
                try:
                    x = np.loadtxt(paths)
                    try:
                        x = ';'.join(map(str,x))
                    except:
                        x = ';'.join(x)

                    os.remove(paths)
                    querry = """insert into meascharts(shipid,id,point,report_number,date,domain,type,chart,unit) values
                                (""" + str(parent_) + "," + str(id_) + ",'" + str(point_) + "','" + str(reportno_) + "','" + str(date_) + "','" + str(domain_) + "','" + str(type_) + "','" + str(x) + "','[?]')"
                    q_run(connTARGET,querry)

                except:
                    print('Error, iter ' + str(p))
        pbar.mainloop()




    measurements_low()

    meascharts()
    convertcharts()









frame=Tk()
pw_new=Label(frame, text='Shipid')
pw_new_in=Entry(frame)

pw_new.grid(row=2,column=0)
pw_new_in.grid(row=2,column=1)

ok=Button(frame,text='zatwierdz',command = runmove)
ok.grid(row=3,column=1)

frame.mainloop()