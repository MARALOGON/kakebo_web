from kakebo import app
from flask import jsonify, render_template, request, redirect, url_for, flash
from kakebo.forms import MovimientosForm, FiltraMovimientosForm, 
from datetime import date

import sqlite3


#Hacemos una funcion para refactorizar el codigo. Todo lo que se refiere a las consultas (query) de la base de datos irá ahora en esta función (cualquier update que se haga se procesa aqui en esta funcion y lo hemos sacado de def index())
def consultaSQL(query, parametros=[]):
    #1. Abrimos la conexión
    conexion = sqlite3.connect("movimientos.db")
    cur = conexion.cursor()

    #2. Ejecutamos la consulta
    cur.execute(query, parametros)

    #3. Obtenemos los datos de la consulta
    claves = cur.description
    filas = cur.fetchall()

    #4. Procesar los datos para devolver una lista de diccionarios. Un diccionario pr fila
    resultado = []
    for fila in filas:
        d = {}
        for tclave, valor in zip(claves, fila):
            d[tclave[0]] = valor
        resultado.append(d)

    conexion.close()
    return resultado

def modificaTablaSQL(query, parametros=[]):
    conexion = sqlite3.connect("movimientos.db")
    cur = conexion.cursor()

    cur.execute(query, parametros)

    conexion.commit() 
    conexion.close()


@app.route('/')
def index():
    filtraForm = FiltraMovimientosForm()

    movimientos = consultaSQL('SELECT * FROM movimientos order by fecha;')
    
    saldo = 0
    for d in movimientos:
        if d['esGasto'] == 0:
            saldo = saldo + d['cantidad']
        else:
            saldo = saldo - d['cantidad']
        d['saldo'] = saldo


    return render_template('movimientos.html', datos = movimientos, formulario = filtraForm)


@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    formulario = MovimientosForm()

    if request.method == 'GET':
        return render_template('alta.html', form = formulario)
    else:

        if formulario.validate():
            
            query = "INSERT INTO movimientos (fecha, concepto, categoria, esGasto, cantidad) VALUES (?, ?, ?, ?, ?)" 
           
            try:
               modificaTablaSQL(query, [formulario.fecha.data, formulario.concepto.data, formulario.categoria.data,
                                formulario.esGasto.data, formulario.cantidad.data])

            except sqlite3.Error as el_error:
                print("Error en SQL INSERT", el_error)
                flash("Se ha producido un error en la base de datos. Pruebe en unos minutos") #Flash es una clase que va a inyectar el mensaje de error en la plantilla (alta.html, base.html, etc.) que le digamos, para que aparezca como mensaje generico cuando se produzca un error 
                return render_template('alta.html', form = formulario)
          
            return redirect(url_for("index"))

        else:
            return render_template('alta.html', form = formulario)


@app.route('/borrar/<int:id>', methods=['GET', 'POST']) #con el <int:id> hacemos llegar a la ruta "borrar" el parametro id de la tabla
def borrar(id):
    if request.method == 'GET':
        filas = consultaSQL("SELECT * FROM movimientos WHERE id=?", [id])
        if len(filas) == 0:
            flash("Este registro no existe", "error")
            return render_template('borrar.html')

        return render_template('borrar.html', movimiento=filas[0])
    else:
        try:
            modificaTablaSQL("DELETE FROM movimientos WHERE id = ?", [id])
        except sqlite3.Error as e:
            flash("Se ha producido un error de base de datos, vuelve a intentarlo", 'error')
            return redirect(url_for('index'))
        
        flash("Borrado realizado con exito", 'aviso')
        return redirect(url_for('index'))

    
@app.route('/modificar/<int:id>', methods=['GET', 'POST']) 
def modificar(id):

    if request.method == 'GET':
        filas = consultaSQL("SELECT * FROM movimientos WHERE id=?", [id])
        if len(filas) == 0:
            flash("Este registro no existe", "error")
            return render_template('modificar.html')
        registro = filas[0]
        registro['fecha'] = date.fromisoformat(registro['fecha'])
        formulario = MovimientosForm(data=registro)
        
        return render_template('modificar.html', form=formulario)

    if request.method == 'POST':
        formulario = MovimientosForm()
        if formulario.validate():
            try:
                modificaTablaSQL("UPDATE movimientos SET fecha = ?, concepto = ?, categoria = ?, esGasto = ?, cantidad = ? WHERE id = ?",
                                [formulario.fecha.data,
                                formulario.concepto.data,
                                formulario.categoria.data,
                                formulario.esGasto.data,
                                formulario.cantidad.data,
                                id]

                )
                flash("Modificación realizada con éxito", "aviso")
                return redirect(url_for("index"))
            except sqlite3.Error as e:
                print("Error en update", e)
                flash("Se ha producido un erro en acceso a base de datos. Contcte con el administrador", "error")
                return render_template('modificar.html', form=formulario)
        else:
            return render_template('modificar.html', form=formulario)