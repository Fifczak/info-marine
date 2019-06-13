import os
import time
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import psycopg2
from report_styles import loadstyles
from report_headtables import standard_info_table
from report_frontpages import standard_with_pms
from report_resulttables import prepare_IM ,drawtable_IM_chart_PMS ,trendresults



# from report_devicetable import devicetable
# from report_shipdata import getshipsdata ,shipdata
# from report_standards import legend_IM ,standards






def getname ( host ,username ,password ) :
    kport = "5432"
    kdb = "postgres"
    cs = "dbname=%s user=%s password=%s host=%s port=%s" % (kdb ,username ,password ,host ,kport)
    conn = None
    conn = psycopg2.connect ( str ( cs ) )
    cur = conn.cursor ()
    # tu trzeba dodać 'kuser' w kwerendzie
    querry = "select full_name from users where login = 'krystiank' limit 1;"
    cur.execute ( querry )
    result = cur.fetchall ()
    conn.commit ()
    cur.close ()
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
    # standards
    # frontpagetype = 1
    # resulttable = 1  # 1 - IM; 2-remontowa
    # measurementequipment
    # summary
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
    print(reptypedict)

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


        # standard_with_pms(document)
        # standard_GSR(document)


        ### HASZUJE DLA SZYBSZEJ PRACY (POTEM TRZEBA TO ROZKMINIC
        # standards ( document )
        # legend_IM ( document )





        measlist = prepare_IM(connD, rn_)
        drawtable_IM_chart_PMS ( document ,measlist ,connD ,rn_ )
        document.add_paragraph ()
        # trendresults ( document )
        # devicetable ( document )
        # getshipsdata ( parent )
        # shipdata ( document )











    # podsumowanie daję tu na sztywno, na dzień dzisiejszy nie wiem czy to jest pobierane z bazy czy uzupełniane ręcznie
    document.add_page_break ()
    summary = document.add_paragraph ()
    summary.add_run ( 'Summary:' ).bold = True
    summary.runs[ 0 ].add_break ()
    s1 = summary.add_run (
        'Next measurements should be done in three month period to obtain trend value for each equipment, in some cases even one month period is preferable.' )
    s1.add_break ()
    s1.add_break ()
    summary.add_run (
        'This report is prepared in good faith based on measurement diagnostic done on available running rotary machine and documentation submitted.' ).font.size = Pt (
        11 )
    document.add_paragraph ()

    signpar = document.add_paragraph ()
    seCAP = signpar.add_run (
        'Service Engineer                                                                                             Approved by' )
    seCAP.alignment = WD_ALIGN_PARAGRAPH.LEFT
    name = str ( getname ( host='localhost' ,username='postgres' ,password='info' ) )
    signpar = document.add_paragraph ( str ( name ))




    # if frontpagetype == 1:
    #  standard_PMS_limit(document)
    document.add_paragraph ()
    # P3 = document.add_paragraph('03. STANDARDS (put informations about standards here)')
    # standards(document)
    measlist = prepare_IM ( connD ,rn_ )
    # drawtable_GSR ( document ,measlist ,connD ,rn_ )

    # drawtable_IM()
    ##########################################
    # appr = document.add_paragraph()
    # appr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    document.save ( 'C:\overmind\Reports\GSR ' + rn_ + '.docx' )




username = 'testuser'
password = 'info'
host = '192.168.10.243'
rn_ = '2070-2019'
connD = [ username ,password ,host ]


makereport ( connD ,str( rn_ ) )
#os.startfile ( 'C:\overmind\Reports\GSR 1987-2019.docx' )
