import mysql.connector

conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                   auth_plugin='mysql_native_password')

mycursor = conn.cursor(buffered=True)
mycursor.execute("SELECT nombre_tabla FROM nttcs_cf.asociacion_marcos;")

for i in mycursor:
    c = conn.cursor(buffered=True)
    try:
        c.execute("ALTER TABLE "+i[0]+" ADD ID INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT;")
        print(i[0]+' a;adido correctamente')
    except:
        print(i[0]+' ya anadido')