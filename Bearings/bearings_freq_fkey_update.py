import psycopg2
from tqdm import tqdm
username = 'testuser'
password = 'info'
host = '192.168.10.243'
connD = [username,password,host]


def column(matrix, i):
    return [row[i] for row in matrix]

def q_run(connD, querry):
	username = connD[0]
	password = connD[1]
	host = connD[2]
	kport = "5432"
	kdb = "postgres"
	#cs = ' host="localhost",database="postgres", user= "postgres" , password="info" '
	cs = "dbname=%s user=%s password=%s host=%s port=%s"%(kdb,username,password,host,kport)
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


query = "select bearing, _id_ from bearings where bearing is not null and bearings_freq_fkey is null group by bearing, _id_"
bear_list_empty = q_run(connD,query)

query = "select bearing, lp from bearings_freq"
bear_list = q_run(connD,query)

print('bearing no fkey', len(bear_list_empty))
print('bearing freqs', len(bear_list))

for bearing in tqdm(bear_list_empty):
    for bearing_id in bear_list:
        if bearing[0] == bearing_id[0]:
           # print(bearing_id[1])
            query = "update bearings set bearings_freq_fkey = {} where bearing = '{}'".format(bearing_id[1],bearing[0])
            q_run(connD,query)
            break