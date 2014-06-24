from flask import Flask


# activate the instance folder
app = Flask(__name__, instance_relative_config=True)

from config import *


from app.models import db
db.init_app(app)

from app import views


