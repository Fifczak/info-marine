import psycopg2
import csv
host = 'localhost'
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
print(q_run(connD, 'Select * from main'))

querry =  """
select ml.raport_number, remrn.raport_number as RemarksT, fdbrn.raport_number as FeedbacksT, remindrn.raport_number as ReminderT

from measurements_low as ml
left join (select raport_number from remarks group by raport_number) as remrn on ml.raport_number = remrn.raport_number
left join (select raport_number from feedbacks group by raport_number) as fdbrn on ml.raport_number = fdbrn.raport_number
left join (select raport_number from reminder group by raport_number) as remindrn on ml.raport_number = remindrn.raport_number
group by ml.raport_number, remrn.raport_number, fdbrn.raport_number, remindrn.raport_number
order by ml.raport_number desc


"""