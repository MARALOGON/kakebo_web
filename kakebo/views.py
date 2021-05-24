from kakebo import app
from flask import render_template, jsonify #jsonify hace lo mismo que json.dumps
import sqlite3


@app.route('/')
def index():

    conexion = sqlite3.connect("movimientos.db")
    cur = conexion.cursor() #Cur es una clase para recorrer la base de datos

    cur.execute('SELECT * FROM movimientos;')

    claves = cur.description #para crear un diccionario

    filas = cur.fetchall() #fetchall es un metodo que devuelve todas las filas de la base de datos que hemos traido con execute, por si queremos utilizarlas para una variable por ejemplo
    movimientos = []
    saldo = 0
    for fila in filas:
        d = {}
        for tuplaclave, valor in zip(claves, fila):
            d[tuplaclave[0]] = valor
        if d['esGasto'] == 0:
            saldo = saldo + d['cantidad']
        else:
              saldo = saldo - d['cantidad']
        d['saldo'] = saldo
        movimientos.append(d)
    
    conexion.close()

    return render_template('movimientos.html', datos = movimientos)


@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    return render_template('alta.html')
