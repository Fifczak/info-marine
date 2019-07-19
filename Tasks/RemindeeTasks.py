
#FIFCZAK BASICS
import psycopg2
from tqdm import tqdm
connD=['testuser','info','192.168.10.243']
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

def checkandupremindertasks():
	querry = """select rem.parent,main.name, max(rem.send_date)as send, min(rem.request_date) as request 
	from reminder rem
	left join main on main.id = rem.parent
	where rem.status is distinct from 2 
		and (rem.request_date) < now() + interval '2 weeks'
		and (rem.send_date) < now() - interval '1 week'
	group by rem.parent,main.name order by rem.parent"""
	toremindlist = list(q_run(connD,querry))
	querry = "select info from tasks where task is distinct from true and info ~'REMINDER TASK' "
	activeremindertasksquerry = list(q_run(connD,querry))
	activeremindertasks = list()
	for line in activeremindertasksquerry:
		activeremindertasks.append(str((line[0][line[0].rfind('#SHIPID:')+8:line[0].rfind('#NAME:')]).strip()))
	for item in tqdm(toremindlist):
		if str(item[0]) not in activeremindertasks:
			taskstr = """REMINDER TASK
#SHIPID:{}
#NAME:{}""".format(item[0],item[1])
			querry = "INSERT INTO TASKS (info) values ('{}')".format(taskstr)
			print(taskstr)
			q_run(connD,querry)

checkandupremindertasks()