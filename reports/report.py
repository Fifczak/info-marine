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
from report_resulttables import *



# TRZEBA PRZEMYSLEC W JAKI SPOSOB BĘDĄ WYBIERANE DANE DO TWORZENIA RAPORTÓW
fileformattype = 1 # 1 - IM; 2 - KAMTRO
headtabletype = 1 # 1 - IM; 2 - KAMTRO
frontpagetype = 1 

	
resulttable = 1 # 1 - IM;	
	
def makereport(connD,rn_):
	username = connD[0]
	password = connD[1]
	host = connD[2]
	#PRZYGOTOWANIE TEMPLATA DO GENEROWANIA RAPORTU
	
	if fileformattype == 1:
		filepath = 'C:\\overmind\\Data\\baseIM.docx'
	if fileformattype == 2:
		filepath = 'C:\\overmind\\Data\\baseKAM.docx'
	document = Document(filepath)
	loadstyles(document) 
	rn_ = str(rn_)
	
	#P1 = document.add_paragraph('01. HEADER (put table with report informations here)')
	if headtabletype == 1:
		standard_info_table(connD,document,rn_)
	if headtabletype == 2:
		standard_Kamtro_table(document)
	
	
	#P2 = document.add_paragraph('02. FRONT PAGE (put front page text here)')
	if frontpagetype == 1:
		standard(document)
	
	P3 = document.add_paragraph('03. STANDARDS (put informations about standards here)')
	P4 = document.add_paragraph('04. RESULTS (present results here)')
	if resulttable == 1:
		measlist = prepare_IM(connD,rn_)
		drawtable_IM(document,measlist,connD,rn_)
	
	P5 = document.add_paragraph('05. MEASUREMENT EQUIPMENT (put information about measurement equipment here)')
	P6 = document.add_paragraph('06. SUMMARY (put summary informations here)')
	P7 = document.add_paragraph('07. SIGNATURES (put company / personal informations here)')
	
	
	

	document.save('C:\overmind\Reports\TEST.docx')
##########################################


username = 'asdasdasd'
password = 'XXX'
host = '192.168.8.125'
connD = [username,password,host]
makereport(connD,'1746U-2018')



