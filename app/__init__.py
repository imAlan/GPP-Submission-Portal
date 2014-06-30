from flask import Flask
from .auth import auth as auth_blueprint
from flask.ext.login import LoginManager
# activate the instance folder

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

app = Flask(__name__, instance_relative_config=True)

from config import *

app.register_blueprint(auth_blueprint, url_prefix='/auth')

from app.models import db
db.init_app(app)

app.config.from_object('config')

from app import views

login_manager.init_app(app)


