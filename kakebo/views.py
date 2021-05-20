from kakebo import app
import sqlite3

@app.route('/')
def index():
    conexion = sqlite3.connect("movimientos.db")
    cur = conexion.cursor()

    cur.execute('SELECT * FROM movimientos;')

    claves = cur.description #para crear un diccionario

    filas = cur.fetchall()
    l = []

    for fila in filas:
        d = {}
        for columna in fila:
    
    conexion.close()

    return "Consulta realizada"