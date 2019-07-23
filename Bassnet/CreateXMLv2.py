import xml.etree.cElementTree as ET





root = ET.Element("BASS_INTEGRATION")
vessel = ET.SubElement(root,  'VESSEL' , VESSEL_CODE="{}".format('FREEDOM'), VESSEL_ID="{}".format('VESSEL-UniqueKey'))
#component trzeba zamknac w forze dla wszystkich urządzen(w zaleznosci od raportu?)
component = ET.SubElement(vessel,  'COMPONENT' , COMPONENT_ID="{}".format('@IM DATABASE PMS'), VSLCOMP_ITEM_ID="{}".format("BASS-UniqueKey"))
#schedulejob trzeba zamknąć w forze w zaleznosci od podziału remarksa na JOB_CODY
schedulejob = ET.SubElement(component,  'SCHEDULE_JOB' , JOB_ITEM_ID="{}".format('BASS-JOBUniqueKey'), JOB_CODE="{}/{}".format('@IM DATABASE PMS','JOB CODE STRING IE: Monhly Reading'))

##TU ZACZNIE SIE ZABAWA CO GDZIE JAK I CZEMU

newinterval = ET.SubElement(schedulejob,  'NEW_INTERVAL' , FLAG="{}".format('Y'))
if str(newinterval.attrib.get('FLAG')) == 'Y':
	newintervaltype = ET.SubElement(newinterval,'NEW_INTERVAL').text = "{}".format('@IM DATABASE INTERVALTYPE')
	newintervallength = ET.SubElement(newinterval, 'NEW_INTERVALLENGTH').text = "{}".format('@IM DATABASE INTERVALLEN')
	newnexdate = ET.SubElement(newinterval, 'NEW_NEXT_DUEDATE').text = "{}".format('@IM DATABASE DUEDATE?(AUTO?)')


newjob = ET.SubElement(schedulejob,  'NEW_JOB' , ISNEW="{}".format('Y'))



infomarineanaly = ET.SubElement(schedulejob,  'INFOMARINE_ANALY' , RESULT="{}".format('Y'))
if str(infomarineanaly.attrib.get('RESULT')) == 'Y':
	joborderitemid = ET.SubElement(infomarineanaly,'JOB_ORDER_ITEM_ID').text = "{}".format('BASS-JOBUniqueKey')
	val = ET.SubElement(infomarineanaly, 'VAL').text = "{}".format('@IM DATABASE RMS VALUE')
	env = ET.SubElement(infomarineanaly, 'ENV').text = "{}".format('@IM DATABASE ENV VALUE')
	comment = ET.SubElement(infomarineanaly, 'COMMENT').text = "{}".format('@IM DATABASE REMARK')





correctivejob  = ET.SubElement(component,  'CORRECTIVE_JOB' , ISNEW="{}".format('Y'))
if str(correctivejob.attrib.get('ISNEW')) == 'Y':
	jobtitle = ET.SubElement(correctivejob,'JOB_TITLE').text = "{}".format('REPLACE BEARING')
	jobdescription = ET.SubElement(correctivejob, 'JOB_DESCRIPTION').text = "{}".format('Job Description on how to Replace Bearing')
	jobnextduedate = ET.SubElement(correctivejob, 'JOB_NEXT_DUEDATE').text = "{}".format('2019-06-30')
	jobcode = ET.SubElement(correctivejob, 'JOBTYPE_CODE').text = "{}".format('CBMJ')



tree = ET.ElementTree(root)
tree.write("C:\\Overmind\\Reports\\filename.xml")


# -<CORRECTIVE_JOB ISNEW="Y">
#
# <JOB_TITLE>Replace Bearing</JOB_TITLE>
#
# <JOB_DESCRIPTION>Job Description on how to Replace Bearing.</JOB_DESCRIPTION>
#
# <JOB_NEXT_DUEDATE>2019-06-30</JOB_NEXT_DUEDATE>
#
# <JOBTYPE_CODE>CBMJ</JOBTYPE_CODE>
#
# </CORRECTIVE_JOB>
