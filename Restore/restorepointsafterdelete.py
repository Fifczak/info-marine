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

querry = "select old_val from logging.t_history where who = 'kubak' and tabname = 'points' and tstamp > '2019-08-23 08:32' and tstamp < '2019-08-23 08:34' "
tobackuplist =list(q_run(connD,querry))



for item in tqdm(tobackuplist):
	row = pd.DataFrame([item[0]])
	#nameindevice =(row['nameindevice'][0])
	id = (row['id'][0])
	point = (row['point'][0])
	sort = (row['sort'][0])
	visible = (row['visible'][0])
	if str(id).strip() != '':
		querry = "INSERT INTO POINTS (id,point,sort,visible) VALUES ({},'{}',{},{})".format(id,point,sort,visible)
		#print(querry)
		q_run(connD, querry)

