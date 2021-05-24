from kakebo import app
from flask import jsonify #jsonify hace lo mismo que json.dumps
import sqlite3


@app.route('/')
def index():
    conexion = sqlite3.connect("movimientos.db")
    cur = conexion.cursor() #Cur es una clase para recorrer la base de datos

    cur.execute('SELECT * FROM movimientos;')

    claves = cur.description #para crear un diccionario

    filas = cur.fetchall() #fetchall es un metodo que devuelve todas las filas de la base de datos que hemos traido con execute, por si queremos utilizarlas para una variable por ejemplo
    movimientos = []

    for fila in filas:
        d = {}
        for tuplaclave, valor in zip(claves, fila):
            d[tuplaclave[0]] = valor
        movimientos.append(d)
    
    conexion.close()

    return jsonify(movimientos)