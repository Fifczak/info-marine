import csv
import psycopg2


connD=['testuser','info','localhost']
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


with open('C:\\overmind\\remarks.csv') as csvfile:
    openfile = csv.reader(csvfile, delimiter=',')
    p = -1
    for line in openfile:
        p +=1
        print(p,line)
        try:
            querry = "insert into remarks(parent,remark,raport_number,id) values ('" + str(line[0]) +"','"  +str(line[2])+"','"+str(line[5])+"','"+str(line[7]) + "')"
            q_run(connD, querry)
            print(querry)
        except:
            pass