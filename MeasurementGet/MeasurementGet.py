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
username = 'filipb'
password = '@infomarine'
host = '192.168.8.10'
connD = [username,password,host]
connD2 = ['dbadmin','242QhpbS&9Fv','192.168.10.243']
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



def copycharts():
    querry = "select chart from measurements order by chart "
    chartlist = q_run(connD,querry)
    print(len(chartlist))
    pbar = tk.Tk()
    pbar.title("Charts")
    p=-1
    var = StringVar()
    var.set(p)
    label1 = tk.Label(pbar,textvariable = var)
    progress_bar = ttk.Progressbar(pbar,orient = 'horizontal',lengt = 286, mode = 'determinate')
    progress_bar['maximum'] =len(chartlist)
    progress_bar.pack()
    label1.pack()
    for oid in chartlist:
        p += 1
        progress_bar['value'] = p+1
        progress_bar.update()
        var.set(str(p) + ' / ' +str(len(chartlist)))
        querry = 'select parent, id, point, report_number, date, domain, type from measurements where chart ='  + str(oid[0])
        detailstab = q_run(connD,querry)
        parent_ = detailstab[0][0]
        id_ = detailstab[0][1]
        point_ = detailstab[0][2]
        reportno_ = detailstab[0][3]
        date_ = detailstab[0][4]
        domain_ = detailstab[0][5]
        type_ = detailstab[0][6]
        if host == 'localhost':
            querry = "select lo_export(measurements.chart,'C:\overmind\\temp\oid" + str(oid[0]) +  ".csv') from measurements where chart = " + str(oid[0])
            q_run(connD,querry)
            paths = ("C:\overmind\\temp\oid" + str(oid[0]) +  ".csv")
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
                q_run(connD2,querry)
            except:
                print('Error, iter ' + str(p))
    pbar.mainloop()
