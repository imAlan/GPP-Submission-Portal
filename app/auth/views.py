from flask import render_template, flash, redirect, url_for, request
from . import auth
from .forms import LogInForm
from ..models import User
from flask.ext.login import login_user

@auth.route('/')
@auth.route('/index', methods=['POST', 'GET'])
def index():
    form = LogInForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        password = form.password.data
        print "validated"
        if user is not None and user.verify_password(password):
            login_user(user, form.remember_me.data)
            return redirect(url_for('home'))
    return render_template('auth/index.html', form=form)