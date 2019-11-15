from tkinter import Tk
from tkinter import filedialog


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

devlist = list()
root = Tk()
root.withdraw()
a = filedialog.askopenfilename()
f = open(a, "r")
lines = f.read().split("\n")  # "\r\n" if needed
xcord = 0
meason = False
xcord = 0
for line in lines:
    xcord += 1
    if line == '#Path':
        device = (get_route_name(lines[xcord]))[0]
        if device not in devlist:
            devlist.append(device)
            print(device)

