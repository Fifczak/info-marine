import datetime
import xlrd
from tqdm import tqdm
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter import Tk
from tkinter import filedialog
import psycopg2
import re
username = 'testuser'
password = 'info'
host = 'localhost'
connD = [username,password,host]

def column(matrix, i):
    return [row[i] for row in matrix]

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



def sta_update():
    class Device(object):
        def __init__(self):
            self.id = ''
            self.name = ''
            self.desc = ''



    Tk().withdraw()
    file = filedialog.askopenfilename()
    workbook = xlrd.open_workbook(file)
    worksheet = workbook.sheet_by_index(0)
    xsize = worksheet.ncols
    ysize = worksheet.nrows


    dframelist = list()
    x = 0
    for row in range(ysize-2):
        x += 1
        y = 0
        for row in range(xsize-1):
            y += 1

            dframe = Device()
            dframe.id = int(worksheet.cell(x, 2).value)
            dframe.name = worksheet.cell(x, 3).value
            dframe.desc = worksheet.cell(x, 4).value
            dframelist.append(dframe)
            break

    for item in tqdm(dframelist):
        querry = "update standards set iso_name = '{}', iso_desc = '{}' where id = {}".format(item.name, item.desc, item.id)
        #print (querry)
        q_run(connD,querry)

sta_update()