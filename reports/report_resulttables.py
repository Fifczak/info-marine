import time

import psycopg2
from chart_scripts import *
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.shared import Cm
from docx.shared import RGBColor
from report_database import *
from report_headtables import *

rn_ = '1987-2019'


# funkcja do stałej szerokości komórek w raportach GSR
def set_col_width_GSR( table ):
    widths = (Cm( 7 ) ,Cm( 1.5 ) ,Cm( 1.5 ) ,Cm( 1.5 ) ,Cm( 1.5 ) ,Cm( 1.5 ) ,Cm( 5 ))
    for row in table.rows:
        for idx ,width in enumerate( widths ):
            row.cells[ idx ].width = width


def q_run( connD ,querry ):
    username = connD[ 0 ]
    password = connD[ 1 ]
    # cs = (host="localhost"  , dbname="postgres" , user= "postgres" , password="info")
    # cs = "dbname=%s user=%s password=%s host=%s port=%s"%(kdb,username,password,host,kport)
    conn = psycopg2.connect( host="localhost" ,dbname="postgres" ,user="postgres" ,password="info" )
    cur = conn.cursor()
    cur.execute( querry )
    try:
        result = cur.fetchall()
        return result
    except:
        pass
    conn.commit()
    cur.close()


def prepare_IM( connD ,report_number ):  # RETURN MEASLIST
    measlist = list()

    class meas( object ):
        def __init__( self ):
            self.id = ''
            self.name = ''
            self.maxval = ''
            self.maxval2 = ''
            self.limit = ''
            self.maxenv = ''
            self.trend = list()
            self.standard = ''
            self.date = ''
            self.drivenby = ''
            self.sort = ''
            self.sort2 = ''

    def loadData( connD ):
        def countLimit( standard ,value ):
            for limNo in limits:
                if str( limNo[ 0 ] ) == str( standard ):
                    if value <= float( limNo[ 3 ] ):  # IF LIM1
                        limSrt = str( limNo[ 2 ] )
                        break
                    else:
                        if value <= float( limNo[ 5 ] ):  # IF LIM2
                            limSrt = str( limNo[ 4 ] )
                            break
                        else:
                            if value <= float( limNo[ 7 ] ):  # IF LIM3
                                limSrt = str( limNo[ 6 ] )
                                break
                            else:
                                limSrt = str( limNo[ 8 ] )
                                break

            return limSrt

        def getTrend( self ):
            trendlist = list()
            for line in reportresults:
                if str( line[ 0 ] ) == str( self.id ):
                    if str( line[ 1 ] ) != str( report_number ):
                        newdate = time.strptime( str( line[ 6 ] ) ,"%Y-%m-%d" )
                        mydate = time.strptime( str( self.date ) ,"%Y-%m-%d" )
                        if newdate < mydate:
                            trendlist.append( str( line[ 3 ] ) )  # VAL
                            trendlist.append( str( line[ 6 ] ) )  # DATE

                            change = abs( (float( line[ 3 ] ) - float( self.maxval )) / float( line[ 3 ] ) )

                            if change <= 0.05:
                                TREND = 'C'

                            if float( line[ 3 ] ) < float( self.maxval ):
                                TREND = 'U'

                            if float( line[ 3 ] ) > float( self.maxval ):
                                TREND = 'D'

                            trendlist.append( TREND )  # TREND=> U-UP, D-DOWN, C-CONST
                            break
            self.trend = trendlist
            return measlist

        querry = "Select parent from measurements_low where raport_number = '" + rn_ + "' limit 1"
        parent = q_run( connD ,querry )

        querry = """select standard,
							limit_1_value,limit_1_name,
							limit_2_value,limit_2_name, 
							limit_3_value,limit_3_name,
							limit_4_value,limit_4_name,
						envflag
					from standards"""
        limits = q_run( connD ,querry )
        querry = """select 
					 ml.id, ml.raport_number, dev.name,  max(ml.value) as RMS, ml2.max as Envelope, dev.norm ,ml.date, dev.drivenby,dss.sort
					from measurements_low as ml
					left join (select 
								 ml.id, ml.raport_number,  max(ml.value)
								 from measurements_low as ml
								 where type = 'envelope P-K' and parent = """ + str( parent[ 0 ][ 0 ] ) + """
								 group by id,raport_number order by raport_number DESC) as ml2 on ml.id = ml2.id and ml.raport_number = ml2.raport_number
					 left join devices as dev on ml.id = dev.id
					 left join(select cast (id as integer), sort from ds_structure where id ~E'^\\\d+$' ) as dss on ml.id = dss.id
					 where ml.type = 'RMS' and ml.parent = """ + str( parent[ 0 ][ 0 ] ) + """
					 group by ml.id, ml.raport_number, ml2.max,dev.name, dev.norm,ml.date,dev.drivenby,dss.sort order by raport_number DESC"""
        reportresults = q_run( connD ,querry )

        for line in reportresults:
            x = meas()
            if str( line[ 1 ] ) == str( report_number ):
                x.id = line[ 0 ]
                x.name = line[ 2 ]
                x.maxval = line[ 3 ]
                x.maxenv = line[ 4 ]
                x.standard = line[ 5 ]
                x.date = line[ 6 ]
                getTrend( x )
                x.limit = countLimit( x.standard ,x.maxval )
                x.drivenby = line[ 7 ]
                x.sort = line[ 8 ][ :4 ]
                x.sort2 = line[ 8 ][ :1 ]
                measlist.append( x )

    loadData( connD )
    return measlist
    maxval


def drawtable_IM( document ,measlist ,connD ,report_number ):  # ):

    querry = "Select parent from measurements_low where raport_number = '" + str( report_number ) + "' limit 1"
    parent = q_run( connD ,querry )
    print( parent )
    querry = "Select sort, id from ds_structure where parent = '" + '84' + "' order by sort"
    sortlistQ = q_run( connD ,querry )
    trueMeasList = list()
    activeIdList = list()
    activeSortList = list()
    activeSortPList = list()
    idlist = list()
    drivenByList = list()
    for sort in sortlistQ:
        for meas in measlist:
            if (sort[ 1 ]).isdigit == False:
                trueMeasList.append( 'header' )
                drivenByList.append( 997 )
                idlist.append( 997 )
            if str( sort[ 1 ] ) == str( meas.id ):
                trueMeasList.append( meas )
                activeIdList.append( str( meas.id ) )
                activeSortList.append( str( meas.sort ) )
                activeSortPList.append( str( meas.sort2 ) )
                drivenByList.append( meas.drivenby )
                idlist.append( meas.id )

    counter = 0
    counterCharts = 0

    xcord = 0
    i = -1
    for measStrip in sortlistQ:
        i += 1
        if (measStrip[ 1 ]).isdigit() == False:  ######## NAGŁÓWKI
            try:
                if measStrip[ 0 ][ -5: ] == '00.00' and sortlistQ[ i + 1 ][ 0 ][ -5: ] != '00.00' and \
                        sortlistQ[ i + 1 ][ 0 ][ -3: ] == '.00':
                    if str( measStrip[ 0 ][ :1 ] ) in activeSortPList:
                        xcord += 1
                    continue
                if measStrip[ 0 ][ -5: ] != '00.00' and measStrip[ 0 ][ -3: ] == '.00':
                    if str( measStrip[ 0 ][ :4 ] ) in activeSortList:
                        xcord += 1
                    continue
            except:
                pass
        else:
            p = -1
            for xx in trueMeasList:
                p += 1
                if str( measStrip[ 1 ] ) == str( xx.id ):
                    try:
                        if str( drivenByList[ p + 1 ] ) == str( xx.id ):
                            xcord += 1
                        else:
                            xcord += 2
                        break
                    except:
                        xcord += 2

    rowscount = xcord
    resulttable = document.add_table( rows=rowscount + 1 ,cols=7 )
    resulttable.style = 'Table Grid'

    ht = resulttable.cell( 0 ,0 ).paragraphs[ 0 ]
    r0 = ht.add_run( 'Nazwa urządzenia' )

    ht = resulttable.cell( 0 ,1 ).paragraphs[ 0 ]
    r0 = ht.add_run( 'Prędkość RMS (mm/s) Freq A Max' )

    ht = resulttable.cell( 0 ,2 ).paragraphs[ 0 ]
    r0 = ht.add_run( 'Prędkość RMS (mm/s) Freq B Max' )

    ht = resulttable.cell( 0 ,3 ).paragraphs[ 0 ]
    r0 = ht.add_run( 'ISO/VDI standard' )

    ht = resulttable.cell( 0 ,4 ).paragraphs[ 0 ]
    r0 = ht.add_run( 'Obwiednia łożysk 0-Peak (gE) Max' )

    ht = resulttable.cell( 0 ,5 ).paragraphs[ 0 ]
    r0 = ht.add_run( 'Prędkość RMS Max (mm/s) Trend' )

    ht = resulttable.cell( 0 ,6 ).paragraphs[ 0 ]
    r0 = ht.add_run( 'Uwagi i sugestie' )

    xcord = 0
    i = -1
    for measStrip in sortlistQ:
        i += 1

        if (measStrip[ 1 ]).isdigit() == False:  ######## NAGŁÓWKI
            try:
                ht = resulttable.cell( xcord + 1 ,0 ).paragraphs[ 0 ]
                if measStrip[ 0 ][ -5: ] == '00.00' and sortlistQ[ i + 1 ][ 0 ][ -5: ] != '00.00' and \
                        sortlistQ[ i + 1 ][ 0 ][ -3: ] == '.00':
                    if str( measStrip[ 0 ][ :1 ] ) in activeSortPList:
                        xcord += 1
                        r0 = ht.add_run( measStrip[ 1 ] )
                        resulttable.cell( xcord ,0 ).merge( resulttable.cell( xcord ,6 ) )

                    continue
                if measStrip[ 0 ][ -5: ] != '00.00' and measStrip[ 0 ][ -3: ] == '.00':
                    if str( measStrip[ 0 ][ :4 ] ) in activeSortList:
                        xcord += 1
                        r0 = ht.add_run( measStrip[ 1 ] )
                        resulttable.cell( xcord ,0 ).merge( resulttable.cell( xcord ,6 ) )

                    continue
            except:
                pass
        else:  ######## POMIARY
            p = -1
            for xx in trueMeasList:
                p += 1
                if str( measStrip[ 1 ] ) == str( xx.id ):

                    ht = resulttable.cell( xcord + 1 ,0 ).paragraphs[ 0 ]
                    r0 = ht.add_run( xx.name )
                    ht = resulttable.cell( xcord + 1 ,1 ).paragraphs[ 0 ]
                    # dodałem tu zamianę kropek na przecinki + zaokrąglenie do 3 miejsca po przecinku
                    txt_result = str( round( xx.maxval ,3 ) )
                    r0 = ht.add_run( txt_result.replace( "." ,"," ) )
                    ht = resulttable.cell( xcord + 1 ,2 ).paragraphs[ 0 ]
                    r0 = ht.add_run( str( xx.maxval2 ) )
                    ht = resulttable.cell( xcord + 1 ,3 ).paragraphs[ 0 ]
                    r0 = ht.add_run( str( xx.limit ) )
                    ht = resulttable.cell( xcord + 1 ,4 ).paragraphs[ 0 ]
                    r0 = ht.add_run ( str ( xx.maxenv ).replace ( "." ,"," ) )
                    ht = resulttable.cell( xcord + 1 ,5 ).paragraphs[ 0 ]
                    if str( xx.limit ) == 'Cl. D':  # TEGO DLA CZYTELNOSCI LEPIEJ ZROBIC FUNKCJE
                        try:

                            trendtemp1 = xx.trend[ 0 ]
                            trendtemp2 = xx.trend[ 1 ]
                            trendtemp3 = xx.trend[ 2 ]

                            if str( trendtemp3 ) == 'U':
                                r0 = ht.add_run()
                                r0.add_picture( 'Iup.gif' )
                            elif str( trendtemp3 ) == 'D':
                                r0 = ht.add_run()
                                r0.add_picture( 'down.gif' )
                            elif str( trendtemp3 ) == 'C':
                                r0 = ht.add_run()
                                r0.add_picture( 'none.gif' )
                            p0 = ht.add_run( '\n' + 'Ostatnia Wartość:' )
                            p0 = ht.add_run( '\n' + str( trendtemp2 ) )
                            p0 = ht.add_run( '\n' + str( trendtemp1 ) )
                        except:
                            pass

                    try:
                        if str( drivenByList[ p + 1 ] ) == str( xx.id ):
                            xcord += 1
                        else:
                            xcord += 1
                            resulttable.cell( xcord + 1 ,0 ).merge( resulttable.cell( xcord + 1 ,6 ) )
                            ht = resulttable.cell( xcord + 1 ,0 ).paragraphs[ 0 ]
                            p0 = ht.add_run( 'TUBEDZIEWYKRES' )
                            xcord += 1
                        break
                    except:  # OSTATNIA LINIA TABELI
                        xcord += 1
                        resulttable.cell( xcord + 1 ,0 ).merge( resulttable.cell( xcord + 1 ,6 ) )
                        ht = resulttable.cell( xcord + 1 ,0 ).paragraphs[ 0 ]
                        p0 = ht.add_run( 'TUBEDZIEWYKRES' )


# def	drawtable_STOCZNIA_REMONTOWA(document,measlist,connD,report_number):#):trzeba troche ukrocic
# 	querry = "Select parent from measurements_low where raport_number = '" + str(report_number) + "' limit 1"
# 	parent = q_run(connD,querry)[0][0]
# 	querry = "Select sort, id from ds_structure where parent = '" + str(parent) + "' order by sort"
# 	sortlistQ = q_run(connD,querry)
# 	trueMeasList = list()
# 	activeIdList = list()
# 	for sort in sortlistQ:
# 		for meas in measlist:
# 			if (sort[1]).isdigit == False:
# 				trueMeasList.append('header')
# 			if str(sort[1])==str(meas.id):
# 				trueMeasList.append(meas)
# 				activeIdList.append(str(meas.id))
# 	counter = 0
# 	counterCharts = 0
# 	i=-1
# 	for measStrip in sortlistQ:  #ILOSC WIERSZY
# 		i += 1
# 		if (measStrip[1]).isdigit() == False:
# 			if measStrip[0][-5:] == '00.00' and sortlistQ[i+1][0][-5:] != '00.00' and sortlistQ[i+1][0][-3:] == '.00':
# 				counter +=1
# 				continue
# 			if measStrip[0][-5:] != '00.00' and measStrip[0][-3:] == '.00' :
# 				if str(sortlistQ[i+1][1]) in activeIdList:
# 					counter +=1
# 					continue
# 		else:
# 			for xx in trueMeasList:
# 				if str(measStrip[1]) == str(xx.id):
# 					counter +=1
# 					if str(xx.drivenby) in activeIdList:
# 						counterCharts +=1
# 						break
# 					else:
# 						break
#
# 	rowscount = (counter*2) - counterCharts
# 	resulttable = document.add_table(rows=rowscount+1, cols=7)
# 	resulttable.style = 'Table Grid'
#
# 	ht= resulttable.cell(0,0).paragraphs[0]
# 	r0 = ht.add_run('Nazwa urządzenia')
#
# 	ht= resulttable.cell(0,1).paragraphs[0]
# 	r0 = ht.add_run('Prędkość RMS (mm/s) Freq A Max')
#
# 	ht= resulttable.cell(0,2).paragraphs[0]
# 	r0 = ht.add_run('Prędkość RMS (mm/s) Freq B Max')
#
# 	ht= resulttable.cell(0,3).paragraphs[0]
# 	r0 = ht.add_run('ISO/VDI standard')
#
# 	ht= resulttable.cell(0,4).paragraphs[0]
# 	r0 = ht.add_run('Obwiednia łożysk 0-Peak (gE) Max')
#
# 	ht= resulttable.cell(0,5).paragraphs[0]
# 	r0 = ht.add_run('Prędkość RMS Max (mm/s) Trend')
#
# 	ht= resulttable.cell(0,6).paragraphs[0]
# 	r0 = ht.add_run('Uwagi i sugestie')
#
# 	xcord = 0
# 	i=-1
# 	for measStrip in sortlistQ:
# 		i += 1
# 		if (measStrip[1]).isdigit() == False:######## NAGŁÓWKI
# 			try:
# 				ht= resulttable.cell(xcord+1,0).paragraphs[0]
# 				if measStrip[0][-5:] == '00.00' and sortlistQ[i+1][0][-5:] != '00.00' and sortlistQ[i+1][0][-3:] == '.00':
# 					r0 = ht.add_run(measStrip[1])
# 					resulttable.cell(xcord+1,0).merge(resulttable.cell(xcord+1,6))
# 					xcord += 1
# 					continue
# 				if measStrip[0][-5:] != '00.00' and measStrip[0][-3:] == '.00' :
# 					if str(sortlistQ[i+1][1]) in activeIdList:
# 						r0 = ht.add_run(measStrip[1])
# 						resulttable.cell(xcord+1,0).merge(resulttable.cell(xcord+1,6))
# 						xcord += 1
# 						continue
# 			except:
# 				pass
# 		else:	######## POMIARY
# 			for xx in trueMeasList:
#
#
#
# 				if str(measStrip[1]) == str(xx.id):
# 					if str(xx.drivenby) == '0':# tu nie dosc ze robi przed to nie rozwiazuje jak nie ma urzadzenia wskazanego przez driven by
# 						xcord += 1
# 					ht = resulttable. cell(xcord+1,0).paragraphs[0]
# 					r0 = ht.add_run(xx.name)
# 					ht = resulttable. cell(xcord+1,1).paragraphs[0]
# 					r0 = ht.add_run(str(xx.maxval))
# 					ht = resulttable. cell(xcord+1,2).paragraphs[0]
# 					r0 = ht.add_run(str(xx.maxval2))
# 					ht = resulttable. cell(xcord+1,3).paragraphs[0]
# 					r0 = ht.add_run(str(xx.limit))
# 					ht = resulttable. cell(xcord+1,4).paragraphs[0]
# 					r0 = ht.add_run(str(xx.maxenv))
# 					ht = resulttable. cell(xcord+1,5).paragraphs[0]
# 					if  str(xx.limit) == 'Cl. D':   #TEGO DLA CZYTELNOSCI LEPIEJ ZROBIC FUNKCJE
# 						try:
# 							trendtemp1 = xx.trend[0]
# 							trendtemp2 = xx.trend[1]
# 							trendtemp3 = xx.trend[2]
#
# 							if str(trendtemp3) == 'U':
# 								r0 = ht.add_run()
# 								r0.add_picture('up.gif')
# 							elif str(trendtemp3) == 'D':
# 								r0 = ht.add_run()
# 								r0.add_picture('down.gif')
# 							elif str(trendtemp3) == 'C':
# 								r0 = ht.add_run()
# 								r0.add_picture('none.gif')
# 							p0 = ht.add_run('\nOstatnia Wartość:')
# 							p0 = ht.add_run('\n' + str(trendtemp2))
# 							p0 = ht.add_run('\n' + str(trendtemp1))
# 						except:
# 							pass
# 					xcord += 1
# 					break

def drawtable_GSR( document ,measlist ,connD ,rn_ ):
    print( 'Wyniki: ' )
    H = document.add_paragraph( 'Wyniki' )
    H.runs[ 0 ].font.name = 'Times New Roman'
    H.runs[ 0 ].font.size = Pt( 14 )
    H.runs[ 0 ].add_break()
    R = H.add_run( 'W tabeli są przedstawione tylko maksymalne wartości dla każdego urządzenia:' )
    R.font.name = 'Times New Roman'
    R.font.size = Pt( 10 )

    # tabela z wynikami, poki co na sztywno, zastanowię się nad mechanizmem do budowania tabeli na podstawie tego co jest w bazie
    restable_gsr = document.add_table( rows=42 ,cols=7 )
    restable_gsr.cell( 0 ,0 ).text = 'Nazwa urządzenia'
    # proponuję rozbić poniższego stringa tak, żeby pobierał z bazy pod jakąś zmienną datę w formacie yyyy-mm (time.timenow.year,time.timenow.month)

    restable_gsr.cell( 0 ,1 ).text = 'Prędkość RMS (mm/s) Freq A Max DATA_TU'
    restable_gsr.cell( 0 ,2 ).text = 'Prędkość RMS (mm/s) Freq B Max DATA_TU'
    restable_gsr.cell( 0 ,3 ).text = 'ISO/VDI standard'
    restable_gsr.cell( 0 ,4 ).text = 'Obwiednia łożysk 0-Peak (gE) Max DATA_TU'
    restable_gsr.cell( 0 ,5 ).text = 'Prędkość RMS Max (mm/s) Trend'
    restable_gsr.cell( 0 ,6 ).text = 'Uwagi i sugestie'
    restable_gsr.cell( 1 ,0 ).text = 'KOMPRESOROWNIA 1'

    restable_gsr.cell( 1 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.color.rgb = RGBColor( 0 ,0 ,255 )
    restable_gsr.cell( 1 ,0 ).paragraphs[ 0 ].runs[ 0 ].bold = True
    restable_gsr.cell( 1 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
    restable_gsr.cell( 1 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )

    restable_gsr.cell( 1 ,0 ).merge( restable_gsr.cell( 1 ,1 ).merge( restable_gsr.cell( 1 ,2 ).merge(
        restable_gsr.cell( 1 ,3 ).merge(
            restable_gsr.cell( 1 ,4 ).merge( restable_gsr.cell( 1 ,5 ).merge( restable_gsr.cell( 1 ,6 ) ) ) ) ) ) )
    restable_gsr.cell( 1 ,0 ).paragraphs[ 0 ].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # formatowanie nagłówków tabeli
    for i in range( 7 ):
        restable_gsr.cell( 0 ,i ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Times New Roman'
        restable_gsr.cell( 0 ,i ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 10 )
        restable_gsr.cell( 0 ,i ).paragraphs[ 0 ].runs[ 0 ].bold = True
        restable_gsr.cell( 0 ,i ).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        restable_gsr.cell( 0 ,i ).paragraphs[ 0 ].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # wywołanie funkcji do formatowania po szerokości w tabeli results dla gsr
    set_col_width_GSR( restable_gsr )

    restable_gsr.cell( 2 ,0 ).text = 'Kompresor nr1'
    restable_gsr.cell( 2 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
    restable_gsr.cell( 2 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
    restable_gsr.cell( 2 ,0 ).paragraphs[ 0 ].runs[ 0 ].bold = True
    restable_gsr.cell( 2 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.color.rgb = RGBColor( 128 ,0 ,128 )
    restable_gsr.cell( 2 ,0 ).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    restable_gsr.cell( 2 ,0 ).paragraphs[ 0 ].vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
    restable_gsr.cell( 2 ,0 ).merge( restable_gsr.cell( 2 ,1 ).merge( restable_gsr.cell( 2 ,2 ).merge(
        restable_gsr.cell( 2 ,3 ).merge(
            restable_gsr.cell( 2 ,4 ).merge( restable_gsr.cell( 2 ,5 ).merge( restable_gsr.cell( 2 ,6 ) ) ) ) ) ) )
    compr_no = 1
    for i in range( 4 ):
        restable_gsr.cell( 3 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' silnik el. '
        restable_gsr.cell( 3 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 3 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 4 ,0 ).text = 'Przekładnia'
        restable_gsr.cell( 4 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 4 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 5 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. męska '
        restable_gsr.cell( 5 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 5 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 6 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. żeńska '
        restable_gsr.cell( 6 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 6 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
    compr_no = 2
    restable_gsr.cell( 7 ,0 ).text = 'Kompresor nr2'
    restable_gsr.cell( 7 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
    restable_gsr.cell( 7 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
    restable_gsr.cell( 7 ,0 ).paragraphs[ 0 ].runs[ 0 ].bold = True
    restable_gsr.cell( 7 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.color.rgb = RGBColor( 128 ,0 ,128 )
    restable_gsr.cell( 7 ,0 ).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    restable_gsr.cell( 7 ,0 ).paragraphs[ 0 ].vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
    restable_gsr.cell( 7 ,0 ).merge( restable_gsr.cell( 7 ,1 ).merge( restable_gsr.cell( 7 ,2 ).merge(
        restable_gsr.cell( 7 ,3 ).merge(
            restable_gsr.cell( 7 ,4 ).merge( restable_gsr.cell( 7 ,5 ).merge( restable_gsr.cell( 7 ,6 ) ) ) ) ) ) )
    compr_no = 2
    for i in range( 4 ):
        restable_gsr.cell( 8 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' silnik el. '
        restable_gsr.cell( 8 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 8 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 9 ,0 ).text = 'Przekładnia'
        restable_gsr.cell( 9 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 9 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 10 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. męska '
        restable_gsr.cell( 10 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 10 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 11 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. żeńska '
        restable_gsr.cell( 11 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 11 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )

    compr_no = 3
    restable_gsr.cell( 12 ,0 ).text = 'Kompresor nr3'
    restable_gsr.cell( 12 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
    restable_gsr.cell( 12 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
    restable_gsr.cell( 12 ,0 ).paragraphs[ 0 ].runs[ 0 ].bold = True
    restable_gsr.cell( 12 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.color.rgb = RGBColor( 128 ,0 ,128 )
    restable_gsr.cell( 12 ,0 ).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    restable_gsr.cell( 12 ,0 ).paragraphs[ 0 ].vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
    restable_gsr.cell( 12 ,0 ).merge( restable_gsr.cell( 12 ,1 ).merge( restable_gsr.cell( 12 ,2 ).merge(
        restable_gsr.cell( 12 ,3 ).merge(
            restable_gsr.cell( 12 ,4 ).merge( restable_gsr.cell( 12 ,5 ).merge( restable_gsr.cell( 12 ,6 ) ) ) ) ) ) )

    for i in range( 4 ):
        restable_gsr.cell( 13 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' silnik el. '
        restable_gsr.cell( 13 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 13 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 14 ,0 ).text = 'Przekładnia'
        restable_gsr.cell( 14 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 14 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 15 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. męska '
        restable_gsr.cell( 15 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 15 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 16 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. żeńska '
        restable_gsr.cell( 16 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 16 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )

    compr_no = 4
    restable_gsr.cell( 17 ,0 ).text = 'Kompresor nr4'
    restable_gsr.cell( 17 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
    restable_gsr.cell( 17 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
    restable_gsr.cell( 17 ,0 ).paragraphs[ 0 ].runs[ 0 ].bold = True
    restable_gsr.cell( 17 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.color.rgb = RGBColor( 128 ,0 ,128 )
    restable_gsr.cell( 17 ,0 ).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    restable_gsr.cell( 17 ,0 ).paragraphs[ 0 ].vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
    restable_gsr.cell( 17 ,0 ).merge( restable_gsr.cell( 17 ,1 ).merge( restable_gsr.cell( 17 ,2 ).merge(
        restable_gsr.cell( 17 ,3 ).merge(
            restable_gsr.cell( 17 ,4 ).merge( restable_gsr.cell( 17 ,5 ).merge( restable_gsr.cell( 17 ,6 ) ) ) ) ) ) )

    for i in range( 4 ):
        restable_gsr.cell( 18 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' silnik el. '
        restable_gsr.cell( 18 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 18 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 19 ,0 ).text = 'Przekładnia'
        restable_gsr.cell( 19 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 19 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 20 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. męska '
        restable_gsr.cell( 20 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 20 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 21 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. żeńska '
        restable_gsr.cell( 21 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 21 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )

    compr_no = 5
    restable_gsr.cell( 22 ,0 ).text = 'Kompresor nr5'
    restable_gsr.cell( 22 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
    restable_gsr.cell( 22 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
    restable_gsr.cell( 22 ,0 ).paragraphs[ 0 ].runs[ 0 ].bold = True
    restable_gsr.cell( 22 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.color.rgb = RGBColor( 128 ,0 ,128 )
    restable_gsr.cell( 22 ,0 ).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    restable_gsr.cell( 22 ,0 ).paragraphs[ 0 ].vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
    restable_gsr.cell( 22 ,0 ).merge( restable_gsr.cell( 22 ,1 ).merge( restable_gsr.cell( 22 ,2 ).merge(
        restable_gsr.cell( 22 ,3 ).merge(
            restable_gsr.cell( 22 ,4 ).merge( restable_gsr.cell( 22 ,5 ).merge( restable_gsr.cell( 22 ,6 ) ) ) ) ) ) )
    for i in range( 4 ):
        restable_gsr.cell( 23 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' silnik el. '
        restable_gsr.cell( 23 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 23 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 24 ,0 ).text = 'Przekładnia'
        restable_gsr.cell( 24 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 24 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 25 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. męska '
        restable_gsr.cell( 25 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 25 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 26 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. żeńska '
        restable_gsr.cell( 26 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 26 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )

    compr_no = 6
    restable_gsr.cell( 27 ,0 ).text = 'Kompresor nr6'
    restable_gsr.cell( 27 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
    restable_gsr.cell( 27 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
    restable_gsr.cell( 27 ,0 ).paragraphs[ 0 ].runs[ 0 ].bold = True
    restable_gsr.cell( 27 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.color.rgb = RGBColor( 128 ,0 ,128 )
    restable_gsr.cell( 27 ,0 ).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    restable_gsr.cell( 27 ,0 ).paragraphs[ 0 ].vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
    restable_gsr.cell( 27 ,0 ).merge( restable_gsr.cell( 27 ,1 ).merge( restable_gsr.cell( 27 ,2 ).merge(
        restable_gsr.cell( 27 ,3 ).merge(
            restable_gsr.cell( 27 ,4 ).merge( restable_gsr.cell( 27 ,5 ).merge( restable_gsr.cell( 27 ,6 ) ) ) ) ) ) )

    for i in range( 4 ):
        restable_gsr.cell( 28 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' silnik el. '
        restable_gsr.cell( 28 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 28 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 29 ,0 ).text = 'Przekładnia'
        restable_gsr.cell( 29 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 29 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 30 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. męska '
        restable_gsr.cell( 30 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 30 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 31 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. żeńska '
        restable_gsr.cell( 31 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 31 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )

    compr_no = 7
    restable_gsr.cell( 32 ,0 ).text = 'Kompresor nr7'
    restable_gsr.cell( 32 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
    restable_gsr.cell( 32 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
    restable_gsr.cell( 32 ,0 ).paragraphs[ 0 ].runs[ 0 ].bold = True
    restable_gsr.cell( 32 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.color.rgb = RGBColor( 128 ,0 ,128 )
    restable_gsr.cell( 32 ,0 ).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    restable_gsr.cell( 32 ,0 ).paragraphs[ 0 ].vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
    restable_gsr.cell( 32 ,0 ).merge( restable_gsr.cell( 32 ,1 ).merge( restable_gsr.cell( 32 ,2 ).merge(
        restable_gsr.cell( 32 ,3 ).merge(
            restable_gsr.cell( 32 ,4 ).merge( restable_gsr.cell( 32 ,5 ).merge( restable_gsr.cell( 32 ,6 ) ) ) ) ) ) )

    for i in range( 4 ):
        restable_gsr.cell( 33 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' silnik el. '
        restable_gsr.cell( 33 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 33 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 34 ,0 ).text = 'Przekładnia'
        restable_gsr.cell( 34 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 34 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 35 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. męska '
        restable_gsr.cell( 35 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 35 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 36 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. żeńska '
        restable_gsr.cell( 36 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 36 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )

    compr_no = 8
    restable_gsr.cell( 37 ,0 ).text = 'Kompresor nr8'
    restable_gsr.cell( 37 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
    restable_gsr.cell( 37 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
    restable_gsr.cell( 37 ,0 ).paragraphs[ 0 ].runs[ 0 ].bold = True
    restable_gsr.cell( 37 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.color.rgb = RGBColor( 128 ,0 ,128 )
    restable_gsr.cell( 37 ,0 ).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    restable_gsr.cell( 37 ,0 ).paragraphs[ 0 ].vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
    restable_gsr.cell( 37 ,0 ).merge( restable_gsr.cell( 37 ,1 ).merge( restable_gsr.cell( 37 ,2 ).merge(
        restable_gsr.cell( 37 ,3 ).merge(
            restable_gsr.cell( 37 ,4 ).merge( restable_gsr.cell( 37 ,5 ).merge( restable_gsr.cell( 37 ,6 ) ) ) ) ) ) )

    for i in range( 4 ):
        restable_gsr.cell( 38 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' silnik el. '
        restable_gsr.cell( 38 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 38 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 39 ,0 ).text = 'Przekładnia'
        restable_gsr.cell( 39 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 39 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 40 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. męska '
        restable_gsr.cell( 40 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 40 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.cell( 41 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. żeńska '
        restable_gsr.cell( 41 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr.cell( 41 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr.style='Table Grid'

    # kompresorownia numer 2 - mała [6 kompr]

    restable_gsr2 = document.add_table( rows=31 ,cols=7 )
    restable_gsr2.cell( 0 ,0 ).text = 'KOMPRESOROWNIA 2'
    restable_gsr2.cell( 0 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
    restable_gsr2.cell( 0 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
    restable_gsr2.cell( 0 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.color.rgb = RGBColor( 0 ,0 ,255 )
    restable_gsr2.cell( 0 ,0 ).paragraphs[ 0 ].runs[ 0 ].bold = True
    restable_gsr2.cell( 0 ,0 ).merge( restable_gsr2.cell( 0 ,1 ).merge( restable_gsr2.cell( 0 ,2 ).merge(
        restable_gsr2.cell( 0 ,3 ).merge(
            restable_gsr2.cell( 0 ,4 ).merge( restable_gsr2.cell( 0 ,5 ).merge( restable_gsr2.cell( 0 ,6 ) ) ) ) ) ) )
    restable_gsr2.cell( 0 ,0 ).paragraphs[ 0 ].alignment = WD_ALIGN_PARAGRAPH.CENTER
    restable_gsr2.cell( 1 ,0 ).text = 'Kompresor nr1'
    restable_gsr2.cell( 1 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
    restable_gsr2.cell( 1 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
    restable_gsr2.cell( 1 ,0 ).paragraphs[ 0 ].runs[ 0 ].bold = True
    restable_gsr2.cell( 1 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.color.rgb = RGBColor( 128 ,0 ,128 )
    restable_gsr2.cell( 1 ,0 ).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    restable_gsr2.cell( 1 ,0 ).paragraphs[ 0 ].vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
    restable_gsr2.cell( 1 ,0 ).merge( restable_gsr2.cell( 1 ,1 ).merge( restable_gsr2.cell( 1 ,2 ).merge(
        restable_gsr2.cell( 1 ,3 ).merge(
            restable_gsr2.cell( 1 ,4 ).merge( restable_gsr2.cell( 1 ,5 ).merge( restable_gsr2.cell( 1 ,6 ) ) ) ) ) ) )
    compr_no = 1
    for i in range( 4 ):
        restable_gsr2.cell( 2 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' silnik el. '
        restable_gsr2.cell( 2 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 2 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 3 ,0 ).text = 'Przekładnia'
        restable_gsr2.cell( 3 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 3 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 4 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. męska '
        restable_gsr2.cell( 4 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 4 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 5 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. żeńska '
        restable_gsr2.cell( 5 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 5 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
    restable_gsr2.cell( 6 ,0 ).text = 'Kompresor nr2'
    restable_gsr2.cell( 6 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
    restable_gsr2.cell( 6 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
    restable_gsr2.cell( 6 ,0 ).paragraphs[ 0 ].runs[ 0 ].bold = True
    restable_gsr2.cell( 6 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.color.rgb = RGBColor( 128 ,0 ,128 )
    restable_gsr2.cell( 6 ,0 ).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    restable_gsr2.cell( 6 ,0 ).paragraphs[ 0 ].vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
    restable_gsr2.cell( 6 ,0 ).merge( restable_gsr2.cell( 6 ,1 ).merge( restable_gsr2.cell( 6 ,2 ).merge(
        restable_gsr2.cell( 6 ,3 ).merge(
            restable_gsr2.cell( 6 ,4 ).merge( restable_gsr2.cell( 6 ,5 ).merge( restable_gsr2.cell( 6 ,6 ) ) ) ) ) ) )

    compr_no = 2
    for i in range( 4 ):
        restable_gsr2.cell( 7 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' silnik el. '
        restable_gsr2.cell( 7 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 7 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 8 ,0 ).text = 'Przekładnia'
        restable_gsr2.cell( 8 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 8 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 9 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. męska '
        restable_gsr2.cell( 9 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 9 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 10 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. żeńska '
        restable_gsr2.cell( 10 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 10 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )

    restable_gsr2.cell( 11 ,0 ).text = 'Kompresor nr3'
    restable_gsr2.cell( 11 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
    restable_gsr2.cell( 11 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
    restable_gsr2.cell( 11 ,0 ).paragraphs[ 0 ].runs[ 0 ].bold = True
    restable_gsr2.cell( 11 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.color.rgb = RGBColor( 128 ,0 ,128 )
    restable_gsr2.cell( 11 ,0 ).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    restable_gsr2.cell( 11 ,0 ).paragraphs[ 0 ].vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
    restable_gsr2.cell( 11 ,0 ).merge( restable_gsr2.cell( 11 ,1 ).merge( restable_gsr2.cell( 11 ,2 ).merge(
        restable_gsr2.cell( 11 ,3 ).merge(
            restable_gsr2.cell( 11 ,4 ).merge(
                restable_gsr2.cell( 11 ,5 ).merge( restable_gsr2.cell( 11 ,6 ) ) ) ) ) ) )
    compr_no = 3

    for i in range( 4 ):
        restable_gsr2.cell( 12 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' silnik el. '
        restable_gsr2.cell( 12 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 12 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 13 ,0 ).text = 'Przekładnia'
        restable_gsr2.cell( 13 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 13 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 14 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. męska '
        restable_gsr2.cell( 14 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 14 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 15 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. żeńska '
        restable_gsr2.cell( 15 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 15 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )

    restable_gsr2.cell( 16 ,0 ).text = 'Kompresor nr4'
    restable_gsr2.cell( 16 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
    restable_gsr2.cell( 16 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
    restable_gsr2.cell( 16 ,0 ).paragraphs[ 0 ].runs[ 0 ].bold = True
    restable_gsr2.cell( 16 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.color.rgb = RGBColor( 128 ,0 ,128 )
    restable_gsr2.cell( 16 ,0 ).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    restable_gsr2.cell( 16 ,0 ).paragraphs[ 0 ].vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
    restable_gsr2.cell( 16 ,0 ).merge( restable_gsr2.cell( 16 ,1 ).merge( restable_gsr2.cell( 16 ,2 ).merge(
        restable_gsr2.cell( 16 ,3 ).merge(
            restable_gsr2.cell( 16 ,4 ).merge(
                restable_gsr2.cell( 16 ,5 ).merge( restable_gsr2.cell( 16 ,6 ) ) ) ) ) ) )
    compr_no = 4
    for i in range( 4 ):
        restable_gsr2.cell( 17 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' silnik el. '
        restable_gsr2.cell( 17 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 17 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 18 ,0 ).text = 'Przekładnia'
        restable_gsr2.cell( 18 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 18 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 19 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. męska '
        restable_gsr2.cell( 19 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 19 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 20 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. żeńska '
        restable_gsr2.cell( 20 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 20 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )

    restable_gsr2.cell( 21 ,0 ).text = 'Kompresor nr5'
    restable_gsr2.cell( 21 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
    restable_gsr2.cell( 21 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
    restable_gsr2.cell( 21 ,0 ).paragraphs[ 0 ].runs[ 0 ].bold = True
    restable_gsr2.cell( 21 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.color.rgb = RGBColor( 128 ,0 ,128 )
    restable_gsr2.cell( 21 ,0 ).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    restable_gsr2.cell( 21 ,0 ).paragraphs[ 0 ].vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
    restable_gsr2.cell( 21 ,0 ).merge( restable_gsr2.cell( 21 ,1 ).merge( restable_gsr2.cell( 21 ,2 ).merge(
        restable_gsr2.cell( 21 ,3 ).merge(
            restable_gsr2.cell( 21 ,4 ).merge(
                restable_gsr2.cell( 21 ,5 ).merge( restable_gsr2.cell( 21 ,6 ) ) ) ) ) ) )
    compr_no = 5
    for i in range( 4 ):
        restable_gsr2.cell( 22 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' silnik el. '
        restable_gsr2.cell( 22 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 22 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 23 ,0 ).text = 'Przekładnia'
        restable_gsr2.cell( 23 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 23 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 24 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. męska '
        restable_gsr2.cell( 24 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 24 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 25 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. żeńska '
        restable_gsr2.cell( 25 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 25 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 25 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )

    restable_gsr2.cell( 26 ,0 ).text = 'Kompresor nr6'
    restable_gsr2.cell( 26 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
    restable_gsr2.cell( 26 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
    restable_gsr2.cell( 26 ,0 ).paragraphs[ 0 ].runs[ 0 ].bold = True
    restable_gsr2.cell( 26 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.color.rgb = RGBColor( 128 ,0 ,128 )
    restable_gsr2.cell( 26 ,0 ).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    restable_gsr2.cell( 26 ,0 ).paragraphs[ 0 ].vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
    restable_gsr2.cell( 26 ,0 ).merge( restable_gsr2.cell( 26 ,1 ).merge( restable_gsr2.cell( 26 ,2 ).merge(
        restable_gsr2.cell( 26 ,3 ).merge(
            restable_gsr2.cell( 26 ,4 ).merge(
                restable_gsr2.cell( 26 ,5 ).merge( restable_gsr2.cell( 26 ,6 ) ) ) ) ) ) )

    compr_no = 6
    for i in range( 4 ):
        restable_gsr2.cell( 27 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' silnik el. '
        restable_gsr2.cell( 27 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 27 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 28 ,0 ).text = 'Przekładnia'
        restable_gsr2.cell( 28 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 28 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 29 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. męska '
        restable_gsr2.cell( 29 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 29 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.cell( 30 ,0 ).text = 'Kompresor powietrza nr ' + str( compr_no ) + ' cz. żeńska '
        restable_gsr2.cell( 30 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.name = 'Arial'
        restable_gsr2.cell( 30 ,0 ).paragraphs[ 0 ].runs[ 0 ].font.size = Pt( 8 )
        restable_gsr2.style='Table Grid'
