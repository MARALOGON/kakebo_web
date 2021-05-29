from kakebo import app
from flask import jsonify, render_template, request, redirect, url_for  #jsonify hace lo mismo que json.dumps
from kakebo.forms import MovimientosForm

import sqlite3

@app.route('/')
def index():
    conexion = sqlite3.connect("movimientos.db")
    cur = conexion.cursor()

    cur.execute("SELECT * FROM movimientos;")

    claves = cur.description
    filas = cur.fetchall()
    movimientos = []
    saldo = 0
    for fila in filas:
        d = {}
        for tclave, valor in zip(claves, fila):
            d[tclave[0]] = valor
            print(d)
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
    formulario = MovimientosForm()

    if request.method == 'GET':
        return render_template('alta.html', form = formulario)
    else:

        if formulario.validate():
            conexion = sqlite3.connect("movimientos.db")
            cur = conexion.cursor()

            #Esta es la forma que utilizamos para poder insertar datos en el formulario utilizando SQLite
            query = "INSERT INTO movimientos (fecha, concepto, categoria, esGasto, cantidad) VALUES (?, ?, ?, ?, ?)" 
            #Lo que va entre comillas es una cadena multilinea, que asignada a una variable, Python va a ejecutar
            try:
                cur.execute(query, [formulario.fecha.data, formulario.concepto.data, formulario.categoria.data,
                                formulario.esGasto.data, formulario.cantidad.data])

            except sqlite3.Error as el_error:
                print("Error en SQL INSERT", el_error)
                return render_template('alta.html', form=formulario)


            #Esto es otra forma de escribir lo mismo que lo de encima (INSERT INTO)
            """ 
            query = "INSERT INTO movimientos (fecha, concepto, categoria, esGasto, cantidad) VALUES (:fecha, :concepto, :categoria, :esGasto, :cantidad)"
            cur.execute(query, {
                'fecha': formulario.fecha.data, 
                'concepto': formulario.concepto.data, 
                'categoria': formulario.categoria.data,
                'esGasto': formulario.esGasto.data, 
                'cantidad':formulario.cantidad.data
            }
            """
            #1. Insertar el movimiento en la base de datos
            conexion.commit() #Siempre que se haga un insert, delete, update, etc. para modificar datos de la database, ha de hacerse un commit para fiarlos, si no no se van a grabar
            conexion.close()

            return redirect(url_for("index"))

           #2. Redirect a la ruta /
        else:
            return render_template('alta.html', form = formulario)
