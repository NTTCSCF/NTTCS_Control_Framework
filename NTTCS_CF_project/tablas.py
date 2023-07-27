import mysql.connector
import openpyxl, xlsxwriter

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

def leerExcel():

    excel_document = openpyxl.load_workbook("NTTCS Control Framework 2023.1.2.xlsx")
    sheet = excel_document['Mappings']
    salida = []
    for i in range(2, 1170):
        fila = []
        for j in range(0, 76):
            letra = xlsxwriter.utility.xl_col_to_name(j)
            valor = letra + str(i)
            if j != 0:
                if (sheet[valor].value != None):
                    fila += [1]
                else:
                    fila += [0]
            else:
                fila += [sheet[valor].value]
        salida += [fila]
    return salida

def escribirExcel(tabla):
    excel_document = openpyxl.Workbook()
    sheet = excel_document.active
    contadorFila = 1
    for i in tabla:
        contadorColumna = 0
        for j in i:
            letra = xlsxwriter.utility.xl_col_to_name(contadorColumna)
            valor = letra + str(contadorFila)
            sheet[valor].value = j
            contadorColumna += 1
        contadorFila += 1
    excel_document.save("demo.xlsx")
r = leerExcel()
tablas = leerTablas()
tablas = ['NTT_ID'] + tablas
tabla = [tablas] + r
escribirExcel(tabla)
print(tabla)
