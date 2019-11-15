from tkinter import Tk
from tkinter import filedialog
import pandas as pd
from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import os
def fft_from_timing():
    Tk().withdraw()
    a = filedialog.askopenfilename()

    f = open(a, "r")
    lines = f.read().split("\n")  # \n" if needed
    meas = list()
    startcollect = False
    for lc,line in enumerate(lines):
        sline = line.split("\t")
        if startcollect == True:
            if str(line).strip() == '':
                break
            meas.append([str(sline[0]).replace(',','.'), str(sline[1]).replace(',','.')])

        if startcollect == False:
            if len(sline) >= 2:
                if str(sline[0]).strip() == 'ms' and str(sline[1]).strip() == 'Nm':
                    startcollect = True
            # except IndexError:
            #     pass

    data = pd.DataFrame(meas, columns=["timing", "value"])
    data['timing'] = pd.to_numeric(data['timing'])
    data['value'] = pd.to_numeric(data['value'])
    fs = round(max(data['timing']) / (data['timing'][1] - data['timing'][0]), 5)
    y = data['value']
    t = data['timing']

    yfft = abs(ifft(y))
    to = (len(yfft) / 2)
    yfft = yfft[0:int(to)]
    fftdata = pd.Series(meas, name ="magnitude")
    fig = plt.figure(figsize=(8, 6))

    ax = fig.add_subplot(211)
    ax.plot(t, y, 'b-', label='data')

    ax = fig.add_subplot(212)
    ax.plot(yfft, 'b-', label='data')
    cursor = Cursor(ax, useblit=True, color='red', linewidth=1)
    f = filedialog.askdirectory()
    path = (f + "/output.xlsx")
    fftdata.to_excel(path)

    plt.show()



fft_from_timing()