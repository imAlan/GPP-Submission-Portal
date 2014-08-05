from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, SelectField, TextAreaField, RadioField, ValidationError
from wtforms.validators import Length, InputRequired, Email, Regexp, Optional
from models import User


class SubmitForm1(Form):
    title = StringField('Title:', validators=[InputRequired(message="This field is required")])
    type_ = SelectField('Type:', choices=[(0, 'Type'), ('Annual Report', 'Annual Report'), ('Audit Report', 'Audit Report'), ('Bond Offering - Official Statements', 'Bond Offering - Official Statements'), ('Budget Report', 'Budget Report'), ('Consultant Report', 'Consultant Report'), ('Guide - Manual', 'Guide - Manual'), ('Hearing - Minutes', 'Hearing - Minutes'), ('Legislative Document', 'Legislative Document'), ('Memoranda - Directive', 'Memoranda - Directive'), ('Press Release', 'Press Release'), ('Serial Publication', 'Serial Publication'), ('Staff Report', 'Staff Report'), ('Report', 'Report')], validators=[InputRequired(message="This field is required")])
    year = SelectField('Year:', choices=[(0, 'Year'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010'), ('2009', '2009'), ('2008', '2008'), ('2007', '2007'), ('2006', '2006'), ('2005', '2005'), ('2004', '2004'), ('2003', '2003'), ('2002', '2002'), ('2001', '2001'), ('2000', '2000')], validators=[InputRequired(message="This field is required")])
    month = SelectField('Month:', choices=[(0, 'Month'), ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], validators=[InputRequired(message="This field is required")])
    day = SelectField('Day:', choices=[(0, 'Day'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31')], validators=[InputRequired(message="This field is required")])
    num = SelectField('Please Specify:', choices=[('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])
    description = TextAreaField('Description:', validators=[InputRequired(message="This field is required"), Length(min=100, max=500, message="Description must be between 100 to 500 characters")])
    url_question = RadioField('Is the document on a website?', choices=[('No', 'No'), ('Yes', 'Yes')], validators=[InputRequired(message="This field is required")])
    part_question = RadioField('Is the document broken into multiple PDF files?', choices=[('No', 'No'), ('Yes', 'Yes')], validators=[InputRequired(message="This field is required")])
    submit = SubmitField('Next')


#used for csrf validation
class SubmitForm2(Form):
    submit = SubmitField('Submit')


class EditForm(Form):
    title = StringField('Title:', validators=[InputRequired(message="This field is required")])
    type_ = SelectField('Type:', choices=[(0, 'Type'), ('Annual Report', 'Annual Report'), ('Audit Report', 'Audit Report'), ('Bond Offering - Official Statements', 'Bond Offering - Official Statements'), ('Budget Report', 'Budget Report'), ('Consultant Report', 'Consultant Report'), ('Guide - Manual', 'Guide - Manual'), ('Hearing - Minutes', 'Hearing - Minutes'), ('Legislative Document', 'Legislative Document'), ('Memoranda - Directive', 'Memoranda - Directive'), ('Press Release', 'Press Release'), ('Serial Publication', 'Serial Publication'), ('Staff Report', 'Staff Report'), ('Report', 'Report')], validators=[InputRequired(message="This field is required")])
    year = SelectField('Year:', choices=[(0, 'Year'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010'), ('2009', '2009'), ('2008', '2008'), ('2007', '2007'), ('2006', '2006'), ('2005', '2005'), ('2004', '2004'), ('2003', '2003'), ('2002', '2002'), ('2001', '2001'), ('2000', '2000')], validators=[InputRequired(message="This field is required")])
    month = SelectField('Month:', choices=[(0, 'Month'), ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], validators=[InputRequired(message="This field is required")])
    day = SelectField('Day:', choices=[(0, 'Day'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31')], validators=[InputRequired(message="This field is required")])
    description = TextAreaField('Description:', validators=[InputRequired(message="This field is required"), Length(min=100, max=500, message="Description must be between 100 to 500 characters")])
    category = SelectField('Category', validators=[Optional()], choices=[(0, 'Category'), ('Business and Consumers', 'Business and Consumers'), ('Cultural/Entertainment', 'Cultural/Entertainment'), ('Education', 'Education'), ('Environment', 'Environment'), ('Finance and Budget', 'Finance and Budget'), ('Government Policy', 'Government Policy'), ('Health', 'Health'), ('Housing and Buildings', 'Housing and Buildings'), ('Human Services', 'Human Services'), ('Labor Relations', 'Labor Relations'), ('Public Safety', 'Public Safety'), ('Recreation/Parks', 'Recreation/Parks'), ('Sanitation', 'Sanitation'), ('Technology', 'Technology'), ('Transportation', 'Transportation')])
    edit = SubmitField('Edit')


class RequestDeletionForm(Form):
    message = TextAreaField('Message:', validators=[InputRequired(message="This field is required")])
    delete = SubmitField('Delete')

class PublishForm(Form):
    submit = SubmitField('Publish')

class RemoveForm(Form):
    submit = SubmitField('Remove')

class SignUpForm(Form):
    username = StringField('Username', validators=[InputRequired(message="This field is required"), Length(min=4, max=30, message="Please use between 4 and 30 characters")])
    password = PasswordField('Password', validators=[InputRequired(message="This field is required"), Length(min=4, message="Please use at least 4 and 30 characters")])
    first = StringField('First Name', validators=[InputRequired(message="This field is required")])
    last = StringField('Last Name', validators=[InputRequired(message="This field is required")])
    agency = SelectField('Agency', choices=[('', 'Agency'), ('Aging', 'Aging'), ('Buildings', 'Buildings'), ('Campaign Finance', 'Campaign Finance'), ('Children''s Services', 'Children''s Services'), ('City Council', 'City Council'), ('City Clerk', 'City Clerk'), ('City Planning', 'City Planning'), ('Citywide Admin Svcs', 'Citywide Admin Svcs'), ('Civilian Complaint', 'Civilian Complaint'), ('Comm - Police Corr', 'Comm - Police Corr'), ('Community Assistance', 'Community Assistance'), ('Comptroller', 'Comptroller'), ('Conflicts of Interest', 'Conflicts of Interest'), ('Consumer Affairs', 'Consumer Affairs'), ('Contracts', 'Contracts'), ('Correction', 'Correction'), ('Criminal Justice Coordinator', 'Criminal Justice Coordinator'), ('Cultural Affairs', 'Cultural Affairs'), ('DOI - Investigation', 'DOI - Investigation'), ('Design/Construction', 'Design/Construction'), ('Disabilities', 'Disabilities'), ('District Atty, NY County', 'District Atty, NY County'), ('Districting Commission', 'Districting Commission'), ('Domestic Violence', 'Domestic Violence'), ('Economic Development', 'Economic Development'), ('Education, Dept. of', 'Education, Dept. of'), ('Elections, Board of', 'Elections, Board of'), ('Emergency Mgmt.', 'Emergency Mgmt.'), ('Employment', 'Employment'), ('Empowerment Zone', 'Empowerment Zone'), ('Environmental - DEP', 'Environmental - DEP'), ('Environmental - OEC', 'Environmental - OEC'), ('Environmental - ECB', 'Environmental - ECB'), ('Equal Employment', 'Equal Employment'), ('Film/Theatre', 'Film/Theatre'), ('Finance', 'Finance'), ('Fire', 'Fire'), ('FISA', 'FISA'), ('Health and Mental Hyg.', 'Health and Mental Hyg.'), ('HealthStat', 'HealthStat'), ('Homeless Services', 'Homeless Services'), ('Hospitals - HHC', 'Hospitals - HHC'), ('Housing - HPD', 'Housing - HPD'), ('Human Rights', 'Human Rights'), ('Human Rsrcs - HRA', 'Human Rsrcs - HRA'), ('Immigrant Affairs', 'Immigrant Affairs'), ('Independent Budget', 'Independent Budget'), ('Info. Tech. and Telecom.', 'Info. Tech. and Telecom.'), ('Intergovernmental', 'Intergovernmental'), ('International Affairs', 'International Affairs'), ('Judiciary Committee', 'Judiciary Committee'), ('Juvenile Justice', 'Juvenile Justice'), ('Labor Relations', 'Labor Relations'), ('Landmarks', 'Landmarks'), ('Law Department', 'Law Department'), ('Library - Brooklyn', 'Library - Brooklyn'), ('Library - New York', 'Library - New York'), ('Library - Queens', 'Library - Queens'), ('Loft Board', 'Loft Board'), ('Management and Budget', 'Management and Budget'), ('Mayor', 'Mayor'), ('Metropolitan Transportation Authority', 'Metropolitan Transportation Authority'), ('NYCERS', 'NYCERS'), ('Operations', 'Operations'), ('Parks and Recreation', 'Parks and Recreation'), ('Payroll Administration', 'Payroll Administration'), ('Police', 'Police'), ('Police Pension Fund', 'Police Pension Fund'), ('Probation', 'Probation'), ('Public Advocate', 'Public Advocate'), ('Public Health', 'Public Health'), ('Public Housing-NYCHA', 'Public Housing-NYCHA'), ('Records', 'Records'), ('Rent Guidelines', 'Rent Guidelines'), ('Sanitation', 'Sanitation'), ('School Construction', 'School Construction'), ('Small Business Svcs', 'Small Business Svcs'), ('Sports Commission', 'Sports Commission'), ('Standards and Appeal', 'Standards and Appeal'), ('Tax Appeals Tribunal', 'Tax Appeals Tribunal'), ('Tax Commission', 'Tax Commission'), ('Taxi and Limousine', 'Taxi and Limousine'), ('Transportation', 'Transportation'), ('Trials and Hearings', 'Trials and Hearings'), ('Veterans - Military', 'Veterans - Military'), ('Volunteer Center', 'Volunteer Center'), ('Voter Assistance', 'Voter Assistance'), ('Youth & Community', 'Youth & Community')], validators=[InputRequired(message="This field is required")])
    phone = StringField('Phone', validators=[InputRequired(message="This field is required"), Regexp(r'\d\d\d-\d\d\d-\d\d\d\d', message="Please input phone number as ###-###-####")])
    email = StringField('Email', validators=[InputRequired(message="This field is required"), Email(message="Not a valid email address")])
    role = SelectField('Role', choices=[('', 'Role'), ('User', 'User'), ('Admin', 'Admin'), ('Agency_Admin', 'Agency_Admin')], validators=[InputRequired(message="This field is required")])
    submit = SubmitField('Add User')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already register.')