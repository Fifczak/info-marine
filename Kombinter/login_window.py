from tkinter import *
from tkinter import messagebox

import psycopg2


def base_check ( login ,pw ):
    cs_local = "dbname='postgres' user = 'postgres' port='5432' host='localhost'"
    conn = psycopg2.connect ( cs_local )
    cur = conn.cursor ()
    querry = 'select * from adm_users'
    cur.execute ( querry )
    result = cur.fetchall ()
    # print('Login: ' +str(result[0][0]))
    # print('Password: ' +str(result[0][1]))

    if login == str ( result[ 0 ][ 0 ] ) and pw == str ( result[ 0 ][ 1 ] ):
        print ( 'You have been logged in as ' + str ( result[ 0 ][ 0 ] ) )
        kill ()
        mainmenu ()
    else:
        messagebox.showinfo ( 'Access denied' ,'Wrong login and/or password' )


def val ():
    text_login = str ( login_input.get () )
    # print(text_login)
    text_pw = str ( pw_input.get () )
    # print(text_pw)
    base_check ( text_login ,text_pw )
    return


def kill ():
    root.destroy ()
    return


def loginwindow ():
    global login_input ,pw_input ,root
    root = Tk ()
    root.title ( 'Login' )
    login_label = Label ( root ,text='Login:' )
    login_label.grid ( column=0 ,row=0 )
    login_input = Entry ( root )
    login_input.grid ( column=1 ,row=0 )
    pw_label = Label ( root ,text='Password:' )
    pw_label.grid ( column=0 ,row=1 )
    pw_input = Entry ( root ,show='*' )
    pw_input.grid ( column=1 ,row=1 )
    ok_button = Button ( root ,text='OK' ,command=val )
    ok_button.grid ( column=1 ,row=2 )
    quit_button = Button ( root ,text='Quit' ,command=kill )
    quit_button.grid ( column=2 ,row=2 )
    root.mainloop ()


loginwindow ()
