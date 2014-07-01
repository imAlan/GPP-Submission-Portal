from flask import render_template, flash, redirect, url_for, request
from . import auth
from .forms import LogInForm
from ..models import User

@auth.route('/')
@auth.route('/index', methods=['POST', 'GET'])
def index():
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print form.username.data
        if user is not None:
            return redirect(url_for('home'))
        flash('wrong username and password')
    return render_template('auth/index.html', form=form)