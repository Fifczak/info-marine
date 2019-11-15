import psycopg2
import pandas.io.sql as sqlio
import pandas as pd
import numpy as np
#connD=['testuser','info','192.168.10.243']
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
def column(matrix, i):
    return [row[i] for row in matrix]


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)

username = 'testuser'
password = 'info'
host = '192.168.10.243'
connD = [username,password,host]
conn = psycopg2.connect(
            "host='{}' port={} dbname='{}' user={} password={}".format(connD[2], '5432', 'postgres', connD[0], connD[1]))


querry = """select datasheet_start, datasheet_koniec,
	   report_start, report_koniec,
	   analysis_start, analysis_koniec 
	from harmonogram 
	where datasheet_start is not null and datasheet_koniec is not null
	  and report_start is not null and report_koniec is not null 
	  and analysis_start is not null and analysis_koniec is not null 
	  and report_number !~ 'U'"""

timelist = sqlio.read_sql_query(querry, conn)


timelist['datasheet_time'] = timelist['datasheet_koniec'] - timelist['datasheet_start']
timelist['report_time'] = timelist['report_koniec'] - timelist['report_start']
timelist['analysis_time'] = timelist['analysis_koniec'] - timelist['analysis_start']

timestats = timelist[['datasheet_time', 'report_time' , 'analysis_time']]
timestats['datasheet_time'] = timestats[['datasheet_time']] / pd.Timedelta('1 minute')
timestats['report_time'] = timestats[['report_time']] / pd.Timedelta('1 minute')
timestats['analysis_time'] = timestats[['analysis_time']] / pd.Timedelta('1 minute')
# timestats['report_time'] = timelist[['report_time']] / pd.Timedelta('1 minute')
# timestats['analysis_time'] = timelist[['analysis_time']] / pd.Timedelta('1 minute')
# , 'report_time', 'analysis_time']]
timestats.hist()
#print(timestats)
#print(timestats.info())