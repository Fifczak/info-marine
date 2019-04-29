def shipdata ( document ) :
    document.add_paragraph ( 'cos tam' )
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
