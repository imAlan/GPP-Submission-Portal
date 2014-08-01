from flask import render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
from forms import SubmitForm1, SignUpForm, SubmitForm2, EditForm, RequestDeletionForm
from sqlalchemy import func, or_
from models import Document, User, db, Section, Submit
from flask.ext.login import login_required
from app import app
import json, datetime, requests, re, os
from werkzeug.urls import url_fix
from urlparse import urlparse
from decorators import admin_required
from pattern.web import URL

Bootstrap(app)

#app.config['SECRET_KEY'] = 'Key To Be Determine'
ALLOWED_EXTENSIONS = set(['pdf'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/home')
@login_required
def home():
    publishing_docs_null = db.session.query(func.count(Document.id)).outerjoin(Section).join(Submit).join(User).filter(Document.common_id == None).filter(Submit.uid == session['uid']).filter(Document.status == "publishing").first()[0]
    print publishing_docs_null
    publishing_doc_sec = db.session.query(func.count(Document.common_id)).outerjoin(Section).join(Submit).join(User).filter(Document.common_id != None).filter(Submit.uid == session['uid']).filter(Document.status == "publishing").group_by(Document.common_id).first()[0]
    print publishing_doc_sec
    publishing_docs = publishing_doc_sec + publishing_docs_null
    print publishing_docs
    if "form1data"  not in session.keys():
        session['form1data'] = None
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
    if not session['form1data']:
        return redirect(url_for('submit'))
    session['back'] = session['back'] - 1
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
                        except:
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
                    download_url = URL(url)
                    date_created = datetime.date(int(form1data['year']), int(form1data['month']), int(form1data['day']))
                    doc = Document(title=form1data['title'], type=form1data['type'], description=form1data['description'], dateCreated=date_created ,agency=session['agency'], doc_url=url)
                    db.session.add(doc)
                    db.session.commit()
                    did = db.session.query(func.max(Document.id)).scalar()
                    doc = Document.query.get(did)
                    filename = str(did) + '_' + form1data['title']
                    doc.filename = filename
                    try:
                        f = open(os.path.join(app.config['UPLOAD_FOLDER'], filename+".pdf"), 'wb')
                        if urlparse(url).scheme == "https://":
                            f.write(download_url.download(cached=False, proxy=("http://cscisa.csc.nycnet:8080/array.dll?Get.Routing.Script", 'https')))
                        else:
                            f.write(download_url.download(cached=False, proxy=("http://cscisa.csc.nycnet:8080/array.dll?Get.Routing.Script", 'http')))
                        f.close()
                        doc.hardcopy = "yes"
                    except:
                        pass
                    sub = Submit(did=did, uid=session['uid'])
                    db.session.add(sub)
                    db.session.commit()
                elif sections > 1:
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
                        download_url = URL(url)
                        sectionid = 'section_' + str(doc)
                        section = request.form.get(sectionid)
                        date_created = datetime.date(int(form1data['year']), int(form1data['month']), int(form1data['day']))
                        doc = Document(title=form1data['title'], type=form1data['type'], description=form1data['description'], dateCreated=date_created, agency=session['agency'], doc_url=url, common_id=common_id, section_id=doc)
                        db.session.add(doc)
                        db.session.commit()
                        did = db.session.query(func.max(Document.id)).scalar()
                        doc = Document.query.get(did)
                        filename = str(did) + '_' + form1data['title']
                        doc.filename = filename
                        try:
                            f = open(os.path.join(app.config['UPLOAD_FOLDER'], filename+".pdf"), 'wb')
                            if urlparse(url).scheme == "https://":
                                f.write(download_url.download(cached=False, proxy=("http://cscisa.csc.nycnet:8080/array.dll?Get.Routing.Script", 'https')))
                            else:
                                f.write(download_url.download(cached=False, proxy=("http://cscisa.csc.nycnet:8080/array.dll?Get.Routing.Script", 'http')))
                            f.close()
                        except:
                            doc.hardcopy = "yes"
                        sub = Submit(did=did, uid=session['uid'])
                        sec = Section(did=did, section=section)
                        db.session.add(sec)
                        db.session.add(sub)
                        db.session.commit()
            elif url_or_file == 'No':
                if sections == 1:
                    file = request.files['file_1']
                    if file:
                        date_created = datetime.date(int(form1data['year']), int(form1data['month']), int(form1data['day']))
                        doc = Document(title=form1data['title'], type=form1data['type'], description=form1data['description'], dateCreated=date_created ,agency=session['agency'])
                        db.session.add(doc)
                        db.session.commit()
                        did = db.session.query(func.max(Document.id)).scalar()
                        doc = Document.query.get(did)
                        filename = str(did) + '_' + doc.title + ".pdf"
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        doc.filename = filename
                        sub = Submit(did=did, uid=session['uid'])
                        db.session.add(sub)
                        db.session.commit()
                elif sections > 1:
                     for doc in range(1, (sections + 1)):
                        fileid = "file_" + str(doc)
                        file = request.files[fileid]
                        if file:
                            date_created = datetime.date(int(form1data['year']), int(form1data['month']), int(form1data['day']))
                            doc = Document(title=form1data['title'], type=form1data['type'], description=form1data['description'], dateCreated=date_created ,agency=session['agency'])
                            sectionid = 'section_' + str(doc)
                            section = request.form.get(sectionid)
                            db.session.add(doc)
                            db.session.commit()
                            did = db.session.query(func.max(Document.id)).scalar()
                            doc = Document.query.get(did)
                            filename = str(did) + '_' + doc.title + ".pdf"
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            doc.filename = filename
                            sub = Submit(did=did, uid=session['uid'])
                            sec = Section(did=did, section=section)
                            db.session.add(sub)
                            db.session.add(sec)
                            db.session.commit()
            return redirect(url_for('home'))
    return render_template('submit2.html', back=session['back'], form=form, submit2form=request.form, submit2files=request.files, sections=int(sections), url_or_file=url_or_file, url_errors=url_errors, section_errors=section_errors, status_errors=status_errors, pdf_errors=pdf_errors, file_errors=file_errors)

@app.route('/signup', methods=['POST', 'GET'])
@admin_required
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
        role = form.role.data
        user = User(username=username, password=password, first=first, last=last, agency=agency, phone=phone,email=email, role=role)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('addUser.html', form=form)

@app.route('/submitted_docs')
@login_required
def submitted_docs():
    docs_sec = db.session.query(Document, func.count(Document.common_id)).outerjoin(Section).join(Submit).join(User).filter(Document.common_id != None).filter(Submit.uid == session['uid']).filter(Document.status == "publishing").group_by(Document.common_id).all()
    docs_null = db.session.query(Document, func.count(Document.id)).outerjoin(Section).join(Submit).join(User).filter(Document.common_id == None).filter(Submit.uid == session['uid']).filter(Document.status == "publishing").group_by(Document.id).all()
    docs = docs_sec + docs_null
    return render_template('submitted.html', results=docs)

@app.route('/published_docs', methods=['POST', 'GET'])
@login_required
def published_docs():
    form = RequestDeletionForm(request.form)
    if form.validate_on_submit():
        doc_id = request.form['doc_id']
        message = form.message.data
        document = db.session.query(Document).join(Submit).join(User).filter(Submit.uid == session['uid']).filter(Document.status == "published").filter(Document.id == doc_id).first()
        results = db.session.query(Document).join(Submit).join(User).filter(Submit.uid == session['uid']).filter(Document.status == "published").filter(Document.common_id == document.common_id).all()
        if document:
            if not results:
                document.reason = message
                document.request_deletion = 'yes'
            else:
                for result in results:
                    result.reason = message
                    result.request_deletion = 'yes'
        db.session.commit()
        #redirect to self to clear form
        return redirect(url_for('published_docs'))
    docs_sec = db.session.query(Document, func.count(Document.common_id), User).outerjoin(Section).join(Submit).join(User).filter(Document.common_id != None).filter(or_(Document.status == "published", Document.status == "removed")).filter(Document.agency == session['agency']).group_by(Document.common_id).all()
    docs_null = db.session.query(Document, func.count(Document.id), User).outerjoin(Section).join(Submit).join(User).filter(Document.common_id == None).filter(or_(Document.status == "published", Document.status == "removed")).filter(Document.agency == session['agency']).group_by(Document.id).all()
    docs = docs_sec + docs_null
    return render_template('published.html', results=docs, form=form)

@app.route('/edit/', methods=['GET', 'POST'])
@login_required
def edit():
    if request.args.get('id').isdigit():
        form = EditForm(request.form)
        doc_id = request.args.get('id').encode('ascii','ignore')
        document = db.session.query(Document, Submit).join(Submit).join(User).filter(Submit.uid == session['uid']).filter(Document.status == "publishing").filter(Document.id == doc_id).first()
        results = db.session.query(Document, Section).outerjoin(Section).join(Submit).join(User).filter(Submit.uid == session['uid']).filter(Document.status == "publishing").filter(Document.common_id == document[0].common_id).all()
        if request.method == 'GET':
            year = str(results[0][0].dateCreated.year)
            month = str(results[0][0].dateCreated.month)
            day = str(results[0][0].dateCreated.day)
            form = EditForm(request.form, type_=results[0][0].type, year=year, month=month, day=day, description=results[0][0].description, title=results[0][0].title)
        elif form.validate_on_submit():
            doc = Document.query.get(doc_id)
            doc.title = form.title.data
            doc.description = form.description.data
            doc.dateCreated = datetime.date(int(form.year.data), int(form.month.data), int(form.day.data))
            doc.type = form.type_.data
            db.session.commit()
            return redirect(url_for('submitted_docs'))
    return render_template('edit.html', form=form, results=results)


@app.route('/delete/')
@login_required
def delete():
    if request.args.get('id').isdigit():
        doc_id = request.args.get('id').encode('ascii','ignore')
        document = db.session.query(Document, Submit).join(Submit).join(User).filter(Submit.uid == session['uid']).filter(Document.status == "publishing").filter(Document.id == doc_id).first()
        results = db.session.query(Document, Section, Submit).join(Section).join(Submit).join(User).filter(Submit.uid == session['uid']).filter(Document.status == "publishing").filter(Document.common_id == document[0].common_id).all()
        if document:
            if not results:
                db.session.delete(document[1])
                db.session.delete(document[0])
            else:
                for result in results:
                    db.session.delete(result[1])
                    db.session.delete(result[0])
                    db.session.delete(result[2])
            db.session.commit()
    return redirect(url_for('submitted_docs'))

@app.route('/view/')
@login_required
def view():
    if request.args.get('id').isdigit():
        doc_id = request.args.get('id').encode('ascii', 'ignore')
        document = db.session.query(Document, Submit).join(Submit).join(User).filter(Document.status == "published").filter(Document.agency == session['agency']).filter(Document.id == doc_id).first()
        results = db.session.query(Document, Section, User).outerjoin(Section).join(Submit).join(User).filter(Document.agency == session['agency']).filter(Document.status == "published").filter(Document.common_id == document[0].common_id).all()
        return render_template('view.html', results=results)

@app.route('/testdb')
def testdb():
    db.drop_all()
    db.create_all()
    return redirect('http://localhost:5000')


@app.errorhandler(403)
def permission_denied(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404