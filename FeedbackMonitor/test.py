import psycopg2
from itertools import filterfalse
username = 'filipb'
password = '@infomarine'
host = '192.168.10.243'
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

def ClDNoRem():
		def countLimit(standard,value):
					limSrt ='NOPE'
					for limNo in limits:
						if str(limNo[0]) == str(standard):
							if value <= float(limNo[3]): #IF LIM1
								limSrt = str(limNo[2])
								break
							else:
								if value <=float(limNo[5]): #IF LIM2
									limSrt = str(limNo[4])
									break
								else:
									if value <=float(limNo[7]): #IF LIM3
										limSrt = str(limNo[6])
										break
									else:
										limSrt = str(limNo[8])
										break
					return limSrt
		
		querry = """select standard,
								limit_1_value,limit_1_name,
								limit_2_value,limit_2_name, 
								limit_3_value,limit_3_name,
								limit_4_value,limit_4_name,
							envflag
						from standards"""
		limits = q_run(connD,querry)
		
		print('[A]ll or [S]hip?')
		answer = input()
		if str(answer) == 'A' or str(answer) == 'a':
			querry = """select 
							 ml.id, ml.raport_number, max(ml.value) as RMS, dev.norm, main.name,dev.name,dev.parent
							from measurements_low as ml
							 left join devices as dev on ml.id = dev.id and dev.parent = ml.parent
							 left join main as main on ml.parent = main.id
							 where ml.type = 'RMS' and raport_number is not null and raport_number <> 'Archive' and raport_number <> '' and dev.norm is not null and (ml.point !~ 'A') and ml.date >= '2018-01-01'
							 group by ml.id, ml.raport_number,dev.norm, main.name,dev.name,dev.parent order by raport_number DESC"""
		
		elif str(answer) == 'S' or str(answer) == 's':
			querry = ("select id, name from main where parent <> 1 and parent is not null  and name <> '-' order by name")
			for line in q_run(connD, querry):
				print( str(line[1]) + ' ' + str(line[0]))
			print('Enter ship id:')
			answer2 = input()
			querry = """select 
							 ml.id, ml.raport_number, max(ml.value) as RMS, dev.norm, main.name,dev.name,dev.parent
							from measurements_low as ml
							 left join devices as dev on ml.id = dev.id and dev.parent = ml.parent
							 left join main as main on ml.parent = main.id
							 where ml.type = 'RMS' and raport_number is not null and raport_number <> 'Archive' and raport_number <> '' and dev.norm is not null and and ml.date >= '2018-01-01' and ml.parent = """ + str(answer2) + """
							 group by ml.id, ml.raport_number,dev.norm, main.name,dev.name,dev.parent order by raport_number DESC"""
		else:
			print ('Error input type')
		measurements = q_run(connD, querry)
		querry = "select rem.raport_number,rem.id,main.name,dev.name,dev.parent from remarks as rem left join devices as dev on rem.id = dev.id left join main as main on dev.parent = main.id group by rem.raport_number,rem.id,main.name,dev.name,dev.parent order by main.name, raport_number, id"
		
		forbiden = list()
		forbiden.append(52)
		forbiden.append(56)
		forbiden.append(57)
		forbiden.append(86)
		forbiden.append(87)

		
		forbiden.append(95)
		
		forbiden.append(111)
		forbiden.append(123)
		forbiden.append(131)
		forbiden.append(132)
		forbiden.append(137)
		forbiden.append(140)
		forbiden.append(141)
		forbiden.append(147)
		forbiden.append(156)
		forbiden.append(168)
		forbiden.append(171)
		forbiden.append(173)

		
		forbiden.append(179)
		
		
		
		
		forbiden.append(185)
		forbiden.append(189)
		forbiden.append(193)
		forbiden.append(200)
		
		forbiden.append(202)
		forbiden.append(203)
		forbiden.append(204)
		forbiden.append(205)	
		remarksraportstemp = q_run(connD, querry)
		RemExistList =list()
		for line in remarksraportstemp:
			RemExistList.append(str(str(line[2]).strip() + '###' + str(line[0]).strip()+'###'+str(line[1]).strip()+'###'+str(line[3]).strip()))
		p = -1
		reportlist1 = list()
		for line in measurements:
			p += 1
			lim = countLimit(line[3],line[2])

			if line[6] not in forbiden:
				if str(lim) == 'Cl. D' or str(lim) == 'V. III':
					#print(str(line[1]) + ' ' + str(line[5]) + ' ' + str(lim) + ' ' + str(line[3]) + ' ' + str(line[2]) )
					strip = str(str(line[4]).strip() +'###'+ str(line[1]).strip()+'###'+str(line[0]).strip()+'###'+str(line[5]).strip())
					if not strip in reportlist1:
						reportlist1.append(strip)
		print('Ilosc pomiarow w klasie D: ' + str(len(reportlist1)))
		
		replist =  [item for item in reportlist1 if item not in RemExistList]

		print('Ilosc pomiarow w klasie D bez remarksa: ' + str(len(replist)))
		replist.sort()
		return (replist)
		
		
		
		
r1 = ClDNoRem()		


with open('Class D no remark.csv', 'w', newline='') as file:
	for l in r1:
		file.write(l)
		file.write('\n')