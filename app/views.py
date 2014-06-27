from flask import render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
from forms import LogInForm, SubmitForm1
from models import Document, User, Submit, db
from app import app
import datetime

Bootstrap(app)

#app.config['SECRET_KEY'] = 'Key To Be Determine'

@app.route('/')
@app.route('/index')
def index():
    db.drop_all()
    db.create_all()
    form = LogInForm()
    #user = User.query.first()
    #print user.username
    return render_template('index.html', form=form)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/submit1', methods=['POST', 'GET'])
def submit():
    form = SubmitForm1(request.form)
    print form
    if form.validate_on_submit():
        year = form.year.data
        month = form.month.data
        day = form.month.data
        date_created = datetime.date(int(year), int(month), int(day))
        doc = Document(title=form.title.data, type=form.type_.data, description=form.description.data, dateCreated=date_created, agency="Records")
        db.session.add(doc)
        db.session.commit()
        print "1"
        return redirect(url_for('home'))
    print "2"
    return render_template('submit.html', form=form)

@app.route('/testdb')
def testdb():
    return redirect(url_for('submit'))
