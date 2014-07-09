from flask import render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
from forms import SubmitForm1, SignUpForm, SubmitForm2
from models import Document, User, db
from flask.ext.login import login_required
from app import app
import datetime, json

Bootstrap(app)

#app.config['SECRET_KEY'] = 'Key To Be Determine'

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/submit1', methods=['POST', 'GET'])
@login_required
def submit():
    form = SubmitForm1(request.form)
    if form.validate_on_submit():
        title = form.title.data
        type_ = form.type_.data
        description = form.description.data
        year = form.year.data
        month = form.month.data
        day = form.month.data
        section = form.num.data
        part = form.part_question.data
        url = form.url_question.data
        #date_created = datetime.date(int(year), int(month), int(day))
        """
        doc = Document(title=title, type=type_, description=description, dateCreated=date_created,
                       agency="Records")
        db.session.add(doc)
        db.session.commit()
        """
        form1data = json.dumps({"title": title, "type": type_, "description": description, "year": year, "day": day, "month": month, "section": section, "url_question": url, "part_question": part})
        session['form1data'] = form1data
        return redirect(url_for('submit2'))
    return render_template('submit.html', form=form)
    # return redirect('http://ask.com')

@app.route('/submit2', methods=['POST', 'GET'])
@login_required
def submit2():
    if request.method == "POST":
        print request.form
        errors = []
        for v in request.form:
            if request.form[v] == '':
                print v
                errors.append(v)
        for doc in range(len(request.form)):
            url = 'url_' + str(doc+1)
            section = 'section_' + str(doc+1)
            url = request.form.get(url)
            section = request.form.get(section)
            print url, section
        #if errors: return error pages

    form1data = json.loads(session['form1data'])
    if form1data['part_question'] == 'Yes':
        sections = form1data['section']
    else:
        sections = 1
    url_or_file = form1data['url_question']
    form = SubmitForm2(request.form)
    return render_template('submit2.html', form=form, sections=int(sections), url_or_file=url_or_file, errors=None)

@app.route('/testdb')
def testdb():
    db.drop_all()
    db.create_all()
    return redirect(url_for('home'))

@app.route('/signup', methods=['POST', 'GET'])
@login_required
def signup():
    form = SignUpForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first = form.first.data
        last = form.last.data
        agency = form.agency.data
        phone = form.phone.data
        email = form.email.data
        user = User(username=username, password=password, first=first, last=last, agency=agency, phone=phone,email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('addUser.html', form=form)
