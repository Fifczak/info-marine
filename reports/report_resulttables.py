import psycopg2
import time
from docx import Document
from report_database import *
def prepare_IM(connD,report_number):
	measlist = list()
	class meas(object):
		def __init__(self):
			self.id =''
			self.name=''
			self.maxval=''
			self.maxval2=''
			self.limit=''
			self.maxenv=''
			self.trend=list()
			self.standard =''
			self.date =''
			self.drivenby=''
	def loadData(connD):
		def countLimit(standard,value):	
			for limNo in limits:
				if str(limNo[0]) == str(standard):
					if value <= float(limNo[3]): #IF LIM1
						limSrt = str(limNo[2])
						break
					else:
						if value <=float(limNo[5]): #IF LIM2
							limSrt = str(limNo[4])
							break
						else:
							if value <=float(limNo[7]): #IF LIM3
								limSrt = str(limNo[6])
								break
							else:
								limSrt = str(limNo[8])
								break
				
			return limSrt
		def getTrend(self):
			trendlist = list()
			for line in reportresults:
				if str(line[0]) == str(self.id):
					if str(line[1]) != str(report_number):
						newdate = time.strptime(str(line[6]), "%Y-%m-%d")
						mydate = time.strptime(str(self.date), "%Y-%m-%d")
						if newdate < mydate:
							trendlist.append(str(line[3])) #VAL
							trendlist.append(str(line[6])) #DATE
							
							change = abs((float(line[3])-float(self.maxval))/float(line[3]))
							
							if change <= 0.05:
								TREND = 'C'
								
							if float(line[3]) < float(self.maxval):
								TREND = 'U'
								
							if float(line[3]) > float(self.maxval):
								TREND = 'D'
								
						
							
							trendlist.append(TREND) #TREND=> U-UP, D-DOWN, C-CONST
							break
			self.trend = trendlist	
		querry = "Select parent from measurements_low where raport_number = '" + str(report_number) + "' limit 1"
		parent = q_run(connD,querry)[0][0]
	
		querry = """select standard,
							limit_1_value,limit_1_name,
							limit_2_value,limit_2_name, 
							limit_3_value,limit_3_name,
							limit_4_value,limit_4_name,
						envflag
					from standards"""
		limits = q_run(connD,querry)			
		querry = """select 
					 ml.id, ml.raport_number, dev.name,  max(ml.value) as RMS, ml2.max as Envelope, dev.norm ,ml.date, dev.drivenby
					from measurements_low as ml
					left join (select 
								 ml.id, ml.raport_number,  max(ml.value)
								 from measurements_low as ml
								 where type = 'envelope P-K' and parent = """ + str(parent) + """
								 group by id,raport_number order by raport_number DESC) as ml2 on ml.id = ml2.id and ml.raport_number = ml2.raport_number
					 left join devices as dev on ml.id = dev.id
					 where ml.type = 'RMS' and ml.parent = """ + str(parent) + """
					 group by ml.id, ml.raport_number, ml2.max,dev.name, dev.norm,ml.date,dev.drivenby order by raport_number DESC"""
		reportresults = q_run(connD, querry)
		
		for line in reportresults:
			x = meas()
			if str(line[1]) == str(report_number):
				x.id =line[0]
				x.name=line[2]
				x.maxval=line[3]
				x.maxenv=line[4]
				x.standard=line[5]
				x.date=line[6]
				getTrend(x)
				x.limit = countLimit(x.standard,x.maxval)
				x.drivenby=line[7]
				measlist.append(x)

	loadData(connD)	
	return measlist
	maxval
def	drawtable_IM(document,measlist,connD,report_number):#):
	querry = "Select parent from measurements_low where raport_number = '" + str(report_number) + "' limit 1"
	parent = q_run(connD,querry)[0][0]
	querry = "Select sort, id from ds_structure where parent = '" + str(parent) + "' order by sort"
	sortlistQ = q_run(connD,querry)
	trueMeasList = list()
	activeIdList = list()
	idlist = list()
	drivenByList = list()
	for sort in sortlistQ:
		for meas in measlist:
			if (sort[1]).isdigit == False:
				trueMeasList.append('header')
				drivenByList.append(997)
				idlist.append(997)
			if str(sort[1])==str(meas.id):
				trueMeasList.append(meas)
				activeIdList.append(str(meas.id))

				drivenByList.append(meas.drivenby)
				idlist.append(meas.id)

	counter = 0
	counterCharts = 0
	i=-1
	for measStrip in sortlistQ:  #ILOSC WIERSZY
		i += 1
		if (measStrip[1]).isdigit() == False:
			if measStrip[0][-5:] == '00.00' and sortlistQ[i+1][0][-5:] != '00.00' and sortlistQ[i+1][0][-3:] == '.00':
				counter +=1
				continue
			if measStrip[0][-5:] != '00.00' and measStrip[0][-3:] == '.00' :
				if str(sortlistQ[i+1][1]) in activeIdList:
					counter +=1
					continue
		else:	
			for xx in trueMeasList:
				if str(measStrip[1]) == str(xx.id):
					counter +=1
					if str(xx.drivenby) in activeIdList:
						counterCharts +=1
						break
					else:
						break
	
	rowscount = (counter*2) - counterCharts +100
	resulttable = document.add_table(rows=rowscount+1, cols=7)
	resulttable.style = 'Table Grid'
	
	ht= resulttable.cell(0,0).paragraphs[0]
	r0 = ht.add_run('Nazwa urządzenia')

	ht= resulttable.cell(0,1).paragraphs[0]
	r0 = ht.add_run('Prędkość RMS (mm/s) Freq A Max')
	
	ht= resulttable.cell(0,2).paragraphs[0]
	r0 = ht.add_run('Prędkość RMS (mm/s) Freq B Max')
		
	ht= resulttable.cell(0,3).paragraphs[0]
	r0 = ht.add_run('ISO/VDI standard')
	
	ht= resulttable.cell(0,4).paragraphs[0]
	r0 = ht.add_run('Obwiednia łożysk 0-Peak (gE) Max')
	
	ht= resulttable.cell(0,5).paragraphs[0]
	r0 = ht.add_run('Prędkość RMS Max (mm/s) Trend')
	
	ht= resulttable.cell(0,6).paragraphs[0]
	r0 = ht.add_run('Uwagi i sugestie')
	
	xcord = 0
	i=-1
	for measStrip in sortlistQ: 
		i += 1
		print(measStrip[0])
		if (measStrip[1]).isdigit() == False:######## NAGŁÓWKI
			try:
				ht= resulttable.cell(xcord+1,0).paragraphs[0]
				if measStrip[0][-5:] == '00.00' and sortlistQ[i+1][0][-5:] != '00.00' and sortlistQ[i+1][0][-3:] == '.00':
					xcord += 1
					r0 = ht.add_run('PLACE')#measStrip[1])
					resulttable.cell(xcord,0).merge(resulttable.cell(xcord,6))
					
					continue
				if measStrip[0][-5:] != '00.00' and measStrip[0][-3:] == '.00' :
					if str(sortlistQ[i+1][1]) in activeIdList:
						xcord += 1
						r0 = ht.add_run('GROUP')#measStrip[1])
						resulttable.cell(xcord,0).merge(resulttable.cell(xcord,6))
						
						continue
			except:
				pass
		else:	######## POMIARY
			p=-1
			#drivenByList.append('0') # zeby nie bylo bledu na koncu petli
			for xx in trueMeasList:
				p+=1
				if str(measStrip[1]) == str(xx.id):

					ht = resulttable. cell(xcord+1,0).paragraphs[0]
					r0 = ht.add_run(xx.name)
					ht = resulttable. cell(xcord+1,1).paragraphs[0]
					r0 = ht.add_run(str(xx.maxval))
					ht = resulttable. cell(xcord+1,2).paragraphs[0]
					r0 = ht.add_run(str(xx.maxval2))
					ht = resulttable. cell(xcord+1,3).paragraphs[0]
					r0 = ht.add_run(str(xx.limit))
					ht = resulttable. cell(xcord+1,4).paragraphs[0]
					r0 = ht.add_run(str(xx.maxenv))			
					ht = resulttable. cell(xcord+1,5).paragraphs[0]
					if  str(xx.limit) == 'Cl. D':   #TEGO DLA CZYTELNOSCI LEPIEJ ZROBIC FUNKCJE
						try:
							trendtemp1 = xx.trend[0]
							trendtemp2 = xx.trend[1]
							trendtemp3 = xx.trend[2]
						
							if str(trendtemp3) == 'U':
								r0 = ht.add_run()
								r0.add_picture('up.gif')
							elif str(trendtemp3) == 'D':
								r0 = ht.add_run()
								r0.add_picture('down.gif')
							elif str(trendtemp3) == 'C':
								r0 = ht.add_run()
								r0.add_picture('none.gif')
							p0 = ht.add_run('\nOstatnia Wartość:')
							p0 = ht.add_run('\n' + str(trendtemp2))
							p0 = ht.add_run('\n' + str(trendtemp1))
						except:
							pass
					

					try:
						if str(drivenByList[p+1]) == str(xx.id):
							xcord += 1
						else:
							xcord += 2
						break
					except:
						break
					
def	drawtable_STOCZNIA_REMONTOWA(document,measlist,connD,report_number):#):trzeba troche ukrocic
	querry = "Select parent from measurements_low where raport_number = '" + str(report_number) + "' limit 1"
	parent = q_run(connD,querry)[0][0]
	querry = "Select sort, id from ds_structure where parent = '" + str(parent) + "' order by sort"
	sortlistQ = q_run(connD,querry)
	trueMeasList = list()
	activeIdList = list()
	for sort in sortlistQ:
		for meas in measlist:
			if (sort[1]).isdigit == False:
				trueMeasList.append('header')
			if str(sort[1])==str(meas.id):
				trueMeasList.append(meas)
				activeIdList.append(str(meas.id))
	counter = 0
	counterCharts = 0
	i=-1
	for measStrip in sortlistQ:  #ILOSC WIERSZY
		i += 1
		if (measStrip[1]).isdigit() == False:
			if measStrip[0][-5:] == '00.00' and sortlistQ[i+1][0][-5:] != '00.00' and sortlistQ[i+1][0][-3:] == '.00':
				counter +=1
				continue
			if measStrip[0][-5:] != '00.00' and measStrip[0][-3:] == '.00' :
				if str(sortlistQ[i+1][1]) in activeIdList:
					counter +=1
					continue
		else:	
			for xx in trueMeasList:
				if str(measStrip[1]) == str(xx.id):
					counter +=1
					if str(xx.drivenby) in activeIdList:
						counterCharts +=1
						break
					else:
						break
	
	rowscount = (counter*2) - counterCharts
	resulttable = document.add_table(rows=rowscount+1, cols=7)
	resulttable.style = 'Table Grid'
	
	ht= resulttable.cell(0,0).paragraphs[0]
	r0 = ht.add_run('Nazwa urządzenia')

	ht= resulttable.cell(0,1).paragraphs[0]
	r0 = ht.add_run('Prędkość RMS (mm/s) Freq A Max')
	
	ht= resulttable.cell(0,2).paragraphs[0]
	r0 = ht.add_run('Prędkość RMS (mm/s) Freq B Max')
		
	ht= resulttable.cell(0,3).paragraphs[0]
	r0 = ht.add_run('ISO/VDI standard')
	
	ht= resulttable.cell(0,4).paragraphs[0]
	r0 = ht.add_run('Obwiednia łożysk 0-Peak (gE) Max')
	
	ht= resulttable.cell(0,5).paragraphs[0]
	r0 = ht.add_run('Prędkość RMS Max (mm/s) Trend')
	
	ht= resulttable.cell(0,6).paragraphs[0]
	r0 = ht.add_run('Uwagi i sugestie')
	
	xcord = 0
	i=-1
	for measStrip in sortlistQ: 
		i += 1
		if (measStrip[1]).isdigit() == False:######## NAGŁÓWKI
			try:
				ht= resulttable.cell(xcord+1,0).paragraphs[0]
				if measStrip[0][-5:] == '00.00' and sortlistQ[i+1][0][-5:] != '00.00' and sortlistQ[i+1][0][-3:] == '.00':
					r0 = ht.add_run(measStrip[1])
					resulttable.cell(xcord+1,0).merge(resulttable.cell(xcord+1,6))
					xcord += 1
					continue
				if measStrip[0][-5:] != '00.00' and measStrip[0][-3:] == '.00' :
					if str(sortlistQ[i+1][1]) in activeIdList:
						r0 = ht.add_run(measStrip[1])
						resulttable.cell(xcord+1,0).merge(resulttable.cell(xcord+1,6))
						xcord += 1
						continue
			except:
				pass
		else:	######## POMIARY
			for xx in trueMeasList:

			
			
				if str(measStrip[1]) == str(xx.id):
					if str(xx.drivenby) == '0':# tu nie dosc ze robi przed to nie rozwiazuje jak nie ma urzadzenia wskazanego przez driven by
						xcord += 1 
					ht = resulttable. cell(xcord+1,0).paragraphs[0]
					r0 = ht.add_run(xx.name)
					ht = resulttable. cell(xcord+1,1).paragraphs[0]
					r0 = ht.add_run(str(xx.maxval))
					ht = resulttable. cell(xcord+1,2).paragraphs[0]
					r0 = ht.add_run(str(xx.maxval2))
					ht = resulttable. cell(xcord+1,3).paragraphs[0]
					r0 = ht.add_run(str(xx.limit))
					ht = resulttable. cell(xcord+1,4).paragraphs[0]
					r0 = ht.add_run(str(xx.maxenv))			
					ht = resulttable. cell(xcord+1,5).paragraphs[0]
					if  str(xx.limit) == 'Cl. D':   #TEGO DLA CZYTELNOSCI LEPIEJ ZROBIC FUNKCJE
						try:
							trendtemp1 = xx.trend[0]
							trendtemp2 = xx.trend[1]
							trendtemp3 = xx.trend[2]
						
							if str(trendtemp3) == 'U':
								r0 = ht.add_run()
								r0.add_picture('up.gif')
							elif str(trendtemp3) == 'D':
								r0 = ht.add_run()
								r0.add_picture('down.gif')
							elif str(trendtemp3) == 'C':
								r0 = ht.add_run()
								r0.add_picture('none.gif')
							p0 = ht.add_run('\nOstatnia Wartość:')
							p0 = ht.add_run('\n' + str(trendtemp2))
							p0 = ht.add_run('\n' + str(trendtemp1))
						except:
							pass
					xcord += 1
					break