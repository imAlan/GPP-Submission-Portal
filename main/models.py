from . import db


class Agency(db.Model):
    __tablename__ = 'Agency'
    aid = db.Column(db.Integer(10), primary_key=True, autoincrement=True)
    agency = db.Column(db.enum( 'Aging',
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
    documents = db.relationship('Document', backref='Agency', lazy='dynamic')


class Category(db.Model):
    __tablename__ = 'Category'
    cid = db.Column(db.Integer(10), primary_key=True, autoincrement=True)
    category = db.Column(db.enum('Business and Consumers',
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
                                 'Transportation'), nullable=False)
    documents = db.relationship('Category', backref='Category', lazy='dynamic')


class Type(db.Model):
    __tablename__ = 'Type'
    tid = db.Column(db.Integer(10), primary_key=True, autoincrement=True)
    type = db.Column(db.enum('Annual Report',
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
    documents = db.relationship('Type', backref='Type', lazy='dynamic')


class Document(db.Model):
    __tablename__ = 'Document'
    did = db.Column(db.Integer(10), primary_key=True, autoincrement=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    datePublished = db.Column(db.datetime.date, nullable=False)
    dateSubmitted = db.Column(db.datetime.datetime, nullable=False)
    dateCreated = db.Column(db.datetime.date, nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    common_id = db.Column(db.Integer(10), default=None)
    section_id = db.Column(db.Integer(10), default=None)
    status = db.Column(db.enum('published', 'removed', 'publishing', 'not_approved'), nullable=False, default='publishing')
    approved = db.Column(db.enum('yes', 'no'), default=False)
    reason = db.Column(db.String(255), default=None)
    hardcopy = db.Column(db.enum('yes', 'no'), default=None)
    doc_url = db.Column(db.String(255), default=None)
    num_access = db.Column(db.Integer(10), default=0)
    aid = db.Column(db.Integer(10), db.ForeignKey('Agency.aid'))
    cid = db.Column(db.Integer(10), db.ForeignKey('Category.cid'))
    tid = db.Column(db.Integer(10), db.ForeignKey('Type.tid'))

class User(db.Model):
    __tablename__ = 'User'
    uid =  db.Column(db.Integer(10), primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    first = db.Column(db.String(50), nullable=False)
    last = db.Column(db.String(50), nullable=False)
    aid = db.Column(db.Integer(10), db.ForeignKey('Agency.aid'))
    email = db.Column(db.String(50), nullable=False)
    date_joined = db.Column(db.datatime.date)
    last_visited = db.Column(db.datatime.date)
    visits = db.Column(db.Integer(10), default=0)

