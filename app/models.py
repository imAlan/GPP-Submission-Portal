from flask.ext.sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from flask import session
from . import login_manager
db = SQLAlchemy()

class Document(db.Model):
    __tablename__ = 'Document'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    datePublished = db.Column(db.Date)
    dateSubmitted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    dateCreated = db.Column(db.Date)
    filename = db.Column(db.String(255), default=None)
    common_id = db.Column(db.Integer, default=None)
    section_id = db.Column(db.Integer, default=None)
    status = db.Column(db.Enum('published', 'removed', 'publishing', 'not_approved'), nullable=False, default='publishing')
    approved = db.Column(db.Enum('yes', 'no'), default=None)
    reason = db.Column(db.String(255), default=None)
    hardcopy = db.Column(db.Enum('yes', 'no'), default=None)
    doc_url = db.Column(db.String(255), default=None)
    num_access = db.Column(db.Integer, default=0)
    agency = db.Column(db.Enum( 'Aging',
                            'Buildings',
                            'Campaign Finance',
                            'Children''s Services',
                            'City Council',
                            'City Clerk',
                            'City Planning',
                            'Citywide Admin Svcs',
                            'Civilian Complaint',
                            'Comm - Police Corr',
                            'Community Assistance',
                            'Comptroller',
                            'Conflicts of Interest',
                            'Consumer Affairs',
                            'Contracts',
                            'Correction',
                            'Criminal Justice Coordinator',
                            'Cultural Affairs',
                            'DOI - Investigation',
                            'Design/Construction',
                            'Disabilities',
                            'District Atty, NY County',
                            'Districting Commission',
                            'Domestic Violence',
                            'Economic Development',
                            'Education, Dept. of',
                            'Elections, Board of',
                            'Emergency Mgmt.',
                            'Employment',
                            'Empowerment Zone',
                            'Environmental - DEP',
                            'Environmental - OEC',
                            'Environmental - ECB',
                            'Equal Employment',
                            'Film/Theatre',
                            'Finance',
                            'Fire',
                            'FISA',
                            'Health and Mental Hyg.',
                            'HealthStat',
                            'Homeless Services',
                            'Hospitals - HHC',
                            'Housing - HPD',
                            'Human Rights',
                            'Human Rsrcs - HRA',
                            'Immigrant Affairs',
                            'Independent Budget',
                            'Info. Tech. and Telecom.',
                            'Intergovernmental',
                            'International Affairs',
                            'Judiciary Committee',
                            'Juvenile Justice',
                            'Labor Relations',
                            'Landmarks',
                            'Law Department',
                            'Library - Brooklyn',
                            'Library - New York',
                            'Library - Queens',
                            'Loft Board',
                            'Management and Budget',
                            'Mayor',
                            'Metropolitan Transportation Authority',
                            'NYCERS',
                            'Operations',
                            'Parks and Recreation',
                            'Payroll Administration',
                            'Police',
                            'Police Pension Fund',
                            'Probation',
                            'Public Advocate',
                            'Public Health',
                            'Public Housing-NYCHA',
                            'Records',
                            'Rent Guidelines',
                            'Sanitation',
                            'School Construction',
                            'Small Business Svcs',
                            'Sports Commission',
                            'Standards and Appeal',
                            'Tax Appeals Tribunal',
                            'Tax Commission',
                            'Taxi and Limousine',
                            'Transportation',
                            'Trials and Hearings',
                            'Veterans - Military',
                            'Volunteer Center',
                            'Voter Assistance',
                            'Youth & Community'), nullable=False)
    category = db.Column(db.Enum('Business and Consumers',
                             'Cultural/Entertainment',
                             'Education',
                             'Environment',
                             'Finance and Budget',
                             'Government Policy',
                             'Health',
                             'Housing and Buildings',
                             'Human Services',
                             'Labor Relations',
                             'Public Safety',
                             'Recreation/Parks',
                             'Sanitation',
                             'Technology',
                             'Transportation'))
    type = db.Column(db.Enum('Annual Report',
                         'Audit Report',
                         'Bond Offering - Official Statements',
                         'Budget Report',
                         'Consultant Report',
                         'Guide - Manual',
                         'Hearing - Minutes',
                         'Legislative Document',
                         'Memoranda - Directive',
                         'Press Release',
                         'Serial Publication',
                         'Staff Report',
                         'Report'), nullable=False)
    users = db.relationship('Submit')

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    first = db.Column(db.String(255), nullable=False)
    last = db.Column(db.String(255), nullable=False)
    agency = db.Column(db.Enum( 'Aging',
                            'Buildings',
                            'Campaign Finance',
                            'Children''s Services',
                            'City Council',
                            'City Clerk',
                            'City Planning',
                            'Citywide Admin Svcs',
                            'Civilian Complaint',
                            'Comm - Police Corr',
                            'Community Assistance',
                            'Comptroller',
                            'Conflicts of Interest',
                            'Consumer Affairs',
                            'Contracts',
                            'Correction',
                            'Criminal Justice Coordinator',
                            'Cultural Affairs',
                            'DOI - Investigation',
                            'Design/Construction',
                            'Disabilities',
                            'District Atty, NY County',
                            'Districting Commission',
                            'Domestic Violence',
                            'Economic Development',
                            'Education, Dept. of',
                            'Elections, Board of',
                            'Emergency Mgmt.',
                            'Employment',
                            'Empowerment Zone',
                            'Environmental - DEP',
                            'Environmental - OEC',
                            'Environmental - ECB',
                            'Equal Employment',
                            'Film/Theatre',
                            'Finance',
                            'Fire',
                            'FISA',
                            'Health and Mental Hyg.',
                            'HealthStat',
                            'Homeless Services',
                            'Hospitals - HHC',
                            'Housing - HPD',
                            'Human Rights',
                            'Human Rsrcs - HRA',
                            'Immigrant Affairs',
                            'Independent Budget',
                            'Info. Tech. and Telecom.',
                            'Intergovernmental',
                            'International Affairs',
                            'Judiciary Committee',
                            'Juvenile Justice',
                            'Labor Relations',
                            'Landmarks',
                            'Law Department',
                            'Library - Brooklyn',
                            'Library - New York',
                            'Library - Queens',
                            'Loft Board',
                            'Management and Budget',
                            'Mayor',
                            'Metropolitan Transportation Authority',
                            'NYCERS',
                            'Operations',
                            'Parks and Recreation',
                            'Payroll Administration',
                            'Police',
                            'Police Pension Fund',
                            'Probation',
                            'Public Advocate',
                            'Public Health',
                            'Public Housing-NYCHA',
                            'Records',
                            'Rent Guidelines',
                            'Sanitation',
                            'School Construction',
                            'Small Business Svcs',
                            'Sports Commission',
                            'Standards and Appeal',
                            'Tax Appeals Tribunal',
                            'Tax Commission',
                            'Taxi and Limousine',
                            'Transportation',
                            'Trials and Hearings',
                            'Veterans - Military',
                            'Volunteer Center',
                            'Voter Assistance',
                            'Youth & Community'), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(255), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.date.today)
    last_visited = db.Column(db.Date, default=datetime.date.today)
    visits = db.Column(db.Integer, default=0)
    documents = db.relationship('Submit')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)


class Submit(db.Model):
    __tablename__ = 'Submit'
    uid = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    did = db.Column(db.Integer, db.ForeignKey('Document.id'), primary_key=True)

class Section(db.Model):
    __tablename__ = 'Section'
    did = db.Column(db.Integer, db.ForeignKey('Document.id'), primary_key=True)
    section = db.Column(db.String(255))

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    session['agency'] = user.agency
    session['uid'] = user.id
    return user