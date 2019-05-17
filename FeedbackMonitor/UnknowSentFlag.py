import psycopg2
import csv
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *



username = 'testuser'
password = 'info'
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

def unknowremarks():
	class backquerry(object):
		def __init__(self):
			self.querry = ''

	SendRemList = list()
	marksendWindow = tk.Tk()
	marksendWindow.title("Sender marker")
	strvar = StringVar()
	def loadsendremlist(SendRemList):
		querry = "select id,raport_number,remark from remarks where sended is null and raport_number is not null and id is not null and raport_number <> '' and remark <>'' order by raport_number, id"
		SendRemList.clear()
		for item in q_run(connD,querry):
			SendRemList.append(item)
		return SendRemList
		
	def refresh():
		querry = "select id,raport_number,remark from remarks where sended is null and raport_number is not null and id is not null and raport_number <> '' and remark <>'' order by raport_number, id"
		SendRemList.clear()
		for item in q_run(connD,querry):
			SendRemList.append(item)
		labelcount.configure(text='Remarks left: ' + str(len(SendRemList)))
		remarktext.delete(1.0, END)
		rem_ = str(SendRemList[0][2])
		remarktext.insert(INSERT, rem_)
		
	def setyes():
		id_ = str(SendRemList[0][0])
		rn_ = str(SendRemList[0][1])
		querry = "update remarks set sended = true where id = " + id_ + " and raport_number = '" + rn_ + "'"
		q_run(connD,querry)
		savelast()
		refresh()
		
	def setno():
		id_ = str(SendRemList[0][0])
		rn_ = str(SendRemList[0][1])
		querry = "update remarks set sended = false where id = " + id_ + " and raport_number = '" + rn_ + "'"
		q_run(connD,querry)
		savelast()
		refresh()
	
	def savelast():
		id_ = str(SendRemList[0][0])
		rn_ = str(SendRemList[0][1])
		backquerry.querry = "update remarks set sended = null where id = " + id_ + " and raport_number = '" + rn_ + "'"
		
	def back():
		q_run(connD,backquerry.querry)
		refresh()
		
		
	SendRemList = loadsendremlist(SendRemList)
	labelcount = tk.Label(marksendWindow, text  = 'Remarks left: ' + str(len(SendRemList)) )
	remarktext = tk.Text(marksendWindow,height=30, width=50)
	ButtonYes = tk.Button(marksendWindow,text = "SENT",command = setyes)
	ButtonNo = tk.Button(marksendWindow,text = "NOT SENT",command = setno)
	ButtonBack = tk.Button(marksendWindow,text = "BACK",command = back)
	remarktext.delete(1.0,END)
	try:
		remarktext.insert(INSERT, SendRemList[0][2])
	except:
		print('Error: Empty SendRemList')
	labelcount.pack()
	remarktext.pack()
	ButtonYes.pack()
	ButtonNo.pack()	
	ButtonBack.pack()	
	marksendWindow.mainloop()
unknowremarks()