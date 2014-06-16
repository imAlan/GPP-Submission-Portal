from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
# activate the instance folder
app = Flask(__name__, instance_relative_config=True)

# access app.config.default["var name"] and loads default config
app.config.from_object('config.default')
# loads the instance/config.py file
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)



