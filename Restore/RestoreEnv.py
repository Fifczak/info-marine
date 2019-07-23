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

querry = "select old_val from logging.t_history where who = 'krystiank' and tstamp > '2019-07-22 13:20' and tstamp < '2019-07-22 13:30' order by tstamp"
tobackuplist =(q_run(connD,querry))



querry = "select old_val from logging.t_history where who = 'filipb' and tstamp > '2019-07-22 18:00' and tstamp < '2019-07-23 08:00' order by tstamp"
backupedlist =(q_run(connD,querry))

backupedidlist = list()
for line in tqdm(backupedlist):
    row = pd.DataFrame([line[0]])
    id = (row['_id_'][0])
    backupedidlist.append(id)

for item in tqdm(tobackuplist):
    row = pd.DataFrame([item[0]])
    val =(row['value'][0])
    id = (row['_id_'][0])
    if id not in backupedidlist:
        querry = "update measurements_low set value = {} where _id_ = {}".format(val,id)
        q_run(connD,querry)

