from app import app
from flask import render_template, request, redirect, url_for, session, abort
from forms import SubmitForm1, SignUpForm, SubmitForm2, EditForm, RequestRemovalForm, PublishForm, RemoveForm, EditUserForm, EditProfileForm, ChangePasswordForm, MessageForm
from sqlalchemy import func, or_, and_, desc
from models import Document, User, db, Section, Submit
from flask.ext.login import login_required, current_user
import json, datetime, requests, re, os
from werkzeug.urls import url_fix
from urlparse import urlparse
from decorators import admin_required, agency_or_admin_required
from pattern.web import URL
from werkzeug.security import generate_password_hash
from flask.ext.mail import Message

#Extensions that are allowed to be submitted
ALLOWED_EXTENSIONS = set(['pdf'])

#Checks if filesname has ext
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/home')
@login_required
def home():
    #Queries Publishing Documents with no sections for current user
    publishing_docs_null = db.session.query(func.count(Document.id)).outerjoin(Section).join(Submit).join(User).filter(Document.common_id == None).filter(or_(Submit.uid == current_user.id, current_user.role == 'Admin', and_(current_user.role == 'Agency_Admin', Document.agency == current_user.agency))).filter(Document.status == "publishing").first()[0]
    #Queries Published Documents with sections for current user
    publishing_doc_sec = db.session.query(func.count(Document.common_id.distinct())).outerjoin(Section).join(Submit).join(User).filter(Document.common_id != None).filter(or_(Submit.uid == current_user.id, current_user.role == 'Admin', and_(current_user.role == 'Agency_Admin', Document.agency == current_user.agency))).filter(Document.status == "publishing").first()[0]
    #All Publishing Document
    publishing_docs = publishing_doc_sec + publishing_docs_null
    #Queries published Documents with no sections for current user
    published_docs_null = db.session.query(func.count(Document.id)).outerjoin(Section).join(Submit).join(User).filter(Document.common_id == None).filter(or_(current_user.role == 'Admin', Document.agency == current_user.agency)).filter(Document.status == "published").first()[0]
    #Queries published Documents with section for current user
    published_doc_sec = db.session.query(func.count(Document.common_id.distinct())).outerjoin(Section).join(Submit).join(User).filter(Document.common_id != None).filter(or_(current_user.role == 'Admin', Document.agency == current_user.agency)).filter(Document.status == "published").first()[0]
    #All Published Documents
    published_docs = published_doc_sec + published_docs_null
    #Queries all Document requesting removal with no section for current user if admin
    remove_docs_null = db.session.query(func.count(Document.id)).outerjoin(Section).join(Submit).join(User).filter(Document.common_id == None).filter(or_(current_user.role == 'Admin', Document.agency == current_user.agency)).filter(Document.request_deletion == 'yes').filter(Document.status == 'published').first()[0]
    #Queries all Document requesting removal with sections for current user if admin
    remove_doc_sec = db.session.query(func.count(Document.common_id.distinct())).outerjoin(Section).join(Submit).join(User).filter(Document.common_id != None).filter(or_(current_user.role == 'Admin', Document.agency == current_user.agency)).filter(Document.request_deletion == 'yes').filter(Document.status == 'published').first()[0]
    #All Document requesting removal
    remove_docs = remove_doc_sec + remove_docs_null
    #Resets submit form 1 data 
    session['form1data'] = None
    return render_template('home.html', publishing_docs=publishing_docs, published_docs=published_docs, remove_docs=remove_docs ,role=current_user.role)

@app.route('/submit1', methods=['POST', 'GET'])
@login_required
def submit():
    form = SubmitForm1(request.form)
    #Validataes form and stores form data in session
    if form.validate_on_submit():
        title = form.title.data
        type_ = form.type_.data
        category = form.category.data
        description = form.description.data
        year = form.year.data
        month = form.month.data
        day = form.month.data
        part = form.part_question.data
        url = form.url_question.data
        #Checks if user clicked multiple sections
        if part == 'No':
            section = 1
        else:
            section = form.num.data
        form1data = json.dumps({"title": title, "type": type_, "description": description, "year": year, "day": day, "month": month, "section": section, "url_question": url, "part_question": part, "category": category})
        #Stores json object
        session['form1data'] = form1data
        #Set session variable back to 0; used for back button in second form
        session['back'] = 0
        return redirect(url_for('submit2'))
    return render_template('submit.html', form=form)

@app.route('/submit2', methods=['POST', 'GET'])
@login_required
def submit2():
    #Checks if form1data has been submitted before accessing this page
    if not session['form1data']:
        return redirect(url_for('submit'))
    #Session variable back is decremented
    session['back'] = session['back'] - 1
    form = SubmitForm2()
    form1data = json.loads(session['form1data'])
    url_or_file = form1data['url_question']
    #Get number of sections
    sections = int(form1data['section'])
    #Error variables
    url_errors = []
    file_errors = []
    section_errors = []
    pdf_errors = []
    status_errors = []
    if form.validate_on_submit():
        #Loops through inputs of form
        for input in request.form:
            #checks if inputs are empty and adds ids to the corresponding error list
            if request.form[input] == '':
                check = input.split('_')
                if check[0] == 'url':
                    url_errors.append(int(check[1]))
                elif check[0] == 'section':
                    section_errors.append(int(check[1]))
                elif check[0] == 'file':
                    file_errors.append(int(check[1]))
            else:
                if url_or_file == 'Yes':
                    if 'url' in input:
                        #checks if url is pdf link
                        url = request.form[input]
                        try:
                            parsed_url = urlparse(url)
                            #checks if the user input has a schema
                            if not parsed_url.scheme:
                                url = "http://" + url
                            proxies = {"http": "http://cscisa.csc.nycnet:8080/array.dll?Get.Routing.Script", "https": "http://cscisa.csc.nycnet:8080/array.dll?Get.Routing.Script"}
                            print "requesting: " + url
                            r = requests.get(url_fix(url), proxies=proxies, timeout=1)
                            if r.status_code == 404:
                                status_errors.append(int(input.split('_')[1]))
                            if r.headers['content-type'] != 'application/pdf':
                                pdf_errors.append(int(input.split('_')[1]))
                        #if requesting the website fails; do regular expression checking
                        except:
                            match = re.search('[\w%+\/-].pdf', request.form[input])
                            if not match:
                                pdf_errors.append(int(input.split('_')[1]))
        #loops through the files inputted
        for file_ in request.files:
            file_id = file_.split('_')[1]
            #no files inputted add to files errors list
            if request.files[file_].filename == '':
                file_errors.append(int(file_id))
            #check is the files one of the allowed files ext
            if not allowed_file(request.files[file_].filename):
                pdf_errors.append(int(file_id))
        #if errors respond with errors
        if pdf_errors or section_errors or url_errors or status_errors or file_errors:
            pass
        else:
            #Urls processing
            if url_or_file == 'Yes':
                if sections == 1:
                    url = request.form.get('url_1')
                    parsed_url = urlparse(url)
                    #check schema
                    if not parsed_url.scheme:
                        url = url_fix("http://" + url)
                    download_url = URL(url)
                    date_created = datetime.date(int(form1data['year']), int(form1data['month']), int(form1data['day']))
                    doc = Document(title=form1data['title'], type=form1data['type'], description=form1data['description'], dateCreated=date_created ,agency=session['agency'], category=form1data['category'], doc_url=url)
                    db.session.add(doc)
                    #add document meta data to datebase
                    db.session.commit()
                    #get max common id
                    did = db.session.query(func.max(Document.id)).scalar()
                    doc = Document.query.get(did)
                    filename = str(did) + '_' + form1data['title']
                    doc.filename = filename
                    #download file into upload folder
                    try:
                        f = open(os.path.join(app.config['UPLOAD_FOLDER'], filename+".pdf"), 'wb')
                        if urlparse(url).scheme == "https://":
                            f.write(download_url.download(cached=False, proxy=("http://cscisa.csc.nycnet:8080/array.dll?Get.Routing.Script", 'https')))
                        else:
                            f.write(download_url.download(cached=False, proxy=("http://cscisa.csc.nycnet:8080/array.dll?Get.Routing.Script", 'http')))
                        f.close()
                        #hardcopy set to yes if downloaded
                        doc.hardcopy = "yes"
                        doc.path = os.path.join(app.config['DOC_PATH'], filename)
                    #NOTE: Script must be written for documents that have hardcopy set to no; to download file
                    except:
                        pass
                    sub = Submit(did=did, uid=session['uid'])
                    db.session.add(sub)
                    db.session.commit()
                    #if more that one sections do samething above for each section
                elif sections > 1:
                    #gets the common id to be inserted by querying the max common id + 1
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
                        doc = Document(title=form1data['title'], type=form1data['type'], description=form1data['description'], dateCreated=date_created, agency=session['agency'], category=form1data['category'], doc_url=url, common_id=common_id, section_id=doc)
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
                            doc.path = os.path.join(app.config['DOC_PATH'], filename)
                        except:
                            pass
                        sub = Submit(did=did, uid=session['uid'])
                        sec = Section(did=did, section=section)
                        db.session.add(sec)
                        db.session.add(sub)
                        db.session.commit()
            #if the user clicked files
            elif url_or_file == 'No':
                if sections == 1:
                    file = request.files['file_1']
                    if file:
                        date_created = datetime.date(int(form1data['year']), int(form1data['month']), int(form1data['day']))
                        doc = Document(title=form1data['title'], type=form1data['type'], description=form1data['description'], dateCreated=date_created ,agency=session['agency'], category=form1data['category'])
                        db.session.add(doc)
                        db.session.commit()
                        did = db.session.query(func.max(Document.id)).scalar()
                        doc = Document.query.get(did)
                        filename = str(did) + '_' + doc.title + ".pdf"
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        doc.path = os.path.join(app.config['DOC_PATH'], filename)
                        doc.filename = filename
                        doc.hardcopy = 'yes'
                        sub = Submit(did=did, uid=session['uid'])
                        db.session.add(sub)
                        db.session.commit()
                elif sections > 1:
                     for doc in range(1, (sections + 1)):
                        fileid = "file_" + str(doc)
                        file = request.files[fileid]
                        if file:
                            date_created = datetime.date(int(form1data['year']), int(form1data['month']), int(form1data['day']))
                            doc = Document(title=form1data['title'], type=form1data['type'], description=form1data['description'], dateCreated=date_created, agency=session['agency'], category=form1data['category'])
                            sectionid = 'section_' + str(doc)
                            section = request.form.get(sectionid)
                            db.session.add(doc)
                            db.session.commit()
                            did = db.session.query(func.max(Document.id)).scalar()
                            doc = Document.query.get(did)
                            filename = str(did) + '_' + doc.title + ".pdf"
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            doc.filename = filename
                            doc.hardcopy = 'yes'
                            doc.path = os.path.join(app.config['DOC_PATH'], filename)
                            sub = Submit(did=did, uid=session['uid'])
                            sec = Section(did=did, section=section)
                            db.session.add(sub)
                            db.session.add(sec)
                            db.session.commit()
            #set session variable confirm to be true so that comfirmation page is allowed through
            session['confirm'] = True
            return redirect(url_for('confirmation'))
    return render_template('submit2.html', back=session['back'], form=form, submit2form=request.form, submit2files=request.files, sections=int(sections), url_or_file=url_or_file, url_errors=url_errors, section_errors=section_errors, status_errors=status_errors, pdf_errors=pdf_errors, file_errors=file_errors)


@app.route('/submit3')
@login_required
def confirmation():
    if 'confirm' in session.keys() and session['confirm']:
        session['confirm'] = False
        return render_template('submit3.html')
    else:
        abort(404)

#User sign up page
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

@app.route('/submitted_docs', methods=['POST', 'GET'])
@login_required
def submitted_docs():
    form = PublishForm(request.form)
    removeForm = RemoveForm(request.form)
    publish_errors = False
    #If user clicked publish
    if form.validate_on_submit() and request.form['submit'] == 'Publish' and current_user.role == 'Admin':
        for input in request.form:
        #split name to get document id
            input = input.split('_')
            if input[0] == 'publish':
                doc_id = input[1]
                #get document form database
                document = db.session.query(Document).join(Submit).join(User).filter(or_(Submit.uid == session['uid'], current_user.role == 'Admin', and_(current_user.role == 'Agency_Admin', Document.agency == current_user.agency))).filter(Document.status == "publishing").filter(Document.id == doc_id).first()
                if not document.category:
                    publish_errors = True
                    break
                if document:
                    #check if document had multiple parts
                    results = db.session.query(Document).join(Submit).join(User).filter(or_(Submit.uid == session['uid'], current_user.role == 'Admin', and_(current_user.role == 'Agency_Admin', Document.agency == current_user.agency))).filter(Document.status == "publishing").filter(Document.common_id != None).filter(document.common_id == document.common_id).all()
                    #change the status od documents to published
                    if not results:
                        document.status = 'published'
                        document.approved = 'yes'
                    else:
                        for result in results:
                            result.status = 'published'
                            result.approved = 'yes'
                    db.session.commit()
        if not publish_errors:
            return redirect(url_for('submitted_docs'))
    #if user clicked removed
    if form.validate_on_submit() and request.form['submit'] == 'Remove':
        for input in request.form:
            input = input.split('_')
            if input[0] == 'remove':
                doc_id = input[1]
                #get document
                document = db.session.query(Document).join(Submit).join(User).filter(or_(Submit.uid == session['uid'], current_user.role == 'Admin', and_(current_user.role == 'Agency_Admin', Document.agency == current_user.agency))).filter(Document.status == "publishing").filter(Document.id == doc_id).first()
                if document:
                    #check if doucment has multiple parts
                    results = db.session.query(Document).join(Submit).join(User).filter(or_(Submit.uid == session['uid'], current_user.role == 'Admin', and_(current_user.role == 'Agency_Admin', Document.agency == current_user.agency))).filter(Document.status == "publishing").filter(Document.common_id != None).filter(document.common_id == Document.common_id).all()
                    #change status to removed
                    if not results:
                        document.status = 'removed'
                    else:
                        for result in results:
                            result.status = 'removed'
                    db.session.commit()
    #query all documents that have status submitted
    docs_sec = db.session.query(Document, func.count(Document.common_id), User).outerjoin(Section).join(Submit).join(User).filter(Document.common_id != None).filter(or_(Submit.uid == session['uid'], current_user.role == 'Admin' ,and_(Document.agency == current_user.agency, current_user.role == 'Agency_Admin'))).filter(Document.status == "publishing").group_by(Document.common_id).all()
    docs_null = db.session.query(Document, func.count(Document.id), User).outerjoin(Section).join(Submit).join(User).filter(Document.common_id == None).filter(or_(Submit.uid == session['uid'], current_user.role == 'Admin' ,and_(Document.agency == current_user.agency, current_user.role == 'Agency_Admin'))).filter(Document.status == "publishing").group_by(Document.id).all()
    docs = docs_sec + docs_null
    return render_template('submitted.html', results=docs, form=form, removeForm=removeForm, publish_errors=publish_errors, current_user=current_user)

@app.route('/published_docs', methods=['POST', 'GET'])
@login_required
def published_docs():
    form = RequestRemovalForm(request.form)
    #if user clicked request document to be removed
    if form.validate_on_submit():
        for input in request.form:
            input = input.split('_')
            if input[0] == 'requestRemoval':
                doc_id = input[1]
                document = db.session.query(Document).join(Submit).join(User).filter(or_(Submit.uid == session['uid'], current_user.role == 'Admin', and_(current_user.role == 'Agency_Admin', Document.agency == current_user.agency))).filter(Document.status == "published").filter(Document.id == doc_id).first()
                if document:
                    results = db.session.query(Document).join(Submit).join(User).filter(or_(Submit.uid == session['uid'], current_user.role == 'Admin', and_(current_user.role == 'Agency_Admin', Document.agency == current_user.agency))).filter(Document.status == "published").filter(Document.common_id != None).filter(document.common_id == Document.common_id).all()
                    if not results:
                        document.reason = form.message.data
                        document.request_deletion = 'yes'
                    else:
                        for result in results:
                            result.reason = form.message.data
                            result.request_deletion = 'yes'
                    db.session.commit()
        return redirect(url_for('published_docs'))
    #if admin query all published documents
    if current_user.role == 'Admin':
        docs_sec = db.session.query(Document, func.count(Document.common_id), User).outerjoin(Section).join(Submit).join(User).filter(Document.common_id != None).filter(or_(Document.status == "published", Document.status == "removed")).group_by(Document.common_id).all()
        docs_null = db.session.query(Document, func.count(Document.id), User).outerjoin(Section).join(Submit).join(User).filter(Document.common_id == None).filter(or_(Document.status == "published", Document.status == "removed")).group_by(Document.id).all()
    #Query all documents that belong to the user's agency
    else:
        docs_sec = db.session.query(Document, func.count(Document.common_id), User).outerjoin(Section).join(Submit).join(User).filter(Document.common_id != None).filter(or_(Document.status == "published", Document.status == "removed")).filter(Document.agency == current_user.agency).group_by(Document.common_id).all()
        docs_null = db.session.query(Document, func.count(Document.id), User).outerjoin(Section).join(Submit).join(User).filter(Document.common_id == None).filter(or_(Document.status == "published", Document.status == "removed")).filter(Document.agency == current_user.agency).group_by(Document.id).all()
    docs = docs_sec + docs_null
    return render_template('published.html', results=docs, form=form, cform=request.form)

@app.route('/remove_docs', methods=['GET', 'POST'])
@login_required
@admin_required
def remove_docs():
    form = RemoveForm(request.form)
    #if admin approves removal of documents
    if form.validate_on_submit():
        for input in request.form:
            input = input.split('_')
            if input[0] == 'remove':
                doc_id = input[1]
                #get documents along with sections
                document = db.session.query(Document).filter(current_user.role == 'Admin').filter(and_(Document.status == "published", Document.request_deletion == 'yes')).filter(Document.id == doc_id).first()
                results = db.session.query(Document).filter(current_user.role == 'Admin').filter(and_(Document.status == "published", Document.request_deletion == 'yes')).filter(document.common_id != None).filter(Document.common_id == document.common_id).all()
                #change the status of the document to removed
                if document:
                    if not results:
                        document.status = 'removed'
                        document.dateRemoved = datetime.date.today()
                    else:
                        for document in results:
                            document.status = 'removed'
                            document.dateRemoved = datetime.date.today()
                    db.session.commit()
        return redirect(url_for('remove_docs'))
    #query all documents that have been requested to removed
    doc_sec = db.session.query(Document, User).join(Submit).join(User).filter(Document.common_id != None).filter(Document.request_deletion == 'yes').filter(Document.status == 'published').group_by(Document.common_id).all()
    doc_null = db.session.query(Document, User).join(Submit).join(User).filter(Document.common_id == None).filter(Document.request_deletion == 'yes').filter(Document.status == 'published').all()
    docs = doc_sec + doc_null
    return render_template('remove_docs.html', docs=docs, form=form)


@app.route('/stats')
@login_required
def stats():
    documents = db.session.query(Document).join(Submit).join(User).filter(or_(User.id == current_user.id, current_user.role == 'Admin')).order_by(desc(Document.num_access)).all()[:5]
    doc_name = [doc.title[:10].strip().encode('ascii','ignore') for doc in documents]
    doc_views = [int(item.num_access) for item in documents]
    users = db.session.query(User, func.count(Submit.uid)).join(Submit).group_by(Submit.uid).all()[:5]
    user_name = [user.username.strip().encode('ascii','ignore') for user, sub in users]
    user_sub = [int(sub) for user, sub in users]
    return render_template('stats.html', doc_views=doc_views, doc_name=doc_name, user_name=user_name, user_sub=user_sub, current_user=current_user)


@app.route('/edit_user/', methods=['GET', 'POST'])
@login_required
@agency_or_admin_required
def edit_user():
    #check if the id is a digit
    if request.args.get('id').isdigit():
        form = EditUserForm(request.form)
        #convert to digit
        user_id = request.args.get('id').encode('ascii', 'ignore')
        #get user and the number of submitted documents
        result = db.session.query(User, func.count(Submit.uid)).outerjoin(Submit).filter(User.id == user_id).group_by(Submit.uid).first()
        if result:
            user = result[0]
            docs = result[1]
            if request.method == 'GET':
                form = EditUserForm(request.form, first=user.first, last=user.last, phone=user.phone, email=user.email)
            #update db on form submit
            elif form.validate_on_submit():
                user.first = form.first.data
                user.last = form.last.data
                user.phone = form.phone.data
                user.email = form.email.data
                db.session.commit()
                return redirect(url_for('users'))
            return render_template('edit_user.html', form=form, user=user, docs=docs, current_user=current_user)
    abort(404)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = User.query.get(current_user.id)
    form = EditProfileForm(request.form, phone=user.phone, email=user.email)
    passform = ChangePasswordForm(request.form)
    if request.method == 'POST':
        #if the user clicked button to update profile
        if request.form['submit'] == 'Update' and form.validate_on_submit():
            phone = form.phone.data
            email = form.email.data
            user.phone = phone
            user.email = email 
            db.session.commit()
            return redirect('home')
        #if user clicked change password
        if request.form['submit'] == 'Change Password' and passform.validate_on_submit():
            #generate hash
            newpass = generate_password_hash(passform.password.data)
            user.password_hash = newpass
            db.session.commit()
            return redirect('edit_profile')
    return render_template('edit_profile.html', form=form, passform=passform ,user=user)

@app.route('/edit_doc/', methods=['GET', 'POST'])
@login_required
def edit_doc():
    #check if id is digit
    if request.args.get('id').isdigit():
        form = EditForm(request.form)
        doc_id = request.args.get('id').encode('ascii','ignore')
        #get document
        document = db.session.query(Document, Submit).join(Submit).join(User).filter(or_(Submit.uid == session['uid'], current_user.role == 'Admin', and_(current_user.role == 'Agency_Admin', Document.agency == current_user.agency))).filter(Document.status == "publishing").filter(Document.id == doc_id).all()
        #check if it has multiple sections
        if document[0][0].common_id != None:
            results = db.session.query(Document, Section).outerjoin(Section).join(Submit).filter(Document.status == "publishing").filter(Document.common_id != None).filter(Document.common_id == document[0][0].common_id).all()
        else:
            results = document
        if request.method == 'GET':
            year = str(document[0][0].dateCreated.year)
            month = str(document[0][0].dateCreated.month)
            day = str(document[0][0].dateCreated.day)
            form = EditForm(request.form, type_=document[0][0].type, year=year, month=month, day=day, description=document[0][0].description, title=document[0][0].title, category=document[0][0].category)
        #update document
        elif form.validate_on_submit():
            doc = Document.query.get(doc_id)
            doc.title = form.title.data
            doc.description = form.description.data
            doc.dateCreated = datetime.date(int(form.year.data), int(form.month.data), int(form.day.data))
            doc.type = form.type_.data
            form.category.data = form.category.data.encode('ascii', 'ignore')
            if form.category.data != 'None':
                doc.category = form.category.data
            db.session.commit()
            return redirect(url_for('submitted_docs'))
    return render_template('edit_doc.html', form=form, results=results, current_user=current_user)

@app.route('/delete/')
@login_required
def delete():
    if request.args.get('id').isdigit():
        doc_id = request.args.get('id').encode('ascii','ignore')
        #get document
        document = db.session.query(Document, Submit).join(Submit).join(User).filter(Submit.uid == session['uid']).filter(Document.status == "publishing").filter(Document.id == doc_id).first()
        results = db.session.query(Document, Section, Submit).join(Section).join(Submit).join(User).filter(Submit.uid == session['uid']).filter(Document.status == "publishing").filter(document.common_id != None).filter(Document.common_id == document[0].common_id).all()
        #if document exist delete the document from database
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
        document = db.session.query(Document, Submit, User).join(Submit).join(User).filter(Document.status == "published").filter(or_(Document.agency == current_user.agency, current_user.role == 'Admin')).filter(Document.id == doc_id).all()
        if document:
            #if document has multiple parts; get all parts
            if document[0][0].common_id:
                results = db.session.query(Document, Section, User).outerjoin(Section).join(Submit).join(User).filter(Document.agency == current_user.agency).filter(Document.status == "published").filter(Document.common_id == document[0][0].common_id).all()
            else:
                results = document
            return render_template('view.html', results=results)
        abort(404)
    return redirect(url_for('published_docs'))

@app.route('/users', methods=['GET', 'POST'])
@login_required
@agency_or_admin_required
def users():
    form = RemoveForm(request.form)
    messageForm = MessageForm(request.form)
    #display all users if Admin
    if current_user.role == 'Admin':
        allUsers = db.session.query(User, func.count(Submit.did)).outerjoin(Submit).filter(User.remove != 1).group_by(User.id).all()
    #display all agency users uf Agency Admin
    elif current_user.role == 'Agency_Admin':
        allUsers = db.session.query(User, func.count(Submit.did)).outerjoin(Submit).filter(User.remove != 1).filter(current_user.agency == User.agency).group_by(User.id).all()
    #if clicked remove user
    if form.validate_on_submit():
        for input in request.form:
            input = input.split('_')
            if input[0] == 'removeUser':
                user_id = input[1]
                if user_id != current_user.id:
                    user = User.query.get(user_id)
                    #set remove to 1 and user will be no longer valid
                    user.remove = 1
                    db.session.commit()
    return render_template('users.html', users=allUsers, form=form, current_user=current_user)

@app.route('/message', methods=['GET', 'POST'])
@login_required
@admin_required
def message():
    form = MessageForm(request.form)
    if form.validate_on_submit():
        recipients = form.recipients.data
        q_emails = db.session.query(User.email).filter(User.agency == recipients).all()
        for email in q_emails:
            print email[0]
        subject = form.subject.data
        message = form.message.data
        #msg = Message(subject=subject, body=message, sender=os.environ.get('DEFAULT_MAIL_SENDER'), recipients=recipients)
        #mail.send(msg)
    return render_template('message.html', form=form)


@app.route('/testdb')
def testdb():
    db.drop_all()
    db.create_all()
    return redirect(url_for('home'))

@app.errorhandler(403)
def permission_denied(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
