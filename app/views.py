from flask import render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
from forms import SubmitForm1, SignUpForm
from models import Document, User, Submit, db
from app import app
import datetime

Bootstrap(app)

#app.config['SECRET_KEY'] = 'Key To Be Determine'

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/submit1', methods=['POST', 'GET'])
def submit():
    form = SubmitForm1(request.form)
    print form
    if form.validate_on_submit():
        title = form.title.data
        type_ = form.type_.data
        description = form.description.data
        year = form.year.data
        month = form.month.data
        day = form.month.data
        date_created = datetime.date(int(year), int(month), int(day))
        doc = Document(title=title, type=type_, description=description, dateCreated=date_created,
                       agency="Records")
        db.session.add(doc)
        db.session.commit()
        print "1"
        # return redirect(url_for('home'))
        return redirect('http://google.com')
    print "2"
    return render_template('submit.html', form=form)
    # return redirect('http://ask.com')

@app.route('/submit2', methods=['POST', 'GET'])
def submit2():
    return render_template('submit2.html')

@app.route('/testdb')
def testdb():
    #db.drop_all()
    db.create_all()
    return redirect(url_for('home'))

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print "it worked!"
        return redirect(url_for('home'))
    return render_template('addUser.html', form=form)
