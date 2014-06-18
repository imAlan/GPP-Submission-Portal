from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from forms import LogInForm

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'hi'

@app.route('/')
def home():
    form = LogInForm()
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')