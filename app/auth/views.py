from flask import render_template, redirect, url_for, request
from . import auth
from .forms import LogInForm, ForgotPasswordForm, AccountForm
from ..models import User, db
from flask.ext.login import login_user, login_required, logout_user, current_user
import datetime

@auth.route('/', methods=['POST', 'GET'])
def index():
    if current_user.is_authenticated():
        return redirect(url_for('home'))
    form = LogInForm(request.form)
    PassForm = ForgotPasswordForm(request.form)
    AccForm = AccountForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        password = form.password.data
        if user is not None and user.verify_password(password):
            login_user(user, remember=form.remember_me.data)
            user.last_visited = datetime.date.today()
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('auth/index.html', form=form, PassForm=PassForm, AccForm=AccForm)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))