from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, SelectField, TextAreaField, RadioField
from wtforms.validators import Length, InputRequired


class LogInForm(Form):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')


class SubmitForm1(Form):
    title = StringField('Title:', validators=[InputRequired(message="This field is required")])
    type_ = SelectField('Type:', choices=[(0, 'Type'), ('Annual Report', 'Annual Report'), ('Audit Report', 'Audit Report'), ('Bond Offering - Official Statements', 'Bond Offering - Official Statements'), ('Budget Report', 'Budget Report'), ('Consultant Report', 'Consultant Report'), ('Guide - Manual', 'Guide - Manual'), ('Hearing - Minutes', 'Hearing - Minutes'), ('Legislative Document', 'Legislative Document'), ('Memoranda - Directive', 'Memoranda - Directive'), ('Press Release', 'Press Release'), ('Serial Publication', 'Serial Publication'), ('Staff Report', 'Staff Report'), ('Report', 'Report')] , validators=[InputRequired(message="This field is required")])
    year = SelectField('Year:', choices=[(0, 'Year'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010'), ('2009', '2009'), ('2008', '2008'), ('2007', '2007'), ('2006', '2006'), ('2005', '2005'), ('2004', '2004'), ('2003', '2003'), ('2002', '2002'), ('2001', '2001'), ('2000', '2000')], validators=[InputRequired(message="This field is required")])
    month = SelectField('Month:', choices=[(0, 'Month'), ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')] , validators=[InputRequired(message="This field is required")])
    day = SelectField('Day:', choices=[(0, 'Day'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31')], validators=[InputRequired(message="This field is required")])
    num = SelectField('Please Specify:', choices=[(0, 'Sections'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], validators=[InputRequired(message="This field is required")])
    description = TextAreaField('Description: (min 100 chars)', validators=[Length(min=100, max=100)])
    url_question = RadioField('Does this document currently reside on NYC.gov or other approved domain?', choices=[(0, 'No'), (1, 'Yes')], validators=[InputRequired(message="This field is required")])
    part_question = RadioField('Is the document broken into multiple PDF files?', choices=[(0, 'No'), (1, 'Yes')], validators=[InputRequired(message="This field is required")])
    submit = SubmitField('Next')








