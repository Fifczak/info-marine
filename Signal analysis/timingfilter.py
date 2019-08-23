#FIFCZAK BASICS
import psycopg2
import pandas as pd
from scipy.fftpack import fft, ifft
connD=['filipb','@infomarine','192.168.10.243']
#connD=['filipb','@infomarine','192.168.10.243']
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
###
import json
from pandas.io.json import json_normalize
from tqdm import tqdm
from tkinter import Tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import csv

import numpy as np
import wavio
from tkinter import Tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt

import filetype
from matplotlib.widgets import Cursor


Tk().withdraw()

a = filedialog.askopenfilename()
kind = filetype.guess(a)





data = pd.DataFrame(columns = ["timing", "value"])

fs = 0
ext = None
try:
	ext = str(kind.extension)
except:
	ext = None


if ext == 'wav':

	testfile = wavio.read(a)
	testfile.data[:, 0]
	wavlist = list(testfile.data[:, 0])
	# 0.620
	bytemaxval = max(wavlist)
	realmaxval = float(input("Max peak on signal: "))
	WTFparameter = realmaxval / bytemaxval
	WTFparameter
	yvals = list()
	for line in wavlist:
		yvals.append(round(line * WTFparameter, 3))
	time = np.arange( 0 , len(wavlist)/testfile.rate, ((len(wavlist)/testfile.rate)/len(wavlist)) )
	time = [round(item,5) for item in time]
	data = pd.DataFrame(list(zip(time, yvals)),  columns = ['timing' , 'value'])

	fs = 1 / ((len(wavlist)/testfile.rate)/len(wavlist))

else:
	f = open(a, "r")
	lines = f.read().split("\n")  # \n" if needed
	meas = list()
	for line in lines:
		sline = line.split("\t")
		try:
			meas.append([sline[1],sline[2]])
		except:
			pass
	data = pd.DataFrame(meas, columns = ["timing", "value"])

	data['timing'] = pd.to_numeric(data['timing'])
	data['value'] = pd.to_numeric(data['value'])
	fs = round(max(data['timing'])/ (data['timing'][1] - data['timing'][0]),5)






from scipy.signal import butter, lfilter,filtfilt


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a
def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y
def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y


import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

# Sample rate and desired cutoff frequencies (in Hz).
#fs = (len(data))

# hcutoff = 500  ##minfreq
# lcutoff = 1000 ## maxfreq


hcutoff = int(input("Down pass frequency: "))
lcutoff = int(input("High pass frequency: "))



t = data['timing']
y = data['value']
yf = butter_lowpass_filter(y, lcutoff, fs)
yf = butter_highpass_filter(yf, hcutoff, fs)

yfft = abs(ifft(y))
to = (len(yfft)/2)
yfft = yfft[0:int(to)]

yffft = abs(ifft(yf))
tof = (len(yffft)/2)
yffft = yffft[0:int(tof)]



fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(311)
ax.plot(t, y, 'b-', label='data')
cursor = Cursor(ax, useblit=True, color='red', linewidth=1)
ax.plot(t, yf, 'g-', linewidth=2, label='filtered data')

ax2 = fig.add_subplot(312)
ax2.plot(yfft, 'b-', label='data')
cursor2 = Cursor(ax2, useblit=True, color='red', linewidth=1)


ax3 = fig.add_subplot(313)
ax3.plot(yffft, 'g-', label='data')
cursor3 = Cursor(ax3, useblit=True, color='red', linewidth=1)


plt.show()
