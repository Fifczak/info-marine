from DS_A import *


from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
import psycopg2
import csv
host = 'localhost'
ownerlist = []
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
def Login():
	def LogApplication(root): ## PYINSTALLER MA JAKIES PROBLEMY Z PSYCOPG W TEJ FUNKCJI - > JEST JAKIS WYJATEK
		var = IntVar()
		def makeWin():
			title = tk.Label(root, text="Info Datasheet")#TITLE 
			title.grid(row=0, column=2)
			user_entry_label = tk.Label(root, text="Username: ")#USERNAME LABEL
			user_entry_label.grid(row=1, column=1)
			user_entry = tk.Entry(root, text="Username: ")  #USERNAME ENTRY BOX
			user_entry.grid(row=1, column=2)
			pass_entry_label = tk.Label(root, text="Password: ")#PASSWORD LABEL
			pass_entry_label.grid(row=2, column=1)
			pass_entry = tk.Entry(root, show="*")    #PASSWORD ENTRY BOX
			pass_entry.grid(row=2, column=2)
			with open('log.csv') as csvfile:
				openfile = csv.reader(csvfile, delimiter=' ')
				p = -1
				for lines in openfile:
					p += 1
					if p == 0:
						user_entry.insert(0,str(lines[0]))
					if p == 1:
						pass_entry.insert(0,str(lines[0]))
			var = IntVar()
			checksave = tk.Checkbutton(root, text="Remember", variable=var)      
			checksave.grid(row=3, column=2)
			sign_in_butt = Button(root, text="Sign In",command = lambda ue = user_entry, pe = pass_entry:logging_in(ue,pe))
			sign_in_butt.grid(row=5, column=2)
		
		def logging_in(user_entry,pass_entry):
			user_get = user_entry.get()#Retrieve Username
			pass_get = pass_entry.get()#Retrieve Password
			if bool(var.get()) == True:
				config = Path('log.csv')
				with open('log.csv', 'w', newline='') as csvfile:
					filewriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
					filewriter.writerow([user_get])
					filewriter.writerow([pass_get])
			connD = [user_get,pass_get,host]
			querry = "SELECT current_user"
			try:
				usercheck =  q_run(connD,querry)#PYINSTALLER ma problemy gdzies tu
				
			except:
				pass
			if usercheck:
				root.destroy()
				#print(usercheck[0])	
				querry = "select name,id from main where parent =1 order by name" 
				ownerlist = q_run(connD, querry)
				
				querry = "select name,id,parent from main where parent <> 1 order by name"
				shiplist = q_run(connD, querry)
				
				
				ShipsApplication(ownerlist,shiplist,connD)
		makeWin()	
	def ShipsApplication(ownerlist,shiplist,connD):
		def onselect(evt):
	
			shipid = tree.item(tree.selection()[0]).get('values')[0]
			#print(tree.item(tree.selection()[0]).get('values')[0])
			#print(tree.item(ident[0]).get(values))
			ShowDatasheet(connD,shipid)

			
		root2 = tk.Tk()
		root2.title("Chose ship")
			
		tree = ttk.Treeview(root2)
		i=-1
		for row in ownerlist:
			i +=1
			parent = tree.insert('','end',text=str(row[0]))
			j =-1
			for row2 in shiplist:
				j+=1
				if str(row[1]) == str(row2[2]):
					tree.insert(parent,'end',text=str(row2[0]),values=(shiplist[j][1]))
					
			#print(parent)
		tree.bind('<Double-Button>', onselect)
		tree.pack(fill=BOTH, expand=1)
			
		

	root = tk.Tk()
	root.title("Login")
	root.geometry("200x120")
	LogApplication(root) #The frame is inside the widgit
	root.mainloop()
	#Keeps the window open/running

	
	
	
Login()