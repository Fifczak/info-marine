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

#filepath = 'C:\\overmind\\Data\\base.docx'
def loadstyles(document):

  obj_styles = document.styles
  
  obj_charstyle = obj_styles.add_style('IM HEAD',WD_STYLE_TYPE.PARAGRAPH)
  style = document.styles['IM HEAD']
  font = style.font
  font.name = 'Cambria'
  font.size = Pt(16)
  font.color.rgb = RGBColor(54, 95, 145) 
  
  
  obj_charstyle = obj_styles.add_style('IM TEXT',WD_STYLE_TYPE.PARAGRAPH)
  style = document.styles['IM TEXT']
  font = style.font
  font.name = 'Times New Roman'
  font.size = Pt(12)
  font.color.rgb = RGBColor(0, 0, 0) 
  
  
  obj_charstyle = obj_styles.add_style('HEADTABLE text',WD_STYLE_TYPE.PARAGRAPH)
  style = document.styles['HEADTABLE text']
  font = style.font
  font.name = 'Calibri'
  font.size = Pt(12)
  
  
  
  
  
  
  obj_charstyle = obj_styles.add_style('Head',WD_STYLE_TYPE.PARAGRAPH)
  style = document.styles['Head']
  font = style.font
  font.name = 'Calibri'
  font.size = Pt(16)
  font.bold = True
  font.color.rgb = RGBColor(68, 114, 196)

  obj_charstyle = obj_styles.add_style('listlvl1',WD_STYLE_TYPE.PARAGRAPH)
  style = document.styles['listlvl1']
  font = style.font
  font.name = 'Calibri Light'
  font.size = Pt(16)
  font.bold = True
  font.color.rgb = RGBColor(47, 84, 150)


  obj_charstyle = obj_styles.add_style('listlvl2',WD_STYLE_TYPE.PARAGRAPH)
  style = document.styles['listlvl2']
  font = style.font
  font.name = 'Calibri Light'
  font.size = Pt(13)
  font.bold = True
  font.color.rgb = RGBColor(47, 84, 150)

  obj_charstyle = obj_styles.add_style('texthead',WD_STYLE_TYPE.PARAGRAPH)
  style = document.styles['texthead']
  font = style.font
  font.name = 'Calibri Light'
  font.size = Pt(11)
  font.bold = True

  obj_charstyle = obj_styles.add_style('textheadU',WD_STYLE_TYPE.PARAGRAPH)
  style = document.styles['textheadU']
  font2 = style.font
  font2.name = 'Calibri Light'
  font2.size = Pt(11)
  font2.bold = True
  font2.underline = True

  obj_charstyle = obj_styles.add_style('text',WD_STYLE_TYPE.PARAGRAPH)
  style = document.styles['text']
  font = style.font
  font.name = 'Calibri'
  font.size = Pt(11)

  obj_charstyle = obj_styles.add_style('textB',WD_STYLE_TYPE.PARAGRAPH)
  style = document.styles['textB']
  font = style.font
  font.name = 'Calibri'
  font.size = Pt(11)
  font.bold = True

  obj_charstyle = obj_styles.add_style('warning',WD_STYLE_TYPE.PARAGRAPH)
  style = document.styles['warning']
  font = style.font
  font.name = 'Calibri Light'
  font.size = Pt(13)


  obj_charstyle = obj_styles.add_style('description',WD_STYLE_TYPE.PARAGRAPH)
  style = document.styles['description']
  font = style.font
  font.name = 'Calibri'
  font.size = Pt(9)
  font.italic = True
