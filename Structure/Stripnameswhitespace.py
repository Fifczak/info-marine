#FIFCZAK BASICS
import psycopg2
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
from tqdm import tqdm

todellist = list()
querry = "select name,id from devices where name ~ ' '"
for line in q_run(connD,querry):
	ll = len(line[0])
	if str(line[0][ll-1:ll]) == ' ':
		todellist.append(line)

for line in tqdm(todellist):
	querry = "update devices set name = '{}' where id = {}".format(line[0].strip(),line[1])
	q_run(connD, querry)
