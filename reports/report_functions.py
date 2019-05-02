def getname ( host ,username ,password ):
    kport = "5432"
    kdb = "postgres"
    cs = "dbname=%s user=%s password=%s host=%s port=%s" % (kdb ,username ,password ,host ,kport)
    conn = None
    conn = psycopg2.connect ( str ( cs ) )
    cur = conn.cursor ()
    querry = "select full_name from users where login = '" + str ( username ) + "' limit 1;"
    cur.execute ( querry )
    result = cur.fetchall ()
    conn.commit ()
    cur.close ()
    return result


def getini ( host ,username ,password ):
    kport = "5432"
    kdb = "postgres"
    cs = "dbname=%s user=%s password=%s host=%s port=%s" % (kdb ,username ,password ,host ,kport)
    conn = None
    conn = psycopg2.connect ( str ( cs ) )
    cur = conn.cursor ()
    querry = "select ini from users where login = '" + str ( username ) + "' limit 1;"
    cur.execute ( querry )
    result = cur.fetchall ()
    conn.commit ()
    cur.close ()
    return result
