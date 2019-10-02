#FIFCZAK BASICS
import psycopg2
import pandas as pd
connD=['filipb','@infomarine','192.168.10.243']

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


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)

querry = "select old_val from logging.t_history where who = 'michalinan' and tstamp > '2019-10-02 08:32:00' and tstamp < '2019-10-02 08:33:00' order by tstamp"
tobackuplist =(q_run(connD,querry))

for item in tqdm(tobackuplist):
    row = pd.DataFrame([item[0]])
    val =(row['value'][0])
    id = (row['_id_'][0])

    querry = """INSERT INTO measurements_low(parent,point,type,unit,date,value,raport_number,id,m_tasks_fkey, m_tasks_setup[0], m_tasks_setup[1])
    VALUES ({},'{}','{}','{}','{}',{},'{}','{}',{},'{}','{}')""".format(row['parent'][0],row['point'][0],row['type'][0],
                                                                  row['unit'][0],row['date'][0],row['value'][0],
                                                                  row['raport_number'][0],row['id'][0],row['m_tasks_fkey'][0],
                                                                  row['m_tasks_setup'][0][0], row['m_tasks_setup'][0][1])
    q_run(connD,querry)
    # if id not in backupedidlist:
    #     querry = "update measurements_low set value = {} where _id_ = {}".format(val,id)
    #     q_run(connD,querry)
    #
