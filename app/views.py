from flask import render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
from forms import SubmitForm1, SignUpForm, SubmitForm2
from models import Document, User, db
from flask.ext.login import login_required
from app import app
import datetime, json, requests, re
from werkzeug.urls import url_fix
from urlparse import urlparse
from pattern.web import URL

Bootstrap(app)

#app.config['SECRET_KEY'] = 'Key To Be Determine'

@app.route('/home')
@login_required
def home():
    for s in session:
        print s
    print session['user_id']
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
        part = form.part_question.data
        url = form.url_question.data
        if part == 'No':
            section = 1
        else:
            section = form.num.data
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
    form = SubmitForm2()
    form1data = json.loads(session['form1data'])
    url_errors = []
    section_errors = []
    pdf_errors = []
    status_errors = []
    if form.validate_on_submit():
        for v in request.form:
            if request.form[v] == '':
                check = v.split('_')
                if check[0] == 'url':
                    url_errors.append(int(check[1]))
                elif check[0] == 'section':
                    section_errors.append(int(check[1]))
            else:
                if 'url' in v:
                    #checks if url is pdf link
                    url = request.form[v]
                    print "requesting: " + url
                    try:
                        parsed_url = urlparse(url)
                        if not parsed_url.scheme:
                            url = "http://" + url
                        proxies = {"http": "http://cscisa.csc.nycnet:8080/array.dll?Get.Routing.Script"}
                        r = requests.get(url_fix(url), proxies=proxies, timeout=1)
                        if r.status_code == 404:
                            status_errors.append(int(v.split('_')[1]))
                        if r.headers['content-type'] != 'application/pdf':
                            pdf_errors.append(int(v.split('_')[1]))
                    except requests.exceptions.Timeout:
                        match = re.search('[\w%+\/-].pdf', request.form[v])
                        if not match:
                            pdf_errors.append(int(v.split('_')[1]))
        if pdf_errors or section_errors or url_errors or status_errors:
            pass
        else:
            for doc in range(len(request.form)):
                url = 'url_' + str(doc+1)
                section = 'section_' + str(doc+1)
                url = request.form.get(url)
                section = request.form.get(section)
                date_created = datetime.date(int(form1data['year']), int(form1data['month']), int(form1data['day']))
                doc = Document(title=form1data['title'], type=form1data['type'], description=form1data['description'], dateCreated=date_created, agency=session['agency'], doc_url=url)
    if form1data['part_question'] == 'Yes':
        sections = form1data['section']
    else:
        sections = 1
    url_or_file = form1data['url_question']
    return render_template('submit2.html', form=form, submit2form=request.form, sections=int(sections), url_or_file=url_or_file, url_errors=url_errors, section_errors=section_errors, status_errors=status_errors ,pdf_errors=pdf_errors)

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

@app.route('/testdb')
def testdb():
    db.drop_all()
    db.create_all()
    return redirect('http://localhost:5000/auth/index')