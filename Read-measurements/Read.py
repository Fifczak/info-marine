import psycopg2

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox

from tkinter.filedialog import askopenfilename
from tkinter import Tk

import matplotlib.pyplot as plt
import numpy as num
import tkinter as tkk
from tkinter import filedialog
import datetime
import xlrd
from math import *


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


def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True


class meas(object):
    def __init__(self):
        self.checked = False
        self.routename = ''
        self.point = ''
        self.domain = ''
        self.type = ''
        self.unit = ''
        self.date = ''
        self.id = ''
        self.mode = ''
        self.chart = list();
        self.start = ''
        self.increment = ''
        self.end = ''
        self.overall = ''

        self.iterb = ''
        self.iterc = ''


# RUN FUNKCJA
def read_measurement_file(device, username, password, host, rnumber, parent):
    connD = [username, password, host]

    def get_meas():
        def readomnitrend():
            def countoverall(self):
                y = meas()
                y.routename = self.routename
                y.point = self.point
                y.domain = self.domain
                y.type = self.type
                y.unit = self.unit
                y.date = self.date
                y.mode = 'Overall'
                sumVal = 0
                freq = float(self.start)
                for m in self.chart:
                    if freq > 10 and freq < 1000:  ## TUTAJ BEDZIE TRZEBA ZROVBC ZMIENNE ZAKRESY W ZALEZNOSCI OD STATKU / URZADZENIA / NORMY
                        sumVal += pow(m, 2)
                    freq += float(self.increment)
                WTFparam = 1
                if self.type == 'Vel':
                    WTFparam = 0.5  # //DLA AURORY
                y.overall = round(sqrt(sumVal) * WTFparam, 3)

                if str(self.type) == 'Env':
                    y.type = 'envelope P-K'
                elif str(self.type) == 'Vel':
                    y.type = 'RMS'
                return y

            def getchart(lines, xcord):
                iter = xcord
                chartstr = ''
                chart = list();
                while True:
                    chartstr = chartstr + str(lines[iter])
                    iter += 1
                    try:
                        if (str(lines[iter])).strip() == '#RefSpeed':
                            break
                    except:
                        break
                charttr = chartstr.split(" ")
                for i in charttr:
                    chart.append(round(float(i), 3))
                return chart

            def get_route_name(routename):
                namepoint = []
                lastslashcord = routename.rfind("\\")
                pointonlast = routename[:lastslashcord]
                lastslashcord = pointonlast.rfind("\\")
                pointname = pointonlast[(lastslashcord + 1):]
                nameonlast = pointonlast[:lastslashcord]
                lastslashcord = nameonlast.rfind("\\")
                cleanname = nameonlast[(lastslashcord + 1):]
                namepoint.append(cleanname)
                namepoint.append(pointname)
                return namepoint

            def get_date(unformateddate):
                equalcord = unformateddate.rfind("=")
                monthstr = unformateddate[(equalcord + 5):(equalcord + 8)]
                if monthstr == 'Jan': month = '01'
                if monthstr == 'Feb': month = '02'
                if monthstr == 'Mar': month = '03'
                if monthstr == 'Apr': month = '04'
                if monthstr == 'May': month = '05'
                if monthstr == 'Jun': month = '06'
                if monthstr == 'Jul': month = '07'
                if monthstr == 'Aug': month = '08'
                if monthstr == 'Sep': month = '09'
                if monthstr == 'Oct': month = '10'
                if monthstr == 'Nov': month = '11'
                if monthstr == 'Dec': month = '12'
                day = unformateddate[(equalcord + 9):(equalcord + 11)]
                year = unformateddate[(len(unformateddate) - 4):]
                datestr = str(year) + '-' + str(month) + '-' + str(day)
                return datestr

            def get_measdomain(measno):
                measdomain = list();

                if str(parent) == '103':
                    if measno == '1004' or measno == '1007' or measno == '1025' or measno == '1059':
                        measdomain.append(
                            'FFT'), measdomain.append('Vel'), measdomain.append('[mm/s]')
                    elif measno == '1018' or measno == '1028' or measno == '1029':
                        measdomain.append('FFT'), measdomain.append('Env'), measdomain.append('[m/s2]')

                    else:
                        measdomain.append('UNKNOWN'), measdomain.append('UNKNOWN'), measdomain.append('UNKNOWN')

                if str(parent) == '46':
                    if measno == '1004' or measno == '1007' or measno == '1026' or measno == '1028':
                        measdomain.append(
                            'FFT'), measdomain.append('Vel'), measdomain.append('[mm/s]')
                    elif measno == '1023' or measno == '1025' or measno == '1027':
                        measdomain.append('FFT'), measdomain.append('Env'), measdomain.append('[m/s2]')

                    else:
                        measdomain.append('UNKNOWN'), measdomain.append('UNKNOWN'), measdomain.append('UNKNOWN')

                return measdomain

            Tk().withdraw()
            a = filedialog.askopenfilename()
            f = open(a, "r")
            lines = f.read().split("\n")  # "\r\n" if needed
            measno = -1
            xcord = 0
            for line in lines:

                xcord += 1

                if line == '#----- Start Task -----':
                    x = meas()
                if line == '#Path':
                    x.routename = (get_route_name(lines[xcord]))[0]
                    x.point = (get_route_name(lines[xcord]))[1]
                if line == '#Setupnumber':
                    x.domain = (get_measdomain(lines[xcord]))[0]
                    x.type = (get_measdomain(lines[xcord]))[1]
                    x.unit = (get_measdomain(lines[xcord]))[2]

                if line == '#Date':
                    x.date = get_date(lines[xcord])

                if line == '#X-Start,Increment,X-End':
                    x.start = str(lines[xcord])[0:7]
                    x.increment = str(lines[xcord])[9:16]
                    x.end = str(lines[xcord])[18:]
                if line == '#Y-Values':
                    x.mode = 'FFT'
                    x.chart = getchart(lines, xcord)
                    measlist.append(x)
                    measlist.append(countoverall(x))

                    measno += 1

        def readmarvib():
            a = filedialog.askopenfilename()
            # a = 'C:\Overmind\data\hara.csv'
            f = open(a, "r")
            lines = f.read().split("\n")  # "\r\n" if needed
            TEMPcols = []
            route = []
            xcord = 0
            iter = 0
            lines_line = 0
            pbar = tk.Tk()
            pbar.title("Reading Marvib measurement file")
            progress_bar = ttk.Progressbar(pbar, orient='horizontal', lengt=286, mode='determinate')
            progress_bar['maximum'] = len(lines)
            progress_bar.pack()
            p = 0
            for line in lines:
                lines_line += 1
                progress_bar['value'] = p
                p += 1
                progress_bar.update()
                if line != " ":  # add other needed checks to skip titles
                    cols = line.split("\t")
                    if cols[0] == 'eDataIdMeaType':
                        if str(lines[p][:14]) == 'eDataIdMeaData':
                            xcord += 1
                            x = meas()

                            if cols[1] == 'eMeaDisplacement':
                                continue
                            if cols[1] == 'eMeaVelocity':  ########### START RMS VELOCITY

                                iter += 1
                                x.mode = 'Overall'
                                x.unit = '[mm/s]'
                                x.type = 'RMS'
                                measflag = 1
                                iterb = lines_line
                                x.iterb = iterb
                                while measflag == 1:
                                    iterb -= 1
                                    cols2 = lines[iterb].split("\t")
                                    if cols2[0] == 'eDataIdLocation' and cols2[1] == 'eTypePoint':
                                        if is_empty(cols2[2]) == False:
                                            x.point = cols2[2]
                                            pointflag = 1
                                            iterc = iterb
                                            while pointflag == 1:
                                                iterc -= 1
                                                cols3 = lines[iterc].split("\t")
                                                if cols3[0] == 'eDataIdLocation' and cols3[1] == 'eTypeMachine':
                                                    x.routename = cols3[2]
                                                    iterc = 0
                                                    break
                                            if iterc == 0:
                                                measflag = 0
                                    if iterb == 0:
                                        measflag = 0
                                measflag = 2
                                iterb = lines_line
                                x.iterc = iterb

                                while measflag == 2:
                                    iterb += 1
                                    try:
                                        cols2 = lines[iterb].split("\t")
                                        if cols2[0] == 'Year':
                                            if len(cols2[3]) == 1:
                                                x.date = str(cols2[1] + '-0' + cols2[3] + '-' + cols2[5])
                                            elif len(cols2[3]) == 2:
                                                x.date = str(cols2[1] + '-' + cols2[3] + '-' + cols2[5])
                                        if cols2[0] == 'RMS':
                                            x.overall = round(float(cols2[1]), 3)
                                            measflag = 0
                                            measlist.append(
                                                x)  ##########################################################################
                                            break
                                        if iterb == iter + 1000:
                                            measflag = 0
                                            break
                                    except:
                                        measflag = 0
                                        break
                            #############END RMS VELOCITY
                            if cols[1] == 'eMeaAcceleration':
                                iter += 1
                                continue
                            if cols[1] == 'eMeaBearingEnvelope':  ########### START PK ENV

                                iter += 1
                                x.mode = 'Overall'
                                x.type = 'envelope P-K'
                                x.unit = '[m/s2]'
                                measflag = 1
                                iterb = lines_line
                                while measflag == 1:
                                    iterb -= 1
                                    cols2 = lines[iterb].split("\t")
                                    if cols2[0] == 'eDataIdLocation' and cols2[1] == 'eTypePoint':
                                        x.point = cols2[2]
                                        pointflag = 1
                                        iterc = iterb
                                        while pointflag == 1:
                                            iterc -= 1
                                            cols3 = lines[iterc].split("\t")
                                            if cols3[0] == 'eDataIdLocation' and cols3[1] == 'eTypeMachine':
                                                x.routename = cols3[2]
                                                iterc = 0
                                                break
                                        if iterc == 0:
                                            measflag = 0
                                    if iterb == 0:
                                        measflag = 0
                                measflag = 2
                                iterb = lines_line
                                while measflag == 2:
                                    try:
                                        iterb += 1
                                        cols2 = lines[iterb].split("\t")
                                        if cols2[0] == 'Year':

                                            if len(cols2[3]) == 1:
                                                x.date = str(cols2[1] + '-0' + cols2[3] + '-' + cols2[5])
                                            else:
                                                x.date = str(cols2[1] + '-' + cols2[3] + '-' + cols2[5])
                                        if cols2[0] == 'PK':
                                            x.overall = round(float(cols2[1]), 3)
                                            measlist.append(
                                                x)  ##########################################################################
                                            break
                                        if iterb == iter + 1000:
                                            measflag = 0
                                    except:
                                        measflag = 0
                                #############END PK ENV

                            if cols[1] == 'eMeaTiming':
                                # iter += 1
                                continue
                            if cols[1] == 'eMeaBearingKurtosis':
                                # iter += 1
                                continue
                            if cols[1] == 'eMeaFourierTransform':  ###########START FFT

                                iter += 1
                                x.mode = 'FFT'
                                x.domain = 'FFT'
                                measflag = 1
                                iterb = lines_line
                                while measflag == 1:
                                    iterb -= 1
                                    cols2 = lines[iterb].split("\t")
                                    if cols2[0] == 'eDataIdLocation' and cols2[1] == 'eTypePoint':
                                        x.point = cols2[2]
                                        pointflag = 1
                                        iterc = iterb
                                        while pointflag == 1:
                                            iterc -= 1
                                            cols3 = lines[iterc].split("\t")
                                            if cols3[0] == 'eDataIdLocation' and cols3[1] == 'eTypeMachine':
                                                x.routename = cols3[2]
                                                iterc = 0
                                                break
                                        if iterc == 0:
                                            measflag = 0
                                    if iterb == 0:
                                        measflag = 0
                                measflag = 2
                                iterb = lines_line
                                while measflag == 2:
                                    try:
                                        iterb += 1
                                        cols2 = lines[iterb].split("\t")
                                        if cols2[0] == 'Year':
                                            if len(cols2[3]) == 1:
                                                x.date = str(cols2[1] + '-0' + cols2[3] + '-' + cols2[5])
                                            else:
                                                x.date = str(cols2[1] + '-' + cols2[3] + '-' + cols2[5])

                                        if cols2[0] == 'eLines':
                                            iter = 0
                                            for item in cols2:
                                                if iter != 0: x.chart.append(round(float(item), 3))
                                                iter += 1

                                        if cols2[0] == 'frange':
                                            if cols2[1] == '2':
                                                maxF = 400
                                            elif cols2[1] == '3':
                                                maxF = 800
                                            elif cols2[1] == '4':
                                                maxF = 1600
                                            elif cols2[1] == '5':
                                                maxF = 3200
                                            x.start = (maxF / 1600)
                                            x.increment = x.start
                                            x.end = maxF

                                        if cols2[0] == 'avx':
                                            if cols2[1] == '0':
                                                x.type = 'Acc'
                                                x.unit = '[m/s2]'
                                            elif cols2[1] == '1':
                                                x.type = 'Vel'
                                                x.unit = '[m/s]'
                                            elif cols2[1] == '2':
                                                x.type = 'Dis'
                                                x.unit = '[m]'
                                            elif cols2[1] == '3':
                                                x.type = 'Env'
                                                x.unit = '[m/s2]'
                                            measlist.append(
                                                x)  ##########################################################################
                                            break
                                        if iterb == iter + 1000:
                                            measflag = 0
                                    except:
                                        measflag = 0
            pbar.destroy()

        def readezthomas():
            def decodedate(inputstring):
                # lastslashcord = routename.rfind( "\\" )
                daystr = inputstring[20:22]
                monthstr = inputstring[23:26]
                yearstr = inputstring[27:31]
                if monthstr == "sty":
                    monthstr = "01"
                elif monthstr == "lut":
                    monthstr = "02"
                elif monthstr == "mar":
                    monthstr = "03"
                elif monthstr == "kwi":
                    monthstr = "04"
                elif monthstr == "maj":
                    monthstr = "05"
                elif monthstr == "cze":
                    monthstr = "06"
                elif monthstr == "lip":
                    monthstr = "07"
                elif monthstr == "sie":
                    monthstr = "08"
                elif monthstr == "wrz":
                    monthstr = "09"
                elif monthstr == "paź":
                    monthstr = "10"
                elif monthstr == "lis":
                    monthstr = "11"
                elif monthstr == "gru":
                    monthstr = "12"
                datestr = yearstr + '-' + monthstr + '-' + daystr
                return datestr

            def decodename(inputstr):
                pointandname = list()
                Machine = inputstr[:2]
                Point = inputstr[2:]
                Point = Point.strip()
                if str(Machine) == 'T1':
                    if Point.find('Mot') != -1: Machine = "Thruster 1 motor"
                    if Point.find('Thruster') != -1: Machine = "Thruster 1"
                if str(Machine) == 'T2':
                    if Point.find('Mot') != -1: Machine = "Thruster 2 motor"
                    if Point.find('Thruster') != -1: Machine = "Thruster 2"
                if str(Machine) == 'T3':
                    if Point.find('Mot') != -1: Machine = "Thruster 3 motor"
                    if Point.find('Thruster') != -1: Machine = "Thruster 3"
                if str(Machine) == 'T4':
                    if Point.find('Mot') != -1: Machine = "Thruster 4 motor"
                    if Point.find('Thruster') != -1: Machine = "Thruster 4"
                if str(Machine) == 'T5':
                    if Point.find('Mot') != -1: Machine = "Thruster 5 motor"
                    if Point.find('Thruster') != -1: Machine = "Thruster 5"
                if str(Machine) == 'T6':
                    if Point.find('Mot') != -1: Machine = "Thruster 6 motor"
                    if Point.find('Thruster') != -1: Machine = "Thruster 6"

                if Point == "Thruster Proa": Point = "H3"
                if Point == "Mot Sup Babor": Point = "HH1"
                if Point == "Mot Inf Proa": Point = "H2"
                if Point == "Mot Inf Babor": Point = "HH2"
                if Point == "Mot Inf Ver": Point = "A2"
                if Point == "Mot Sup Proa": Point = "H1"
                if Point == "Thruster Vert" or Point == "Thruster Ver": Point = "HH3"
                if Point == "Thruster Babor": Point = "A3"

                pointandname.append(Machine)

                pointandname.append(Point)
                return pointandname

            def countoverall(self):
                y = meas()
                y.routename = self.routename
                y.point = self.point
                y.domain = self.domain
                y.type = self.type
                y.unit = self.unit
                y.date = self.date
                y.mode = 'Overall'
                sumVal = 0
                freq = float(self.start)
                for m in self.chart:
                    if freq > 10 and freq < 1000:  ## TUTAJ BEDZIE TRZEBA ZROVBC ZMIENNE ZAKRESY W ZALEZNOSCI OD STATKU / URZADZENIA / NORMY
                        sumVal += pow(m, 2)
                    freq += float(self.increment)
                WTFparam = 1
                if self.type == 'Vel':
                    WTFparam = 0.5  # //DLA AURORY
                y.overall = round(sqrt(sumVal) * WTFparam, 3)
                if str(self.type) == 'Env':
                    y.type = 'envelope P-K'
                elif str(self.type) == 'Vel':
                    y.type = 'RMS'
                return y

            file = filedialog.askopenfilename()
            workbook = xlrd.open_workbook(file)
            worksheet = workbook.sheet_by_index(0)

            for column in range(worksheet.ncols):  # Tu szukamy pomiarów

                if worksheet.cell(0, column).value == 'eZ-TOMAS Remote 8,0,40' or worksheet.cell(0,
                                                                                                 column).value == 'eZ-TOMAS 8,0,40':  # Znalezienie raport sheeta
                    DecDate = decodedate(worksheet.cell(2, column).value)

                    for row in range(worksheet.nrows):
                        if worksheet.cell(row, column).value == '1.   Frequency (Hz)':
                            for row2 in range(worksheet.nrows):  # Szukanie measstart
                                if worksheet.cell(row + row2 + 1, column + 1).value == xlrd.empty_cell.value:
                                    measnumbers = row2

                                    measstart = (row + row2 + 3)
                                    break
                            for row2 in range(measnumbers):  # Szukanie nazw
                                x = meas()
                                chartlist = list()
                                x.date = DecDate
                                x.mode = 'FFT'
                                x.domain = 'FFT'
                                x.type = 'Vel'
                                x.routename = decodename(worksheet.cell(row + row2 + 1, column + 1).value)[0]
                                x.point = decodename(worksheet.cell(row + row2 + 1, column + 1).value)[1]
                                x.start = worksheet.cell(measstart, column).value
                                x.increment = worksheet.cell(measstart + 1, column).value
                                chartlist.clear()
                                for chartiter in range(worksheet.nrows):
                                    if worksheet.cell(measstart + chartiter,
                                                      column + row2).value == xlrd.empty_cell.value: break
                                    x.chart.append(
                                        round(float(worksheet.cell(measstart + chartiter, column + row2).value), 3))
                                    x.end = worksheet.cell(measstart + chartiter, column).value
                                    chartlist.append(
                                        round(float(worksheet.cell(measstart + chartiter, column + row2 + 1).value), 3))
                                x.chart = chartlist
                                measlist.append(x)
                                measlist.append(countoverall(x))
                            break

        if str(device) == 'Vibscanner':
            readomnitrend()
        elif str(device) == 'Marvib':
            readmarvib()
        elif str(device) == 'ezThomas':
            readezthomas()

    def changepointWindow(point, id_):
        def change_pointname():
            querry = "SELECT point from points where point = '" + str(changepointEntry.get()) + "' and id = " + str(id_)
            trypoint = q_run(connD, querry)
            if not trypoint:
                querry = "UPDATE points set point = '" + str(
                    changepointEntry.get()) + "' where point = '" + point + "' and id = " + str(id_)
                q_run(connD, querry)
                changepointWindow.destroy()
            else:
                messagebox.showinfo("Error", ("Point " + str(changepointEntry.get()) + " exists"))

        changepointWindow = tk.Tk()
        changepointWindow.title("Change point name")
        changepointEntry = tk.Entry(changepointWindow)
        changepointEntry.insert(END, point)
        okbutton = tk.Button(changepointWindow, text='ChaHHnge point name', command=lambda: change_pointname())
        changepointEntry.pack(side=TOP)
        okbutton.pack(side=TOP)
        changepointWindow.mainloop()

    def window_load():
        deviceframe = Frame(Window)
        mylist = Listbox(Window)
        mylist.config(width=0)
        ycord = 0
        for x in measlist:
            mylist.insert(END, str(x.routename) + ' ' + str(x.point) + ' ' + str(x.domain) + ' ' + str(x.date))
            ycord += 1
        cs = mylist.curselection()
        mylist.pack(side=LEFT, fill=BOTH)
        Window.mainloop()

    def deviceinstructWindow(id_):
        def change_routename(routename):
            querry = "UPDATE crosstable SET nameindevice ='" + (str(routename)).strip() + "' where id =" + str(id_)
            q_run(connD, querry)

        def pointselect(evt):
            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)

            changepointWindow(value, id_)

        PointsWindow = tk.Tk()
        PointsWindow.title("Points")
        querry = 'select point from points where id = ' + str(id_) + ' order by sort'
        pointquerry = q_run(connD, querry)
        querry = 'select name from devices where id = ' + str(id_)
        namequerry = q_run(connD, querry)
        querry = 'select nameindevice from crosstable where id = ' + str(id_)
        routenamequerry = q_run(connD, querry)
        deviceID = tk.Label(PointsWindow, text="#" + str(id_) + str(namequerry[0][0]))
        nameindevice = tk.Entry(PointsWindow)
        nameindevice.config(width=100)
        nameindevice.insert(END, routenamequerry[0][0])
        okbutton = tk.Button(PointsWindow, text='Change routename',
                             command=lambda: change_routename(nameindevice.get()))
        pointslist = Listbox(PointsWindow)
        pointslist.config(width=100)
        pointslist.bind('<Double-Button>', pointselect)
        ycord = 0
        for x in pointquerry:
            pointslist.insert(END, str(x[0]))
        deviceID.pack(side=TOP)
        nameindevice.pack(side=TOP)
        okbutton.pack(side=TOP)
        pointslist.pack(side=TOP)
        PointsWindow.mainloop()

    def createchartwindow(id_):
        ChartWindow = tk.Tk()
        ChartWindow.title("Chart")
        L1 = Chartwindow.Label(text="TEST")
        L1.pack(side=TOP)
        ChartWindow.mainloop()

    def window_crosstable():
        Window = tk.Tk()
        Window.title("Loader")
        okbutton = tk.Button(Window, text='Reload')
        okbutton.pack(side=TOP)

        def upload():
            Window.destroy()
            pbar = tk.Tk()
            pbar.title("Uploading Measurements")
            progress_bar = ttk.Progressbar(pbar, orient='horizontal', lengt=286, mode='determinate')

            progress_bar['maximum'] = len(measlist)
            progress_bar.pack()

            p = 0
            OveCount = 0
            for i in measlist:
                # print(i.point)
                p += 1

                if i.mode == 'FFT':
                    try:
                        progress_bar['value'] = p
                    except:
                        progress_bar['value'] = progress_bar['value']
                    progress_bar.update()
                    chartstrlist = list();
                    chartstrlist.append(str(i.increment))
                    chartstrlist.append(str(i.end))
                    for j in i.chart:
                        strj = str(j)
                        chartstrlist.append(strj)
                    chartstr = (";".join(chartstrlist))
                    querry = "INSERT INTO meascharts(shipid,id,point,report_number, date, domain, type, unit, chart) VALUES (" + str(
                        parent) + "," + str(i.id) + ",'" + str(i.point) + "','" + str(rnumber) + "','" + str(
                        i.date) + "','" + str(i.domain) + "','" + str(i.type) + "','" + str(i.unit) + "','" + str(
                        chartstr) + "')"

                if i.mode == 'Overall':
                    OveCount += 1
                    querry = "INSERT INTO measurements_low(parent,id, point, raport_number, date, type, unit, value) VALUES (" + str(
                        parent) + "," + str(i.id) + ",'" + str(i.point) + "','" + str(rnumber) + "','" + str(
                        i.date) + "','" + str(i.type) + "','" + str(i.unit) + "','" + str(i.overall) + "')"

                q_run(connD, querry)
                try:
                    chartstrlist.clear
                    del chartstr
                except:
                    x = 1
            pbar.destroy()
            querry = "select dev_in from harmonogram where report_number ='" + str(rnumber) + "' limit 1"
            devins = q_run(connD, querry)
            try:
                devin = devins[0]
                newdevin = int(devin) + int(OveCount)
            except:
                newdevin = 0 + int(OveCount)

            querry = "update harmonogram set dev_in = " + str(newdevin) + " where report_number ='" + str(rnumber) + "'"
            q_run(connD, querry)

        def check_routename(x, no):
            routename = x.routename
            routename = routename.strip()
            cpoint = x.point
            cpoint = cpoint.strip()

            for y in crosstablequerry:
                if str((y[1]).strip()) == str(routename):
                    for yy in pointstable:
                        if yy[1] == str(cpoint):
                            x.id = y[0]
                            if str(yy[0]) == str(x.id):
                                x.checked = True
                                mylist.itemconfig(no, bg='green')
            mylist.forget()
            crosstablelist.forget()
            mylist.pack(side=LEFT, fill=BOTH)
            crosstablelist.pack(side=LEFT, fill=BOTH)

        def onselect(evt):
            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)
            deviceinstructWindow(crosstablequerry[index][0])

        def onselect2(evt):
            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)
            cstart = (float(measlist[index].start))
            cincrement = float(measlist[index].increment)
            cend = (float(measlist[index].end))
            fig = plt.figure(figsize=(15, 6))
            plt.cla()
            Y = list();
            Y.append(cstart)
            ycord = 0
            for y in measlist[index].chart:
                if ycord != 0:
                    Y.append(float(Y[ycord - 1]) + cincrement)
                ycord += 1
            x = measlist[index].chart
            plt.plot(Y, x)
            plt.xlabel('Frequency [Hz]')
            plt.ylabel('Velocity[mm/s]')
            axes = plt.gca
            plt.show()

        def reload_lists():
            Window.destroy()

            window_crosstable()

        querry = 'select cs.id,nameindevice,name from crosstable as cs left join devices as dev on cs.id = dev.id where cs.parent = ' + str(
            parent) + ' order by name'
        crosstablequerry = q_run(connD, querry)
        querry = 'select id, point, sort from points where id IN (select id from devices where parent = ' + str(
            parent) + ') order by id, sort'
        pointstable = q_run(connD, querry)
        crosstableframe = Frame(Window)
        crosstablelist = Listbox(Window)
        crosstablelist.config(width=100)
        crosstablelist.bind('<Double-Button>', onselect)
        mylist = Listbox(Window)
        mylist.config(width=100)
        mylist.bind('<Double-Button>', onselect2)
        ycord = 0
        for x in measlist:
            mylist.insert(END,
                          str(x.routename) + ' ' + str(x.point) + ' ' + str(x.mode) + ' ' + str(x.overall) + ' ' + str(
                              x.type) + ' ' + str(x.date))
            check_routename(x, ycord)
            ycord += 1
        ycord = 0
        for x in crosstablequerry:
            crosstablelist.insert(END, str(x[1]) + ' #' + str(x[0]) + ' # ' + str(x[2]))
            ycord += 1
        cs = mylist.curselection()
        mylist.pack(side=LEFT, fill=BOTH)
        cs = crosstablelist.curselection()
        crosstablelist.pack(side=LEFT, fill=BOTH)
        okbutton.config(command=reload_lists)
        checkflag = True
        for i in measlist:
            if i.checked == False: checkflag = False
        if checkflag == True:
            if not measlist:
                x = 1
            else:
                upload()
                messagebox.showinfo("Dialog", ("Measurements uploaded"))
                try:
                    Window.destroy()
                except:
                    z = 1
        else:
            Window.mainloop()

    # username = ''
    # password = ''
    # host = ''
    # connD = [username, password, host]
    # parent = 103  # aurora

    # parent = 73 # hafnia america
    # parent = 55 #neptuno platform
    # parent = 35 #norddolphin
    # parent = 61 #nordpenguin
    # parent = 46 #Elizabeth russ
    # rnumber = '2008-2019'

    measlist = []
    get_meas()

    window_crosstable()

# 'Vibscanner'
# 'Marvib'
# 'ezThomas'
read_measurement_file('Marvib','testuser','info','localhost','2016-2019', '61')
