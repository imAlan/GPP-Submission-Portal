from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired


class LogInForm(Form):
    username = StringField('Username', validators=[InputRequired(message="Input Required")])
    password = PasswordField('Password', validators=[InputRequired(message="Input Required")])
    remember_me = BooleanField('Keep me logged in')
    login = SubmitField('Login')