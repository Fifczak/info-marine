import psycopg2
import re
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
def updatemissingdata():
	querry ="select costflag,typ, kwrange[1],kwrange[2], price[1],price[2], low[1],low[2] , high[1],high[2]from costcases"
	costcases =q_run(connD, querry)
	querry = """select  fdb._id_,fdb.costflag,dev.type,dev.kw from feedbacks as fdb
	left join devices as dev on fdb.id = dev.id
	where fdb.costflag is not null  and( fdb.low[1] = 'no kW' or fdb.low[1] = 'no TYPE' or fdb.low[1] = 'NO COST CASE')
	order by fdb._id_ 
	"""
	_id_list = list(q_run(connD, querry))
	print(querry)
	class coststrings:
		def __init__(self):
			self.pricestr = ''
			self.priceval = ''
			self.lowstr = ''
			self.lowval = ''
			self.highstr = ''
			self.highval = ''


	for line in tqdm(_id_list):
		for case in costcases:
			if line[1] == case [0]:
				if str(line[2]).strip() == str(case[1]).strip():
					kw = (re.findall( r'\d+\.*\d*', str(line[3]))[0])
					if (float(kw) >= float(case[2]) and float(kw) <= float(case[3])) or (case[2]==0 and case[3]==0) :

						# print(case[2],'<',kw,'<',case[3])
						# print(line[0])
						pricestr = case[4]
						priceval = case[5]
						lowstr = case[6]
						lowval = case[7]
						highstr = case[8]
						highval = case[9]
						querry = "update feedbacks set "\
						"price = '{" + '"' + str(pricestr)  +'" ,"'+str(priceval)+ '"' + "}'" \
						", low = '{" + '"' + str(lowstr) + '" ,"' + str(lowval) + '"' + "}'" \
						", high = '{" + '"' + str(highstr)  +'" ,"'+str(highval)+ '"' + "}'"\
						+ ' where _id_ = ' + str (line[0])
						print(querry)
						q_run(connD,querry)
						break


updatemissingdata()