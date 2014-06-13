from flask import Flask
app = Flask(__name__, instance_relative_config=True)  # activate the instance folder
app.config.from_object('config.default')  # access app.config.default["var name"] and loads default config
app.config.from_pyfile('config.py')  # loads the instance/config.py file
app.config.from_envvar('APP_CONFIG_FILE')  # loads the variable specified from env var set in run.py

