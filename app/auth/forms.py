from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Email


class LogInForm(Form):
    username = StringField('Username', validators=[InputRequired(message="This field is Required")])
    password = PasswordField('Password', validators=[InputRequired(message="This field is Required")])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')


class ForgotPasswordForm(Form):
    email = StringField('Email', validators=[InputRequired(message="This field is required"), Email(message="Not a valid email address") ])
    submit = SubmitField('Submit')


class AccountForm(Form):
    name = StringField('Name', validators=[InputRequired(message="This field is required")])
    email = StringField('Email', validators=[InputRequired(message="This field is required"), Email(message="Not a valid email address")])
    agency = StringField('Agency', validators=[InputRequired(message="This field is required")])
    message = TextAreaField('Message', validators=[InputRequired(message="This field is required")])
    submit = SubmitField('Submit')