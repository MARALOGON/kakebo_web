from flask import Flask

app = Flask(__name__) #Se instancia la clase Flask, siempre tiene que llevar parametro __name__. Flask es la clase de flask que es la aplicación en si, lo que va contener todo

@app.route('/')  #Este @app se llama decorador (estrucutura basica de Python). Este decorador asocia todo el contenido de la funcion a la ruta
def index(): #Siempre debajo de un decorador hay una funcion 
    return 'Hola, mundo'

@app.route('/adios')
def bye():
    return 'Hasta luego, cocodrilo'
