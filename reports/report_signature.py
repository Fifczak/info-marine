import docx,psycopg2
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

def getname(host, username, password):
	kport = "5432"
	kdb = "postgres"
	host='localhost'
	cs = "dbname=%s user=%s password=%s host=%s port=%s"%(kdb,username,password,host,kport)
	conn = None
	conn = psycopg2.connect(str(cs))
	cur = conn.cursor()
	querry = "select full_name from users where login = '" + str(username) + "'"
	cur.execute(querry)
	print(username)
	result = cur.fetchall()
	conn.commit()
	cur.close()
	return result

def signature(document):
	username='postgres'
	password='info'
    #querry="select from users where login='"+connD[0]+"'"
	H0=document.add_paragraph()
	H0L=H0.add_run("Prepared by:").alignment=WD_PARAGRAPH_ALIGNMENT.LEFT

