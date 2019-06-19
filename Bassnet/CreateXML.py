import xml.dom.minidom
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



def callback():
	rn_ =  e.get() # This is the text you may want to use later
	makexmlfile(rn_)
	master.destroy()
def makexmlfile(rn_):

	username = 'testuser '
	password = 'info'
	host = '192.168.10.243'


	connD = [ username ,password ,host ]


	querry = """
	select ml.id,dev.name,rem.remark,remi.request_date,ml.raport_number
	from measurements_low as ml
	left join devices as dev on ml.id = dev.id
	left join remarks as rem on ml.id = rem.id and ml.raport_number = rem.raport_number
	left join reminder as remi on ml.id = remi.id and ml.raport_number = remi.raport_number
	left join ds_structure as dss on dss.id = cast (ml.id as text)
	where ml.raport_number = '2069-2019'
	group by ml.id ,dev.name,rem.remark,remi.request_date,ml.raport_number, dss.sort
	order by dss.sort
	""".format(rn_)
	devlist = q_run(connD,querry)
	print(devlist)
	querry = "select id,name from main where id = (select shipid from harmonogram where report_number = '{}') ".format(rn_)
	ans = list(q_run(connD,querry))[0]

	xmltext = """<?xml version="1.0" encoding="UTF-8"?>
	<VESSEL VESSEL_CODE="{}" VESSEL_ID="{}">""".format(ans[1],ans[0])



	for item in devlist:
		xmltext += """
		<COMPONENT COMPONENT_ID="{}" COMPONEN_NAME="{}" VSLCOMP_ITEM_ID="BASS-UniqueKey" >
			<SCHEDULE_JOB JOB_ITEM_ID="BASS-JOBUniqueKey">
				<JOB_CODE>{}/{}</JOB_CODE>
				<JOB_INTERVAL>3</JOB_INTERVAL><!-- 3 = Month, value to be sync from BASS -->
				<JOB_INTERVALLENGTH>2</JOB_INTERVALLENGTH>
				<NEW_INTERVAL VALUE="N">
					<NEW_INTERVAL/>
					<NEW_INTERVALLENGTH/>
					<NEW_NEXT_DUEDATE/>
				</NEW_INTERVAL>
			</SCHEDULE_JOB>""".format(item[0], item[1].replace('&','and'),item[0],item[4])
		if str(item[2]) == 'None':
			xmltext +="""
			<CORRECTIVE_JOB VALUE="N">
				<JOB_TITLE/>
				<JOB_DESCRIPTION/>
				<JOB_NEXT_DUEDATE/>
				<JOBTYPE_CODE/>
			</CORRECTIVE_JOB>
		</COMPONENT>"""
		else:
			xmltext +="""
			<CORRECTIVE_JOB VALUE="Y">
				<JOB_TITLE>CHANGE BEARING</JOB_TITLE>
				<JOB_DESCRIPTION>{}</JOB_DESCRIPTION>
				<JOB_NEXT_DUEDATE>????-??-??</JOB_NEXT_DUEDATE>
				<JOBTYPE_CODE>CBMJ</JOBTYPE_CODE>
			</CORRECTIVE_JOB>
		</COMPONENT>""".format(item[2])


	xmltext += "</VESSEL>"






	with open("C:\\Overmind\\Reports\\" + str(rn_) + ".xml", "w") as text_file:
		text_file.write(xmltext)
master = Tk()
e = Entry(master)
e.pack()
e.focus_set()
rn_ = ''
b = Button(master, text="OK", width=10, command=callback)
b.pack()
mainloop()