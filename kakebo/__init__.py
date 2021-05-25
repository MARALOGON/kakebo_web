from flask import Flask

app = Flask(__name__, instance_relative_config=True) #instance relativa config = True significa que vamos a sacra la configuracion 8config.py) fuera del codigo
app.config.from_object('config')

from kakebo import views


