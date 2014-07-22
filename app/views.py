from flask import render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
from forms import SubmitForm1, SignUpForm, SubmitForm2
from sqlalchemy import func, or_
from models import Document, User, db, Section, Submit
from flask.ext.login import login_required
from app import app
import json, datetime, requests, re, os
from werkzeug.urls import url_fix
from urlparse import urlparse
from werkzeug.utils import secure_filename
#from pattern.web import URL

Bootstrap(app)

#app.config['SECRET_KEY'] = 'Key To Be Determine'
ALLOWED_EXTENSIONS = set(['pdf'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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
        part = form.part_question.data
        url = form.url_question.data
        if part == 'No':
            section = 1
        else:
            section = form.num.data
        form1data = json.dumps({"title": title, "type": type_, "description": description, "year": year, "day": day, "month": month, "section": section, "url_question": url, "part_question": part})
        session['form1data'] = form1data
        session['back'] = 0
        return redirect(url_for('submit2'))
    return render_template('submit.html', form=form)

@app.route('/submit2', methods=['POST', 'GET'])
@login_required
def submit2():
    session['back'] = session['back'] - 1
    print session['back']
    form = SubmitForm2()
    form1data = json.loads(session['form1data'])
    url_or_file = form1data['url_question']
    sections = int(form1data['section'])
    url_errors = []
    file_errors = []
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
                elif check[0] == 'file':
                    file_errors.append(int(check[1]))
            else:
                if url_or_file == 'Yes':
                    if 'url' in v:
                        #checks if url is pdf link
                        url = request.form[v]
                        try:
                            parsed_url = urlparse(url)
                            if not parsed_url.scheme:
                                url = "http://" + url
                            proxies = {"http": "http://cscisa.csc.nycnet:8080/array.dll?Get.Routing.Script", "https": "http://cscisa.csc.nycnet:8080/array.dll?Get.Routing.Script"}
                            print "requesting: " + url
                            r = requests.get(url_fix(url), proxies=proxies, timeout=1)
                            if r.status_code == 404:
                                status_errors.append(int(v.split('_')[1]))
                            if r.headers['content-type'] != 'application/pdf':
                                pdf_errors.append(int(v.split('_')[1]))
                        except Exception as e:
                            print e
                            match = re.search('[\w%+\/-].pdf', request.form[v])
                            if not match:
                                pdf_errors.append(int(v.split('_')[1]))
        for file_ in request.files:
            file_id = file_.split('_')[1]
            if request.files[file_].filename == '':
                file_errors.append(int(file_id))
            if not allowed_file(request.files[file_].filename):
                pdf_errors.append(int(file_id))
        if pdf_errors or section_errors or url_errors or status_errors or file_errors:
            pass
        else:
            if url_or_file == 'Yes':
                if sections == 1:
                    url = request.form.get('url_1')
                    parsed_url = urlparse(url)
                    if not parsed_url.scheme:
                        url = url_fix("http://" + url)
                    date_created = datetime.date(int(form1data['year']), int(form1data['month']), int(form1data['day']))
                    doc = Document(title=form1data['title'], type=form1data['type'], description=form1data['description'], dateCreated=date_created ,agency=session['agency'], doc_url=url)
                    db.session.add(doc)
                    db.session.commit()
                    did = db.session.query(func.max(Document.id)).scalar()
                    sub = Submit(did=did, uid=session['uid'])
                    db.session.add(sub)
                    db.session.commit()
                else:
                    common_id = db.session.query(func.max(Document.common_id)).scalar()
                    if not common_id:
                        common_id = 1
                    else:
                        common_id = common_id + 1
                    for doc in range(1, (sections + 1)):
                        url = 'url_' + str(doc)
                        url = request.form.get(url)
                        parsed_url = urlparse(url)
                        if not parsed_url.scheme:
                            url = url_fix("http://" + url)
                        section = 'section_' + str(doc)
                        section = request.form.get(section)
                        date_created = datetime.date(int(form1data['year']), int(form1data['month']), int(form1data['day']))
                        doc = Document(title=form1data['title'], type=form1data['type'], description=form1data['description'], dateCreated=date_created, agency=session['agency'], doc_url=url, common_id=common_id, section_id=doc)
                        db.session.add(doc)
                        db.session.commit()
                        did = db.session.query(func.max(Document.id)).scalar()
                        sub = Submit(did=did, uid=session['uid'])
                        sec = Section(did=did, section=section)
                        db.session.add(sec)
                        db.session.add(sub)
                        db.session.commit()
            elif url_or_file == 'No':
                if sections == 1:
                    file = request.files['file_1']
                    if file:
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                else:
                     print "testing"
            return redirect(url_for('home'))
    #print 'rform', request.form
    #print 'rfile', request.files
    return render_template('submit2.html', back=session['back'], form=form, submit2form=request.form, submit2files=request.files, sections=int(sections), url_or_file=url_or_file, url_errors=url_errors, section_errors=section_errors, status_errors=status_errors, pdf_errors=pdf_errors, file_errors=file_errors)

@app.route('/signup', methods=['POST', 'GET'])
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

@app.route('/submitted_docs')
@login_required
def submitted_docs():
    query = db.session.query(Document, Section).outerjoin(Section).join(Submit).join(User).filter(Submit.uid == session['uid']).filter(Document.status == "publishing").all()
    return render_template('submitted.html', results=query)

@app.route('/published_docs')
@login_required
def published_docs():
    query = db.session.query(Document, Section).outerjoin(Section).join(Submit).join(User).filter(Submit.uid == session['uid']).filter(or_(Document.status == "published", Document.status == "removed")).all()
    return render_template('published.html', results=query)

@app.route('/edit')

@app.route('/testdb')
def testdb():
    db.drop_all()
    db.create_all()
    return redirect('http://localhost:5000/auth/index')