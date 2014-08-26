from flask import Flask
from flask.ext.login import LoginManager
from flask_bootstrap import Bootstrap
from flask.ext.mail import Mail

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.index'

app = Flask(__name__, instance_relative_config=True)
bootstrap = Bootstrap(app)
mail = Mail(app)

from .auth import auth as auth_blueprint

from config import *

app.register_blueprint(auth_blueprint, url_prefix='/')

from app.models import db
db.init_app(app)

app.config.from_object('config')

from app import views

login_manager.init_app(app)