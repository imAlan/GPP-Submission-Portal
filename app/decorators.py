from flask import abort
from flask.ext.login import current_user
from functools import wraps
from flask import redirect, url_for


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print "admin"
        if current_user is None:
            print "No"
            return redirect(url_for('home'))
        elif current_user.role != 'Admin':
            print "aborting"
            abort(403)
        return f(*args, **kwargs)
    return decorated_function