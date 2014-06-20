from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from forms import LogInForm

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'hi'

@app.route('/')
def index():
    form = LogInForm()
    return render_template('index.html', form=form)

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/submit')
def submit():
    return render_template('submit.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')