import mysql.connector

conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                   auth_plugin='mysql_native_password')

mycursor = conn.cursor(buffered=True)
mycursor.execute("SELECT nombre_tabla FROM nttcs_cf.asociacion_marcos;")
def leerTablas():
    archivo = open('tablas.txt', "r")
    tablas = archivo.read()
    tablas = tablas.split('\n')
    return tablas
def insertarColumnas(tablas):

    for i in tablas:
        c = conn.cursor(buffered=True)
        try:
            c.execute("ALTER TABLE " + i + " ADD comentario2 TEXT NULL;")
            c.execute("ALTER TABLE " + i + " ADD comentario TEXT NULL;")
            print(i+' anadido correctamente')
        except:
            print(i+' ya anadido')

t = leerTablas()
insertarColumnas(t)
print('ejecucion Terminada')