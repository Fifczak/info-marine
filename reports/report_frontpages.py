from docx import *
from docx import Document
from docx.shared import Inches
from docx.shared import Pt
from docx.shared import RGBColor

from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.text import WD_BREAK
from docx.enum.text import WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER

from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

def standard(document):
	H1 = document.add_paragraph('Measurement condition')
	H1.style = document.styles['IM HEAD']
	H1.alignment = WD_ALIGN_PARAGRAPH.LEFT
	T1 = document.add_paragraph('Measurements were taken during normal operating condition.')
	T1.style = document.styles['IM TEXT']
	T1.alignment = WD_ALIGN_PARAGRAPH.LEFT
	H2 = document.add_paragraph('Results presentation')
	H2.style = document.styles['IM HEAD']
	H2.alignment = WD_ALIGN_PARAGRAPH.LEFT
	

	T1 = document.add_paragraph()
	r0 = T1.add_run('Measured values are presented in the table below. Each machine if applicable is separated for driver (el. motor, diesel engine, etc.) and driven unit (pump, compressor, etc.). ')
	r1 = T1.add_run('First column ')
	r1.italic = True
	r1.underline = True
	r2 = T1.add_run('of the table consist name of the equipment. ')
	r1 = T1.add_run('Second column ')
	r1.italic = True
	r1.underline = True
	r2 = T1.add_run('contains the highest value of vibration velocity measured on the equipment in all measurement points.')
	r1 = T1.add_run('Third column ')
	r1.italic = True
	r1.underline = True
	r2 = T1.add_run('contains classification of the vibration class according to proper ISO standard and other normative documents. Classification depends on highest reading of measured equipment only. ')
	r1 = T1.add_run('Fourth column ')
	r1.italic = True
	r1.underline = True
	r2 = T1.add_run('contains additional readings of enveloped value of acceleration, which is helpful in detection of early stage of bearing wear. ')
	r1 = T1.add_run('Fifth column ')
	r1.italic = True
	r1.underline = True
	r2 = T1.add_run('contains vibration trend values if previous results are available from the same source. ')
	r1 = T1.add_run('Sixth column  ')
	r1.italic = True
	r1.underline = True
	r2 = T1.add_run('contains remarks and suggestions based on the analysis of vibration signal. This column can be taken as the final conclusion about machine condition. If cell is empty, it means that there is no existing problem or defect shown in vibration signal.')
	T1.style = document.styles['IM TEXT']
	T1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

	
