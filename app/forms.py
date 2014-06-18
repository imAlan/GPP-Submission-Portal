from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired


class LogInForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SubmitForm1(Form):
    title = StringField('Title', validators=[DataRequired()])
    type_ = SelectField('')
