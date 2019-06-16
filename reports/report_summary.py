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

def IMVibEng(document,connD,rn):
	document.add_page_break()
	#TABELKA Z PARAMETRAMI STATKU
	shiptable = document.add_table(rows=3, cols=2)  # trzeba usunąć enter przed
	shiptable.style = 'Table Grid'
	shiptable.cell(2, 0).merge(shiptable.cell(2, 1))

	querry = "select shiptype,lenght,bradth from shipsdata where shipid = (select shipid from harmonogram where report_number = '" + str(rn) + "' limit 1)"
	print(querry)
	shipdata = list(q_run( connD ,querry ))[0]
	print(shipdata)
	##SHIPTABLE [0,0]
	ht = shiptable.cell(0, 0).paragraphs[0]
	r0 = ht.add_run()
	r0.text = 'Ship type:'
	ht = shiptable.cell(0, 0).add_paragraph()
	r0 = ht.add_run()
	r0.text = str(shipdata[0])

	##SHIPTABLE [0,1]

	ht = shiptable.cell(0, 1).paragraphs[0]
	r0 = ht.add_run()
	r0.text = 'Main dimensions:'
	ht = shiptable.cell(0, 1).add_paragraph()
	r0 = ht.add_run()
	r0.text = 'Length(b.p)............................................' + str(shipdata[1]) + ' m'
	ht = shiptable.cell(0, 1).add_paragraph()
	r0 = ht.add_run()
	r0.text = 'Breadth(B.).............................................' + str(shipdata[2]) + ' m'

	##SHIPTABLE [1,0]
	ht = shiptable.cell(1, 0).paragraphs[0]
	r0 = ht.add_run()
	r0.text = 'Sea depth:'
	ht = shiptable.cell(1, 0).add_paragraph()
	r0 = ht.add_run()
	r0.text = 'Last twice times greater than Vessel draught'

	##SHIPTABLE [2,0]
	ht = shiptable.cell(2, 0).paragraphs[0]
	r0 = ht.add_run()
	r0.text = 'Measurement method:'
	ht = shiptable.cell(2, 0).add_paragraph()
	r0 = ht.add_run()
	r0.text = 'According to standard ISO 10816 : - procedure No. 2 Measurement report'



	summary = document.add_paragraph()
	summary.add_run('Summary:').bold = True
	summary.runs[0].add_break()
	s1 = summary.add_run(
		'Next measurements should be done in three month period to obtain trend value for each equipment, in some cases even one month period is preferable.')
	s1.add_break()
	s1.add_break()
	summary.add_run(
		'This report is prepared in good faith based on measurement diagnostic done on available running rotary machine and documentation submitted.').font.size = Pt(
		11)
	document.add_paragraph()