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
from docx.enum.table import WD_ALIGN_VERTICAL

from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

from report_database import *

#używana wszędzie w raportach IM
def standard_info_table(connD, document,rn_):
	username = connD[0]
	password = connD[1]
	host = connD[2]
	querry = "select main.name, shd.imo, main2.name from main right join shipsdata as shd on main.id = shd.shipid right join main as main2 on main.parent = main2.id where main.id = (select shipid from reports where raport_number = '1987-2019')"
	result = q_run(connD, querry)

	print (str(result)+'rn: '+str(rn_))
	shipstr=result[0][0]
	print(shipstr)
	headtable = document.add_table(rows=2, cols=3)#trzeba usunąć enter przed

	#querry='select reporttype from main where name="%s"'%(shipstr)
	#conn=psycopg2.connect(dbname='postgres',user='postgres',password='info')
	#cur=conn.cursor()
	#cur.execute(querry)
	#parent_=cur.fetchall()


	headtable.style = 'Table Grid'
	headtable.cell(0,0).merge(headtable.cell(0,1).merge(headtable.cell(0,2)))
	ht= headtable.cell(0,0).paragraphs[0]
	ht.alignment = WD_ALIGN_PARAGRAPH.CENTER
	r0 = ht.add_run()
	r0.text='Vibration diagnostic report '
	r0.font.name='Calibri'
	r0.font.size=Pt(12)
	r1 = ht.add_run(rn_)
	r1.bold = True
	r1.font.name='Calibri'

	ht = headtable.cell(1,0).paragraphs[0]
	ht.alignment = WD_ALIGN_PARAGRAPH.LEFT


	r0 = ht.add_run('Project: ')
	r0.font.name='Calibri'
	r1 = ht.add_run(shipstr)
	r1.bold = True
	r1.font.name='Calibri'

	imostr = str(result[0][1])
	ht = headtable.cell(1,0).add_paragraph()
	r0 = ht.add_run('IMO no: ')
	r0.font.name = 'Calibri'
	r1 = ht.add_run(imostr)
	r1.font.name = 'Calibri'
	r1.bold = True


	ownerstr = str(result[0][2])
	ht = headtable.cell(1,0).add_paragraph()
	r0 = ht.add_run('Ordered by: ')
	r0.font.name = 'Calibri'
	r1 = ht.add_run(ownerstr)
	r1.bold = True
	r1.font.name = 'Calibri'
	ht = headtable.cell(1,1).paragraphs[0]
	r0 = ht.add_run('Date of measurement: ')
	r0.font.name = 'Calibri'
	headtable.cell(1, 1).add_paragraph()

	ht.alignment = WD_ALIGN_PARAGRAPH.CENTER
	ht.vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
	ht = headtable.cell(1,1).add_paragraph()

	ht.alignment = WD_ALIGN_PARAGRAPH.CENTER
	ht.vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
	r0 = ht.add_run('XXXX-XX-XX')
	r0.bold=True
	r0.font.name = 'Calibri'
	ht = headtable.cell(1,2).paragraphs[0]
	ht.alignment = WD_ALIGN_PARAGRAPH.CENTER
	r0 = ht.add_run('Place of measurement:')
	r0.font.name = 'Calibri'

	headtable.cell(1, 2).add_paragraph()
	ht = headtable.cell(1,2).add_paragraph()
	ht.alignment = WD_ALIGN_PARAGRAPH.CENTER
	r0 = ht.add_run('During normal operation')
	r0.bold=True
	r0.font.name = 'Calibri'
	section=document.sections[0]
	footer=section.footer
	footer.add_paragraph(shipstr+' '+rn_)
	footer.alignment=WD_ALIGN_PARAGRAPH.LEFT
	footer.alignment_vertical=WD_ALIGN_VERTICAL.TOP


#tabela początkowa kamtro
def standard_Kamtro_table(document):
	headtable = document.add_table(rows=3, cols=2)
	headtable.cell(0,0).add_paragraph('KAMTRO KAMTRO KAMTRO: ','texthead')
	headtable.cell(0,0).alignment = WD_ALIGN_PARAGRAPH.LEFT
