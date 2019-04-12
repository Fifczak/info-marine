
from tkinter import filedialog
import csv
import operator
from math import pow
import math

a = filedialog.askopenfilename()
#f = open(a, ",")
#lines = f.read().split("\n") # "\r\n" if needed


with open(a, newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	CrankshaftAngle = list()
	pressure = list()
	pressures = []

	for row in spamreader:
		samples = len(row)
		break
	samplesY = 0

	
	
		
	for i in range(samples):
		pressures.append([])
		for j in range(720):
			pressures[i].append(' ')
	r = -1
	for row in spamreader:
		r+=1
		pressure.clear()
		c = -1
		for col in row:
			c+=1
			pressures[c][r] = (round(float(col),3))
			

	s =0
	maxindexlist = list()
	for sample in pressures:
		s += 1
		if s != 1:
			templist = list()
			templist.clear()
			

			for item in sample:
				if item != ' ' :
					try:
						templist.append((item))
					except:
						pass
			max_value = max(templist)
			max_index = templist.index(max_value)
			if max_index > 600:
				max_index = 670 - max_index
			else:
				max_index = 310 - max_index
			max_index = max_index
			maxindexlist.append(max_index)
	mean = (round(sum(maxindexlist) / len(maxindexlist),1 ))
	maxv =  max(maxindexlist)
	minv =  min(maxindexlist)
	#print(maxindexlist)
	#sumakwadratow
	SK = 0
	for index in maxindexlist:
		SK += pow(index-mean,2)

	stdev = round(math.sqrt((SK)/(len(maxindexlist))),1)
	
	
	
	print('Mean = ' + str(mean))	
	print('High = ' + str(maxv))	
	print('Min = ' + str(minv))	
	print('Spread = ' + str(maxv - minv))	
	print('SD = ' + str(stdev))	
#print(CrankshaftAngle)