from app import app


#Debug and sqlalchemy_echo overvides the config.py variables
#Remove variables when in production
#DEBUG = True
#SQLALCHEMY_ECHO = True  #logs sql
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:password@localhost/submission"
app.config['SECRET_KEY'] = 'Key To Be Determine'  # secret key to prevent csrf