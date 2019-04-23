##2131231232
import sys
import datetime
import os
import os.path
import time

import matplotlib.pyplot as plt

from docx import Document
from docx.shared import Inches
from docx.shared import Pt
from docx.shared import RGBColor

from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.text import WD_BREAK
from docx.enum.text import WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER

from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *

from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

import numpy as np	
from report_styles import loadstyles	
from report_headtables import *
from report_frontpages import *
from report_resulttables import prepare_IM, drawtable_IM
from report_standards import standards, legend_IM
from report_signature import signature

username = 'postgres'
password = 'info'
host = 'localhost'
connD = [username,password,host]
def q_run(connD, querry):
	username = connD[0]
	password = connD[1]
	#cs = (host="localhost"  , dbname="postgres" , user= "postgres" , password="info")
	#cs = "dbname=%s user=%s password=%s host=%s port=%s"%(kdb,username,password,host,kport)
	conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="info")
	cur = conn.cursor()
	cur.execute(querry)
	try:
		result = cur.fetchall()
		return result
	except:
		pass
	conn.commit()
	cur.close()
rn_='1987-2019'
querry = "Select parent from measurements_low where raport_number = '" + rn_ + "' limit 1"
parent = q_run(connD,querry)
querry = """select 
					 ml.id, ml.raport_number, dev.name,  max(ml.value) as RMS, ml2.max as Envelope, dev.norm ,ml.date, dev.drivenby,dss.sort
					from measurements_low as ml
					left join (select 
								 ml.id, ml.raport_number,  max(ml.value)
								 from measurements_low as ml
								 where type = 'envelope P-K' and parent = """ + str(parent[0][0]) + """
								 group by id,raport_number order by raport_number DESC) as ml2 on ml.id = ml2.id and ml.raport_number = ml2.raport_number
					 left join devices as dev on ml.id = dev.id
					 left join(select cast (id as integer), sort from ds_structure where id ~E'^\\\d+$' ) as dss on ml.id = dss.id
					 where ml.type = 'RMS' and ml.parent = """ + str(parent[0][0]) + """
					 group by ml.id, ml.raport_number, ml2.max,dev.name, dev.norm,ml.date,dev.drivenby,dss.sort order by raport_number DESC"""
reportresults = q_run(connD, querry)
def getTrend (self):
	trendlist = list()
	for line in reportresults:
		if str(line[0]) == str(self.id):
			if str(line[1]) != str(report_number):
				newdate = time.strptime(str(line[6]), "%Y-%m-%d")
				mydate = time.strptime(str(self.date), "%Y-%m-%d")
				if newdate < mydate:
					trendlist.append(str(line[3]))  # VAL
					trendlist.append(str(line[6]))  # DATE

					change = abs((float(line[3]) - float(self.maxval)) / float(line[3]))

					if change <= 0.05:
						TREND = 'C'

					if float(line[3]) < float(self.maxval):
						TREND = 'U'

					if float(line[3]) > float(self.maxval):
						TREND = 'D'

					trendlist.append(TREND)  # TREND=> U-UP, D-DOWN, C-CONST
					break
	self.trend = trendlist
	return measlist

# TRZEBA PRZEMYSLEC W JAKI SPOSOB BĘDĄ WYBIERANE DANE DO TWORZENIA RAPORTÓW
fileformattype = 1 # 1 - IM; 2 - KAMTRO ; 3-Stocznia Remontowa
headtabletype = 1 # 1 - IM; 2 - KAMTRO
frontpagetype = 1 

	
resulttable = 1 # 1 - IM;	
	
def makereport(connD,rn_):
	username = connD[0]
	password = connD[1]
	host = connD[2]
	#PRZYGOTOWANIE TEMPLATA DO GENEROWANIA RAPORTU
	#dodana formatka do remontowej
	if fileformattype == 1:
		filepath = 'C:\\overmind\\Data\\baseIM.docx'
	if fileformattype == 2:
		filepath = 'C:\\overmind\\Data\\baseKAM.docx'
	if fileformattype==3:
		filepath='C:\\overmind\\Data\\baseGSR.docx'
	document = Document(filepath)
	loadstyles(document) 
	rn_ = str(rn_)
	
	#wybór headtable IM/Kamtro
	if headtabletype == 1:
		standard_info_table(connD,document,rn_)
	if headtabletype == 2:
		standard_Kamtro_table(document)
	#wybór rodzaju raportu (pms/charts etc)
	#P2 = document.add_paragraph('02. FRONT PAGE (put front page text here)')
	if frontpagetype == 1:
		standard_PMS_limit(document)

	document.add_paragraph()

	#P3 = document.add_paragraph('03. STANDARDS (put informations about standards here)')
	standards(document)
	if headtabletype==1:
		legend_IM(document)

	if headtabletype==2:
		legend_KAMTRO(document)


	#prepare_IM(connD, '1987-2019')
	#getTrend(shipstr)
	#rawtable_IM(document, measlist, connD, report_number)



	if resulttable == 1:
		measlist = prepare_IM(connD,rn_)
		drawtable_IM(document,measlist,connD,rn_)
	
	P5 = document.add_paragraph('05. MEASUREMENT EQUIPMENT (put information about measurement equipment here)')
	P6 = document.add_paragraph('06. SUMMARY (put summary informations here)')
	P7 = document.add_paragraph('07. SIGNATURES (put company / personal informations here)')

	signature(document)
	appr=document.add_paragraph()
	appr.alignment=WD_ALIGN_PARAGRAPH.RIGHT
	appr.add_run('Approved by: ')
	document.save('C:\overmind\Reports\TEST SIEM '+rn_+'.docx')

##########################################



makereport(connD,'1987-2019')
os.startfile('C:\overmind\Reports\TEST SIEM 1987-2019.docx')