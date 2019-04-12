from docx import *
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

from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

from report_database import *


def standard_info_table(connD, document,rn_):
	username = connD[0]
	password = connD[1]
	host = connD[2]
	querry = "select main.name, shd.imo, main2.name from main right join shipsdata as shd on main.id = shd.shipid right join main as main2 on main.parent = main2.id where main.id = (select shipid from reports where raport_number = '1746U2-2018')"
	result = q_run(connD, querry)
	
	
	print (str(result))
	shipstr = str(result[0][0])
	
	headtable = document.add_table(rows=2, cols=3)#trzeba usunąć enter przed 
	headtable.style = 'Table Grid'
	headtable.cell(0,0).merge(headtable.cell(0,1).merge(headtable.cell(0,2)))
	
	ht= headtable.cell(0,0).paragraphs[0]
	ht.alignment = WD_ALIGN_PARAGRAPH.CENTER
	r0 = ht.add_run('Vibration diagnostic report ')
	r1 = ht.add_run(rn_)
	r1.bold = True

	ht = headtable.cell(1,0).paragraphs[0]
	ht.alignment = WD_ALIGN_PARAGRAPH.LEFT
	r0 = ht.add_run('Project ')
	r1 = ht.add_run(shipstr)
	r1.bold = True
	imostr = str(result[0][1])
	ht = headtable.cell(1,0).add_paragraph()
	r0 = ht.add_run('IMO no: ')
	r1 = ht.add_run(imostr)
	r1.bold = True
	ownerstr = str(result[0][2])
	ht = headtable.cell(1,0).add_paragraph()
	r0 = ht.add_run('Ordered by: ')
	r1 = ht.add_run(ownerstr)
	r1.bold = True
	
	ht = headtable.cell(1,1).paragraphs[0]
	ht.alignment = WD_ALIGN_PARAGRAPH.CENTER
	r0 = ht.add_run('Date of measurement:')
	
	ht = headtable.cell(1,1).add_paragraph()
	ht.alignment = WD_ALIGN_PARAGRAPH.CENTER
	r0 = ht.add_run('XXXX-XX-XX')

	ht = headtable.cell(1,2).paragraphs[0]
	ht.alignment = WD_ALIGN_PARAGRAPH.CENTER
	r0 = ht.add_run('Place of measurement:')
	
	ht = headtable.cell(1,2).add_paragraph()
	ht.alignment = WD_ALIGN_PARAGRAPH.CENTER
	r0 = ht.add_run('During normal operation')
	
	
def standard_Kamtro_table(document):
	headtable = document.add_table(rows=3, cols=2)
	headtable.cell(0,0).add_paragraph('KAMTRO KAMTRO KAMTRO: ','texthead')
	headtable.cell(0,0).alignment = WD_ALIGN_PARAGRAPH.LEFT	
