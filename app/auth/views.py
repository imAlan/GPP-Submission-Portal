from flask import render_template, redirect, url_for, request
from . import auth
from .forms import LogInForm, ForgotPasswordForm, AccountForm
from ..models import User, db
from flask.ext.login import login_user, login_required, logout_user, current_user
import datetime, os
from .. import mail
from flask.ext.mail import Message

@auth.route('/', methods=['POST', 'GET'])
def index():
    print os.environ.get('DEFAULT_MAIL_SENDER')
    print os.environ.get('RECIPIENT')
    if current_user.is_authenticated():
        return redirect(url_for('home'))
    form = LogInForm(request.form)
    PassForm = ForgotPasswordForm(request.form)
    AccForm = AccountForm(request.form)
    if request.method == 'POST' and request.form['submit'] == 'Reset Password' and PassForm.validate_on_submit():
        email = PassForm.email.data
        msg = Message(subject='Requesting Password Change', body=email, sender='chen.alan101@gmail.com',
                      recipients=['chen.alan101@gmail.com'])
        mail.send(msg)
        return redirect(url_for('home'))
    if request.method == 'POST' and request.form['submit'] == 'Request Account' and AccForm.validate_on_submit():
        return redirect(url_for('home'))
    error = None
    if request.method == 'POST' and request.form['submit'] == 'Login' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).filter(User.remove != 1).first()
        password = form.password.data
        if user is not None and user.verify_password(password):
            login_user(user, remember=form.remember_me.data)
            user.last_visited = datetime.date.today()
            user.visits += 1
            db.session.commit()
            return redirect(url_for('home'))
        else:
            error = "The email or password you entered is incorrect."
            return render_template('auth/index.html', form=form, PassForm=PassForm, AccForm=AccForm, error=error)
    return render_template('auth/index.html', form=form, PassForm=PassForm, AccForm=AccForm, error=error)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))