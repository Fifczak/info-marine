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

querry = """
	select
	fdb.parent, fdb.id, fdb._id_, mai.id, mai.name
	from feedbacks as fdb

	left
	join
	devices as dev
	on
	fdb.id = dev.id
	left
	join
	main as mai
	on
	dev.parent = mai.id

	where
	fdbflag
	IS
	Null and fdb.parent is null
	"""
noparenttable = q_run(connD,querry)
for item in noparenttable:
	print(item)
	querry = "update feedbacks set parent = " + str(item[3]) + " where _id_ = " + str(item[2])
	print(querry)
	q_run(connD, querry)