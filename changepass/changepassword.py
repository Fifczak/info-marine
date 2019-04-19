import psycopg2

from tkinter import *


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

def changepass():

    querry = "alter user " + str(loginin.get()) + " with password '" + str(pw_new_in.get()) + "'"
    q_run(connD,querry)
    print('DONE')
#connD=['testuser','info','localhost']
connD=['dbadmin','242QhpbS&9Fv','192.168.10.243']
frame=Tk()
login=Label(frame,text='Login')
login.grid(row=0, column=0)
loginin=Entry(frame)
loginin.grid(row=0, column=1)



pw_new=Label(frame, text='New PW')
pw_new_in=Entry(frame,show='*')

pw_new.grid(row=2,column=0)
pw_new_in.grid(row=2,column=1)

ok=Button(frame,text='zatwierdz',command = changepass)

ok.grid(row=3,column=1)
frame.mainloop()

print(loginin.get())


conn=psycopg2.connect(cs)


