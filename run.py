#!flask/bin/python
from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')