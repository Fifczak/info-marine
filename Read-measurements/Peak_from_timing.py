import psycopg2
from math import sqrt, fabs
connD = ['testuser','info','192.168.10.243']

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



def recountoverall(id,RN):
    querry = """
    SELECT point from meascharts where report_number = '{}'
     and id ={} and type = 'Vel' and domain = 'TIM' group by point
    """.format(RN,id)

    pointslist = q_run(connD, querry)

    for point in pointslist:
        x = []
        querry = """SELECT chart from meascharts where report_number = '{}' 
        and id = {} and domain = 'TIM' and point = '{}' limit 1 """.format(RN, id, point[0])
        chartstr = q_run(connD, querry)[0][0]
        chartstrlist = chartstr.split(";")
        for line in chartstrlist:
            x.append(float(line))

        xlen = int(len(x) - 2)
        tp = x[0]
        dt = (x[1] / xlen)
        x = x[2:]
        xbz = [fabs(xc) for xc in x]


        # sumVal = 0
        #
        # freq = float(tp)
        # for m in x:
        #     if freq > FROM and freq < TO:  ## TUTAJ BEDZIE TRZEBA ZROVBC ZMIENNE ZAKRESY W ZALEZNOSCI OD STATKU / URZADZENIA / NORMY
        #         sumVal += pow(m, 2)
        #     freq += float(dt)
        # overall = round(sqrt(sumVal), 3)
        print(point[0], max(xbz))


id = input("Device id:")


recountoverall(id,'TIMINGTEST')