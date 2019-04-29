from docx.enum.text import WD_ALIGN_PARAGRAPH
def shipdata ( document ) :
    # sdata-nazwa dla tabeli z danymi statku
    sdata = document.add_table ( rows=3 ,cols=2 )
    # konwencja: c - nr komórki, 1 liczba oznacza indeks wiersza 2 liczba indeks kolumny
    c00 = sdata.cell ( 0 ,0 ).paragraphs[ 0 ].add_run ( 'Ship Type:' )
    c00.bold = True
    sdata.style = 'Table Grid'
    c00.add_break ()
    sdata.cell ( 0 ,0 ).paragraphs[ 0 ].add_run ( 'tu str(q)' )
    c10 = sdata.cell ( 1 ,0 ).paragraphs[ 0 ].add_run ( 'Sea depth:' )
    c10.bold = True
    c10.add_break ()
    sdata.cell ( 1 ,0 ).paragraphs[ 0 ].add_run ( 'Least two times greater than Vessel draught.' )
    c01 = sdata.cell ( 0 ,1 ).paragraphs[ 0 ].add_run ( 'Main dimensions: ' )
    c01.bold = True
    # sdata.cell(0,1).paragraphs[0].alignment=WD_ALIGN_PARAGRAPH.CENTER
    sdata.cell ( 0 ,1 ).paragraphs[ 0 ].runs[ 0 ].alignment = WD_ALIGN_PARAGRAPH.CENTER
    sdata.cell ( 0 ,1 ).paragraphs[ 0 ].add_run ().add_break ()
    sdata.cell ( 0 ,1 ).paragraphs[ 0 ].add_run ( 'Lenght BP.....' + 'zmienna z wynikiem querry' ).add_break ()
    sdata.cell ( 0 ,1 ).paragraphs[ 0 ].add_run ( 'Bradth.............' + 'zmienna z wynikiem querry' )
    sdata.cell ( 1 ,1 ).paragraphs[ 0 ].add_run ( 'Weather conditions: ' ).bold = True
    weather = sdata.cell ( 1 ,1 ).add_paragraph ( '-' ).alignment = WD_ALIGN_PARAGRAPH.CENTER
    sdata.cell ( 1 ,1 ).add_paragraph ()
    sdata.cell ( 2 ,0 ).merge ( sdata.cell ( 2 ,1 ) )
