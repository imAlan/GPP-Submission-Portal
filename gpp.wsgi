activate_this = '/var/www/http/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys, os
import logging, sys

sys.path.insert(0, '/var/www/http')

logging.basicConfig(stream=sys.stderr)
from app import app as application

if __name__ == '__main__':
    application.run()