from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from forms import LogInForm, SubmitForm1

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

@app.route('/submit1', methods=['POST', 'GET'])
def submit():
    form = SubmitForm1(request.form)
    if request.method == 'POST' and form.validate():
        print "done"
    return render_template('submit.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')