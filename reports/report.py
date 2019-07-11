import os
import time
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import psycopg2
from report_styles import loadstyles
from report_headtables import standard_info_table
from report_frontpages import standard_with_pms
from report_resulttables import prepare_IM ,drawtable_IM_chart_PMS,drawtable_IM_chart_PMS_limit ,trendresults
from report_standards import legend_IM ,standards
from time import gmtime, strftime
from report_measurementequipment import MarVibENG
from report_summary import IMVibEng
from report_signature import signatureENG

from tkinter import filedialog


# from report_devicetable import devicetable
#NIEUZYWANE from report_shipdata import getshipsdata ,shipdata



def getini ( connD) :
	querry = "select ini from users where login = '"+str(connD[0]).strip()+"' limit 1;"
	result = list(q_run(connD,querry))
	return result[ 0 ][ 0 ]

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



def makereport ( connD ,rn_ ):
	rn_ = str(rn_)

	#############################################################################################
	############################ 0.USTALANIE SKŁADOWYCH DO RAPORTU ##############################
	#############################################################################################

	querry = "select reporttype from main where id = (select shipid from harmonogram where report_number = '"+str(rn_)+"')"
	reporttype = list(q_run(connD,querry))[0][0]

	# fileformattype = 1  # 1 - IM; 2 - KAMTRO ; 3-Stocznia Remontowa
	# headtabletype = 1  # 1 - IM; 2 - KAMTRO; 3 - stocznia remontowa
	# standards #
	# frontpagetype = 1
	# resulttable = 1  # 1 - IM chart + PMS ; 2-remontowa ; 3 - IM chart + PMS + limit
	# measurementequipment
	# summary #1 - standard IM summary
	# signatures

	reptypedict = {
		"fileformat": 0,
		"headtabletype": 0,
		"frontpagetype": 0,
		"standards": 0,
		"resulttable": 0,
		"measurementequipment": 0,
		"summary": 0,
		"signatures": 0,
	}

	if int(reporttype) == 3:
		reptypedict.update( {"fileformat": 1})
		reptypedict.update({"headtabletype": 1})
		reptypedict.update({"standards": 1})
		reptypedict.update({"frontpagetype": 1})
		reptypedict.update({"resulttable": 1})
		reptypedict.update({"measurementequipment": 1})
		reptypedict.update({"summary": 1})
		reptypedict.update({"signatures": 1})

	if int(reporttype) == 5:
		reptypedict.update( {"fileformat": 1})
		reptypedict.update({"headtabletype": 1})
		reptypedict.update({"standards": 1})
		reptypedict.update({"frontpagetype": 1})
		reptypedict.update({"resulttable": 3})
		reptypedict.update({"measurementequipment": 1})
		reptypedict.update({"summary": 1})
		reptypedict.update({"signatures": 1})


	#############################################################################################
	############################ I. WYBIERANIE FORMATKI POD RAPORT ##############################
	#############################################################################################

	if reptypedict["fileformat"] == 1:
		filepath = 'C:\\overmind\\Data\\baseIM.docx'
	if reptypedict["fileformat"] == 2:
		filepath = 'C:\\overmind\\Data\\baseKAM.docx'
	if reptypedict["fileformat"] == 3:
		filepath = 'C:\\overmind\\Data\\baseGSR.docx'
	document = Document ( filepath )
	loadstyles ( document )


	#############################################################################################
	################################# II. TABELA NAGŁÓWEK #######################################
	#############################################################################################


	if reptypedict["headtabletype"] == 1:
		standard_info_table ( connD ,document ,rn_ )
	elif reptypedict["headtabletype"] == 2:
		standard_Kamtro_table ( document )
	elif reptypedict["headtabletype"] == 3:
		standard_GSR_table ( document )




	#############################################################################################
	############################# III. TEKST STRONA TYTUŁOWA ####################################
	#############################################################################################


	if reptypedict["frontpagetype"] == 1:
		standard_with_pms ( document )

	#############################################################################################
	######################################## IV. NORMY ##########################################
	#############################################################################################


	if reptypedict["standards"] == 1:
		standards ( document )



	#############################################################################################
	######################################## V. WYNIKI ##########################################
	#############################################################################################

	if reptypedict["resulttable"] == 1:
		measlist = prepare_IM(connD, rn_)
		drawtable_IM_chart_PMS ( document ,measlist ,connD ,rn_ )
	if reptypedict["resulttable"] == 3:
		measlist = prepare_IM(connD, rn_)
		drawtable_IM_chart_PMS_limit ( document ,measlist ,connD ,rn_ )

	#############################################################################################
	################################ VI. Urządzenie pomiarowe ###################################
	#############################################################################################


	if reptypedict["measurementequipment"] == 1:
		MarVibENG ( document,connD ,rn_)


	#############################################################################################
	################################## VII. Podsumowanie ########################################
	#############################################################################################


	if reptypedict["standards"] == 1:
		IMVibEng ( document,connD ,rn_)

	#############################################################################################
	##################################### VI. Podpis ############################################
	#############################################################################################
	if reptypedict["standards"] == 1:
		signatureENG ( document ,connD)


	#############################################################################################
	##################################### ZAPISANIE  ############################################
	#############################################################################################

	#if int(reporttype) == 3:
	querry = "select name from main where id = (select shipid from harmonogram where report_number = '" + str(rn_) + "')"
	shipname = list(q_run(connD,querry))[0][0]

	f = filedialog.askdirectory()
	document.save ( f +'/'+ str(shipname) + ' - vibration report '
					+ str(rn_) + '_' + str(getini(connD)) + '_' + str(strftime("%Y-%m-%d", gmtime())) + '.docx')





#
username = 'testuser '
password = 'info'
host = '192.168.10.243'
rn_ = '1952U3-2019'
# # #rn_ ='1968-2019'
# #
#host = 'localhost'
#rn_ = '2128-2019'
# # #
connD = [ username ,password ,host ]
#
makereport(connD,rn_)