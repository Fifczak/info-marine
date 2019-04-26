from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt


def devicetable ( document ):
    H = document.add_paragraph ( 'Measurement equipment' )
    H1 = document.add_paragraph ( 'Measurement equipment' ,style='List Bullet' )
    H.runs[ 0 ].font.name = 'Times New Roman'
    H.runs[ 0 ].font.size = Pt ( 12 )
    H.runs[ 0 ].bold = True

    devtab = document.add_table ( rows=6 ,cols=2 )
    devtab.style = 'Table Grid'
    devtab.cell ( 0 ,0 ).merge ( devtab.cell ( 0 ,1 ) )
    devtab.cell ( 0 ,0 ).text = 'Technical data'
    devtab.cell ( 0 ,0 ).paragraphs[ 0 ].alignment = WD_ALIGN_PARAGRAPH.CENTER
    devtab.cell ( 1 ,0 ).text = 'Maker:'
    devtab.cell ( 1 ,1 ).text = 'Info Marine'
    devtab.cell ( 2 ,0 ).text = 'Serial number:'
    devtab.cell ( 3 ,0 ).text = 'Date of manufacture:'
    devtab.cell ( 4 ,0 ).text = 'Measuring range:'
    devtab.cell ( 5 ,0 ).text = 'Indication error:'
