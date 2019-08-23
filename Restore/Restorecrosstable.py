#FIFCZAK BASICS
import psycopg2
import pandas as pd
connD=['filipb','@infomarine','192.168.10.243']
#connD=['filipb','@infomarine','192.168.10.243']
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
###
import json
from pandas.io.json import json_normalize
from tqdm import tqdm

querry = "select old_val from logging.t_history where who = 'michalinan' and tabname = 'crosstable' and tstamp > '2019-08-09 15:43' and tstamp < '2019-08-09 15:44' "
tobackuplist =list(q_run(connD,querry))



for item in tqdm(tobackuplist):
	row = pd.DataFrame([item[0]])
	nameindevice =(row['nameindevice'][0])
	id = (row['id'][0])
	if str(nameindevice).strip() != '':
		querry = "update crosstable set nameindevice = '{}' where id = {}".format(nameindevice,id)
		q_run(connD, querry)

