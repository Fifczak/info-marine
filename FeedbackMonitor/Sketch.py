import psycopg2
import csv
host = '192.168.10.243'
username = 'testuser'
password =  'info'
connD = [username,password,host]

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

#
# querry = "select raport_number,_id_ from feedbacks where fdbflag  IS Null  and raport_number ~' ' order by raport_number DESC, id DESC"
# badlist = q_run(connD,querry)
#
# for item in badlist:
# 	print(item)
# 	goodrn = str(item[0]).strip()
# 	print(goodrn)
# 	querry = "Update feedbacks set raport_number = '" + str(goodrn) + "' where _id_ = " + str(item[1])
# 	print(querry)
# 	q_run(connD, querry)
#
#
#
# querry ="""select fdb.raport_number,ml.parent
# from feedbacks as fdb
# left join (select parent, raport_number
# 			from measurements_low
# 			where raport_number <> ''
# 			group by parent,raport_number
# 			order by raport_number desc) as ml on fdb.raport_number = ml.raport_number
# where fdb.fdbflag  IS Null and fdb.documentdate >= '2018-01-01' and ml.parent is not null
# group by fdb.raport_number,ml.parent
# order by fdb.raport_number DESC"""
#
# parentlist  = q_run(connD,querry)
# for item in parentlist:
#
# 	rn = str(item[0]).strip()
# 	parent = str(item[1]).strip()
# 	querry = "Update feedbacks set parent = '" + str(parent) + "' where raport_number = '" + str(rn) + "'"
# 	print(querry)
# 	q_run(connD, querry)

querry = """
select parent,id,_id_ from feedbacks where fdbflag  IS Null and documentdate >= '2018-01-01'   order by documentdate DESC, id DESC
"""

for line in q_run(connD, querry):
	parent = line[0]
	id = line[1]
	lp = line[2]
	print(line)