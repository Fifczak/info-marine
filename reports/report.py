import os.path
import time

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_devicetable import devicetable
from report_frontpages import *
from report_headtables import *
from report_resulttables import prepare_IM ,drawtable_IM ,trendresults
from report_shipdata import shipdata
from report_standards import legend_IM ,standards
from report_styles import loadstyles

username = 'postgres'
password = 'info'
host = 'localhost'
connD = [ username ,password ,host ]


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
def q_run ( connD ,querry ):
    username = connD[ 0 ]
    password = connD[ 1 ]
    # cs = (host="localhost"  , dbname="postgres" , user= "postgres" , password="info")
    # cs = "dbname=%s user=%s password=%s host=%s port=%s"%(kdb,username,password,host,kport)
    conn = psycopg2.connect ( host="localhost" ,dbname="postgres" ,user="postgres" ,password="info" )
    cur = conn.cursor ()
    cur.execute ( querry )
    try:
        result = cur.fetchall ()
        return result
    except:
        pass
    conn.commit ()
    cur.close ()


rn_ = '1987-2019'
querry = "Select parent from measurements_low where raport_number = '" + rn_ + "' limit 1"
parent = q_run ( connD ,querry )
querry = """select 
					 ml.id, ml.raport_number, dev.name,  max(ml.value) as RMS, ml2.max as Envelope, dev.norm ,ml.date, dev.drivenby,dss.sort
					from measurements_low as ml
					left join (select 
								 ml.id, ml.raport_number,  max(ml.value)
								 from measurements_low as ml
								 where type = 'envelope P-K' and parent = """ + str ( parent[ 0 ][ 0 ] ) + """
								 group by id,raport_number order by raport_number DESC) as ml2 on ml.id = ml2.id and ml.raport_number = ml2.raport_number
					 left join devices as dev on ml.id = dev.id
					 left join(select cast (id as integer), sort from ds_structure where id ~E'^\\\d+$' ) as dss on ml.id = dss.id
					 where ml.type = 'RMS' and ml.parent = """ + str ( parent[ 0 ][ 0 ] ) + """
					 group by ml.id, ml.raport_number, ml2.max,dev.name, dev.norm,ml.date,dev.drivenby,dss.sort order by raport_number DESC"""
reportresults = q_run ( connD ,querry )


def getTrend ( self ):
    trendlist = list ()
    for line in reportresults:
        if str ( line[ 0 ] ) == str ( self.id ):
            if str ( line[ 1 ] ) != str ( report_number ):
                newdate = time.strptime ( str ( line[ 6 ] ) ,"%Y-%m-%d" )
                mydate = time.strptime ( str ( self.date ) ,"%Y-%m-%d" )
                if newdate < mydate:
                    trendlist.append ( str ( line[ 3 ] ) )  # VAL
                    trendlist.append ( str ( line[ 6 ] ) )  # DATE

                    change = abs ( (float ( line[ 3 ] ) - float ( self.maxval )) / float ( line[ 3 ] ) )

                    if change <= 0.05:
                        TREND = 'C'

                    if float ( line[ 3 ] ) < float ( self.maxval ):
                        TREND = 'U'

                    if float ( line[ 3 ] ) > float ( self.maxval ):
                        TREND = 'D'

                    trendlist.append ( TREND )  # TREND=> U-UP, D-DOWN, C-CONST
                    break
    self.trend = trendlist
    return measlist


# TRZEBA PRZEMYSLEC W JAKI SPOSOB BĘDĄ WYBIERANE DANE DO TWORZENIA RAPORTÓW
fileformattype = 1  # 1 - IM; 2 - KAMTRO ; 3-Stocznia Remontowa
headtabletype = 1  # 1 - IM; 2 - KAMTRO; 3 - stocznia remontowa
frontpagetype = 1
resulttable = 1  # 1 - IM; 2-remontowa
report_number = '1987-2019'

def makereport ( connD ,rn_ ):
    username = connD[ 0 ]
    password = connD[ 1 ]
    host = connD[ 2 ]
    # PRZYGOTOWANIE TEMPLATA DO GENEROWANIA RAPORTU
    # dodana formatka do remontowej
    if fileformattype == 1:
        filepath = 'C:\\overmind\\Data\\baseIM.docx'
    if fileformattype == 2:
        filepath = 'C:\\overmind\\Data\\baseKAM.docx'
    if fileformattype == 3:
        filepath = 'C:\\overmind\\Data\\baseGSR.docx'
    document = Document ( filepath )
    loadstyles ( document )
    rn_ = str ( rn_ )
    # wybór headtable IM/Kamtro
    if headtabletype == 1:
        standard_info_table ( connD ,document ,rn_ )
        standard_with_pms ( document )
        standards ( document )
        legend_IM ( document )
        prepare_IM ( connD ,report_number )
        measlist = prepare_IM ( connD ,rn_ )
        respar = document.add_paragraph ( 'Results' )
        respar.runs[ 0 ].bold = True
        respar.runs[ 0 ].font.name = 'Times New Roman'
        respar.runs[ 0 ].font.size = Pt ( 12 )
        respar.add_run ().add_break ()
        resrun = respar.add_run (
            "In table are presented only readings with max. RMS results for each device equipment:" )
        resrun.font.size = Pt ( 11 )
        drawtable_IM ( document ,measlist ,connD ,report_number )
        document.add_paragraph ()
        trendresults ( document )
        devicetable ( document )
        shipdata ( document )
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



    if headtabletype == 2:
        standard_Kamtro_table ( document )
        standard_with_pms ( document )
    if headtabletype == 3:
        standard_GSR_table ( document )
        standard_GSR ( document )

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

makereport ( connD ,'1987-2019' )
os.startfile ( 'C:\overmind\Reports\GSR 1987-2019.docx' )
