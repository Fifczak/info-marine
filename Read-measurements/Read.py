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
import math

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

def column(matrix, i):
    return [row[i] for row in matrix]


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
            def READoverall(lines,start):
                xcord2 = -1
                while 1:
                    xcord2 += 1
                    if lines[xcord + xcord2] == '#TrendPlusRef':
                        #print((lines[xcord + xcord2+2]).split())######################################### TUTAJ DO SPRAWDZENIA CO ZA WARTOŚĆ BIERZE
                        values =  ((lines[xcord + xcord2+2]).split())
                        value = values[len(values)-4]
                    if lines[xcord + xcord2] == '#Date':
                        date = get_date(lines[xcord + xcord2+1])
                        break
                value = round(float(value), 3)
                return date,value
            def countoverall(self):
                WTFparam = 1
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

                min = 0
                if str(self.type) == 'Env':
                    min = 0
                    WTFparam = 1
                    ### TRZEBA PRZEMYSLEC CZY JEDYNYM WYJATKIEM NIE BEDZIE FSRU I NIE ZROBIC PO PROSTU != 234
                    if str(parent) == '234': ##Jeśli chcemy miec RMS
                        WTFparam = 1
                    if str(parent) == '45' or str(parent) == '46' or str(parent) == '47' or str(parent) == '48': ##Jeśli chcemy miec 0-P
                        WTFparam = 0.73
                elif str(self.type) == 'Vel':
                    min = 10
                    WTFparam = 0.58


                for m in self.chart:
                    if freq > min and freq < 1000:  ## TUTAJ BEDZIE TRZEBA ZROVBC ZMIENNE ZAKRESY W ZALEZNOSCI OD STATKU / URZADZENIA / NORMY
                        sumVal += pow(m, 2)
                    freq += float(self.increment)






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

                if str(parent)=='48':
                    if measno == '1004' or measno == '1007':
                        measdomain.append(
                            'FFT'), measdomain.append('Vel'), measdomain.append('[mm/s]')
                    elif measno == '1018':
                        measdomain.append('FFT'), measdomain.append('Env'), measdomain.append('[m/s2]')
                    else:
                        measdomain.append('UNKNOWN'), measdomain.append('UNKNOWN'), measdomain.append('UNKNOWN')

                if str(parent) == '103':
                    if measno == '1004' or measno == '1007' or measno == '1025' or measno == '1059':
                        measdomain.append(
                            'FFT'), measdomain.append('Vel'), measdomain.append('[mm/s]')
                    elif measno == '1018' or measno == '1028' or measno == '1029':
                        measdomain.append('FFT'), measdomain.append('Env'), measdomain.append('[m/s2]')

                    else:
                        measdomain.append('UNKNOWN'), measdomain.append('UNKNOWN'), measdomain.append('UNKNOWN')

                if str(parent) == '46' or str(parent) == '47':
                    if measno == '1004' or measno == '1007' or measno == '1026' or measno == '1028':
                        measdomain.append(
                            'FFT'), measdomain.append('Vel'), measdomain.append('[mm/s]')
                    elif measno == '1023' or measno == '1025' or measno == '1027':
                        measdomain.append('FFT'), measdomain.append('Env'), measdomain.append('[m/s2]')

                    else:
                        measdomain.append('UNKNOWN'), measdomain.append('UNKNOWN'), measdomain.append('UNKNOWN')


                if str(parent) == '234': #FSRU
                    if measno == '1007' :
                        measdomain.append('FFT'), measdomain.append('Vel'), measdomain.append('[mm/s]')
                    elif measno == '1018':
                        measdomain.append('FFT'), measdomain.append('Env'), measdomain.append('[m/s2]')
                    elif measno == '1014':
                        measdomain.append('RMS'), measdomain.append('Vel'), measdomain.append('[m/s2]')
                    else:
                        measdomain.append('UNKNOWN'), measdomain.append('UNKNOWN'), measdomain.append('UNKNOWN')




                return measdomain

            root = Tk()
            root.withdraw()
            a = filedialog.askopenfilename()

            f = open(a, "r")
            lines = f.read().split("\n")  # "\r\n" if needed
            xcord = 0
            meason = False

            for line in lines:

                xcord += 1

                if line == '#----- Start Task -----':
                    x = meas()
                    meason = True
                if meason == True:
                    if line == '#Path':
                        x.routename = (get_route_name(lines[xcord]))[0]
                        x.point = (get_route_name(lines[xcord]))[1]
                    if line == '#Setupnumber':
                        x.domain = (get_measdomain(lines[xcord]))[0]
                        x.type = (get_measdomain(lines[xcord]))[1]
                        x.unit = (get_measdomain(lines[xcord]))[2]
                    if str(x.domain) == 'RMS':
                        x.mode = 'Overall'
                        x.date, x.overall = (READoverall(lines, xcord))
                        print (x.date, x.overall)
                        x.type = 'RMS'
                        measlist.append(x)
                        meason = False
                        continue
                    else:
                        if line == '#Date':
                            x.date = get_date(lines[xcord])

                        if line == '#X-Start,Increment,X-End':
                            x.start = str(lines[xcord])[0:7]
                            x.increment = str(lines[xcord])[9:16]
                            x.end = str(lines[xcord])[18:]
                        if line == '#Y-Values':
                            x.mode = 'FFT'
                            x.chart = getchart(lines, xcord)
                            if str(x.type) != 'UNKNOWN':
                                measlist.append(x)
                                if str(parent) != '234' or str(x.type) == 'Env': #przemyslec i zmienic warunek na ze statku na to czy byl overall
                                    measlist.append(countoverall(x))
                                    meason = False
                                    continue

        def readmarvib():
            root = Tk()
            root.withdraw()
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
                                            measlist.append(x)
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
                                            measlist.append(x)
                                            break
                                        if iterb == iter + 1000:
                                            measflag = 0
                                    except:
                                        measflag = 0
                                #############END PK ENV

                            if cols[1] == 'eMeaTiming':
                                iter += 1
                                x.mode = 'TIM'
                                x.domain = 'TIM'
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

                                        if cols2[0] == 'eTableOfSamplesValues':
                                            iter = 0
                                            for item in cols2:
                                                if iter != 0: x.chart.append(round(float(item), 3))
                                                iter += 1
                                            break
                                        if cols2[0] == 'fs':
                                            if cols2[1] == '0':
                                                x.increment = 1 / 256
                                            elif cols2[1] == '1':
                                                x.increment = 1 / 512
                                            elif cols2[1] == '2':
                                                x.increment = 1 / 1024
                                            elif cols2[1] == '3':
                                                x.increment = 1 / 2048
                                            elif cols2[1] == '4':
                                                x.increment = 1 / 4096
                                            elif cols2[1] == '5':
                                                x.increment = 1 / 8192
                                            elif cols2[1] == '6':
                                                x.increment = 1 / 16384
                                            elif cols2[7] == '3':
                                                x.increment = 1 / 32768
                                            elif cols2[8] == '4':
                                                x.increment = 1 / 65536
                                            x.start = 0
                                            x.end = x.increment * 4096

                                        if cols2[0] == 'avx':
                                            if cols2[1] == '0':
                                                x.type = 'Acc'
                                                x.unit = '[m/s2]'
                                            elif cols2[1] == '1':
                                                x.type = 'Vel'
                                                x.unit = '[mm/s]'
                                            elif cols2[1] == '2':
                                                x.type = 'Dis'
                                                x.unit = '[m]'
                                            elif cols2[1] == '3':
                                                x.type = 'Env'
                                                x.unit = '[m/s2]'
                                            measlist.append(x)

                                            #break
                                        if iterb == iter + 1000:
                                            measflag = 0
                                    except:
                                        measflag = 0

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
                                            elif cols2[1] == '6':
                                                maxF = 6400
                                            x.start = (maxF / 1600)
                                            x.increment = x.start
                                            x.end = maxF

                                        if cols2[0] == 'avx':
                                            if cols2[1] == '0':
                                                x.type = 'Acc'
                                                x.unit = '[m/s2]'
                                            elif cols2[1] == '1':
                                                x.type = 'Vel'
                                                x.unit = '[mm/s]'
                                            elif cols2[1] == '2':
                                                x.type = 'Dis'
                                                x.unit = '[m]'
                                            elif cols2[1] == '3':
                                                x.type = 'Env'
                                                x.unit = '[m/s2]'
                                            measlist.append(x)


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

            root = Tk()
            root.withdraw()
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
                                    try:
                                        chartlist.append(
                                            round(float(worksheet.cell(measstart + chartiter, column + row2 + 1).value), 3))
                                    except:chartlist.append(0)
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
                querry = "UPDATE measurements_low set point = '{}' where id = {} and point = '{}' ".format(changepointEntry.get(),id_,point)
                q_run(connD, querry)
                querry = "UPDATE meascharts set point = '{}' where id = {} and point = '{}' ".format(changepointEntry.get(),id_,point)
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

            def recountoverall(id,rn):
                querry = "SELECT point,value from measurements_low where raport_number = '" + str(rn) + "' and id = " + str(id) + " and type = 'RMS' group by point,value"

                pointslist = q_run(connD, querry)

                for point in pointslist:
                    x = []
                    querry = "SELECT chart from meascharts where report_number = '" + str(rn) + "' and id = " + str(
                        id) + " and type = 'Vel'  and domain = 'FFT' and point = '" + str(point[0]) + "'"
                    chartstr = q_run(connD, querry)[0][0]
                    chartstrlist = chartstr.split(";")
                    for line in chartstrlist:
                        x.append(float(line))

                    xlen = int(len(x) - 2)
                    tp = x[0]
                    dt = (x[1] / xlen)
                    x = x[2:]

                    sumVal = 0

                    freq = float(tp)
                    for m in x:
                        if freq > 5 and freq < 1000:  ## TUTAJ BEDZIE TRZEBA ZROVBC ZMIENNE ZAKRESY W ZALEZNOSCI OD STATKU / URZADZENIA / NORMY
                            sumVal += pow(m, 2)
                        freq += float(dt)
                    overall = round(sqrt(sumVal), 3)
                    querry = "UPDATE measurements_low set value = "+str(overall)+" where raport_number = '" + str(
                        rn) + "' and id = " + str(id) + " and type = 'RMS' and point = '" + str(point[0]) + "'"
                    q_run(connD,querry)

            def checkreminder():
                querry = """select rem.id,max(ml.date),rem.raport_number from reminder as rem
                        left join measurements_low as ml on ml.id = rem.id 
                        where rem.parent = """+str(parent)+"""and status is distinct from 2
                        group by rem.id,rem.raport_number"""

                for i in q_run(connD,querry):
                    for  j in measlist:
                        if str(i[0]) == str(j.id):
                            if str(i[1]) < str(j.date):

                                querry = "UPDATE reminder set status = 2 where  id = " + str(i[0])
                                q_run(connD,querry)
                                break

            def checkvsg():
                querry = "select dev.id from devices dev where dev.parent = {} and standard_fkey = 45".format(parent)
                VSGidslist = column(list(q_run(connD,querry)),0)
                return VSGidslist

            def countVSG(chartstr,type):
                range = [0,0]
                if str(type) == 'Dis':
                   range = [2,10]
                elif str(type) == 'Vel':
                    range = [10, 250]
                elif str(type) == 'Acc':
                    range = [250, 1000]


                chartlist = chartstr.split(';')
                df = float(chartlist[0])
                f0 = df
                fmax = float(chartlist[1])
                xlines = chartlist[2:]
                f = f0
                sum = 0
                for mm in xlines:
                    if f >= range[0] and f <= range[1] :

                        sum += math.pow( float(mm), 2 )

                    f += df
                sum = math.sqrt(sum)
                if str(type) == 'Dis':
                    if sum <= 17.8:
                        VSG = 1.1
                    elif sum <= 28.3 :
                        VSG = 1.8
                    elif sum <= 44.8 :
                        VSG = 2.8
                    elif sum <= 71.1 :
                        VSG = 4.5
                    elif sum <= 113 :
                        VSG = 7.1
                    elif sum <= 178 :
                        VSG = 11
                    elif sum <= 283:
                        VSG = 18
                    elif sum <= 448:
                        VSG = 28
                    elif sum <= 710:
                        VSG = 45
                    elif sum <= 1125:
                        VSG = 71
                    elif sum <= 1784:
                        VSG = 112
                    else:
                        VSG = 180
                if str(type) == 'Vel':
                    if sum <= 1.12:
                        VSG = 1.1
                    elif sum <= 1.78:
                        VSG = 1.8
                    elif sum <= 2.82 :
                        VSG = 2.8
                    elif sum <= 4.46 :
                        VSG = 4.5
                    elif sum <= 7.07 :
                        VSG = 7.1
                    elif sum <= 11.2 :
                        VSG = 11
                    elif sum <= 17.8:
                        VSG = 18
                    elif sum <= 28.2:
                        VSG = 28
                    elif sum <= 44.6:
                        VSG = 45
                    elif sum <= 70.7:
                        VSG = 71
                    elif sum <= 112:
                        VSG = 112
                    else:
                        VSG = 180
                if str(type) == 'Acc':
                    if sum <= 1.76:
                        VSG = 1.1
                    elif sum <= 2.79 :
                        VSG = 1.8
                    elif sum <= 4.42 :
                        VSG = 2.8
                    elif sum <= 7.01 :
                        VSG = 4.5
                    elif sum <= 11.1 :
                        VSG = 7.1
                    elif sum <= 17.6 :
                        VSG = 11
                    elif sum <= 27.9:
                        VSG = 18
                    elif sum <= 44.2:
                        VSG = 28
                    elif sum <= 70.1:
                        VSG = 45
                    elif sum <= 111:
                        VSG = 71
                    elif sum <= 176:
                        VSG = 112
                    else:
                        VSG = 180
                return VSG

            def getvsg(meas,chartstr):
                return countVSG(chartstr,meas.type)

            VSGidslist = checkvsg()

            checkreminder()

            Window.withdraw()

            pbar = tk.Tk()
            pbar.title("Uploading Measurements")
            progress_bar = ttk.Progressbar(pbar, orient='horizontal', lengt=286, mode='determinate')

            progress_bar['maximum'] = len(measlist)
            progress_bar.pack()

            p = 0
            OveCount = 0

            for i in measlist:

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
                    if i.id in VSGidslist:
                        VSG = getvsg(i,chartstr)
                        if str(i.type) == 'Dis': VT = 'VSGD'
                        elif str(i.type) == 'Vel': VT = 'VSGV'
                        elif str(i.type) == 'Acc': VT = 'VSGA'
                        VSGquerry = "INSERT INTO measurements_low(parent,id,point,raport_number, date, type, unit, value)" \
                                    " VALUES ({},{},'{}','{}','{}','{}','{}','{}')".format(str(parent),str(i.id),str(i.point),
                                                               str(rnumber),str(i.date),
                                                               VT,'VSG',VSG)
                        q_run(connD, VSGquerry)
                if i.mode == 'Overall':
                    OveCount += 1

                    if str(parent) == '150' and str(i.type) == 'envelope P-K':
                        i.unit = '[gE]'
                        i.overall = round(i.overall / 10,3)

                    querry = "INSERT INTO measurements_low(parent,id, point, raport_number, date, type, unit, value) VALUES (" + str(
                        parent) + "," + str(i.id) + ",'" + str(i.point) + "','" + str(rnumber) + "','" + str(
                        i.date) + "','" + str(i.type) + "','" + str(i.unit) + "','" + str(i.overall) + "')"
                if i.mode == 'TIM':
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

                    if i.type == 'Vel': taskid = 4
                    tasksetup =  ((i.unit).replace('[', '')).replace(']', '')

                    # taskid = 4
                    # tasksetup = m/s2
                    querry = """
                    INSERT INTO meascharts(shipid,id,point,report_number,date,domain,type,unit,chart,m_tasks_chart_fkey, m_tasks_setup[0])
                    VALUES ({},{},'{}','{}','{}','{}','{}','{}','{}','{}','{}')
                    """.format(parent,i.id,i.point,rnumber,i.date,i.domain,i.type,i.unit,chartstr,taskid,tasksetup)


                q_run(connD, querry)

                try:
                    chartstrlist.clear
                    del chartstr
                except:
                    x = 1

            if str(parent) == '54': #ILOAR
                listaid = ['18117', '18115', '18113', '18123', '18121', '18105', '18103', '18101', '18111', '18109','18107']
                p = 0
                for id in listaid:
                    p += 1
                    recountoverall(id,rnumber)
                    progress_bar['value'] = p
                    progress_bar.update()

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
            if x.type != 'UNKNOWN':
                mylist.insert(END,
                              str(x.routename) + ' ' + str(x.point) + ' ' + str(x.mode) + ' ' + str(x.overall) + ' ' + str(
                                  x.type) + ' ' + str(x.date))
                check_routename(x, ycord)
                ycord += 1
            else:
                x.checked = True
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



    measlist = list()
    get_meas()

    window_crosstable()

# 'Vibscanner'
# 'Marvib'
# 'ezThomas'
read_measurement_file('Marvib','testuser','info','192.168.10.243','TIMINGTEST', '299')