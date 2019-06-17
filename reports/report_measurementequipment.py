from docx.enum.text import WD_BREAK
from docx.enum.text import WD_COLOR_INDEX, WD_ALIGN_PARAGRAPH
from docx.shared import Cm
from docx.shared import Pt
import psycopg2

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

def MarVibENG(document,connD,rn):
	document.add_page_break()
	summary = document.add_paragraph()
	summary.add_run('Measurement equipment:').bold = True


	shiptable = document.add_table(rows=7, cols=2)  # trzeba usunąć enter przed
	shiptable.style = 'Table Grid'
	shiptable.cell(0, 0).merge(shiptable.cell(0, 1))


	##SHIPTABLE [0,0]
	ht = shiptable.cell(0, 0).paragraphs[0]
	r0 = ht.add_run()
	r0.text = 'Technical data'

	##SHIPTABLE [1,0]
	ht = shiptable.cell(1, 0).paragraphs[0]
	r0 = ht.add_run()
	r0.text = 'Maker:'
	##SHIPTABLE [2,0]
	ht = shiptable.cell(2, 0).paragraphs[0]
	r0 = ht.add_run()
	r0.text = 'Type:'
	##SHIPTABLE [3,0]
	ht = shiptable.cell(3, 0).paragraphs[0]
	r0 = ht.add_run()
	r0.text = 'Serial number:'
	##SHIPTABLE [4,0]
	ht = shiptable.cell(4, 0).paragraphs[0]
	r0 = ht.add_run()
	r0.text = 'Calibration to:'
	##SHIPTABLE [5,0]
	ht = shiptable.cell(5, 0).paragraphs[0]
	r0 = ht.add_run()
	r0.text = 'Measuring range:'
	##SHIPTABLE [6,0]
	ht = shiptable.cell(6, 0).paragraphs[0]
	r0 = ht.add_run()
	r0.text = 'Indication error:'

	querry = "select device, serialno, caldue from equipment where lp = (select equipment from shipsdata where shipid = (select shipid from harmonogram where report_number = '" + str(rn) + "' limit 1) limit 1) limit 1"
	try:eqdata = list(q_run(connD, querry))[0]
	except: eqdata=list(['ERROR','ERROR','ERROR'])
	##SHIPTABLE [1,1]
	ht = shiptable.cell(1, 1).paragraphs[0]
	r0 = ht.add_run()
	r0.text = str('Info Marine')
	##SHIPTABLE [2,1]
	ht = shiptable.cell(2, 1).paragraphs[0]
	r0 = ht.add_run()
	r0.text = str(eqdata[0])
	##SHIPTABLE [3,1]
	ht = shiptable.cell(3, 1).paragraphs[0]
	r0 = ht.add_run()
	r0.text = str(eqdata[1])
	##SHIPTABLE [4,1]
	ht = shiptable.cell(4, 1).paragraphs[0]
	r0 = ht.add_run()
	r0.text = str(eqdata[2])

	##SHIPTABLE [5,1]
	ht = shiptable.cell(5, 1).paragraphs[0]
	r0 = ht.add_run()
	r0.text = str('2Hz-30kHz / RPM = 60-20000')
	##SHIPTABLE [6,1]
	ht = shiptable.cell(6, 1).paragraphs[0]
	r0 = ht.add_run()
	r0.text = str('±0,5%')

	ht = document.add_paragraph()
	r0 = ht.add_run()
	r0.text = str('MarVib is calibrated, certificate for verification - if required.')