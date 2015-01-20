from app import app
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://submission:D0R15_5ubm15510N@10.155.145.91/submission"
app.config['SECRET_KEY'] = 'Key To Be Determine'  # secret key to prevent csrf
#Debug and sqlalchemy_echo overvides the config.py variables
#Remove variables when in production
#DEBUG = True
#SQLALCHEMY_ECHO = True  #logs sql
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:password@localhost/submission"
app.config['UPLOAD_FOLDER'] = '/export/local/admin/GPP-Submission-Portal/app/static/data/gppPdfs'
app.config['DOC_PATH'] = '/static/data/gppPdfs'

a