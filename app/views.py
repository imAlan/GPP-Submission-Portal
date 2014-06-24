from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import LogInForm, SubmitForm1
from models import Document, User, Submit, db
from app import app

Bootstrap(app)

app.config['SECRET_KEY'] = 'hi'

@app.route('/')
@app.route('/index')
def index():
    db.create_all()
    form = LogInForm()
    #user = User.query.first()
    #print user.username
    return render_template('index.html', form=form)

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/submit1', methods=['POST', 'GET'])
def submit():
    form = SubmitForm1(request.form)
    if request.method == 'POST' and form.validate():
        print "done"
    return render_template('submit.html', form=form)

@app.route('/testdb')
def testdb():
    db.create_all()
    return redirect(url_for('index'))
