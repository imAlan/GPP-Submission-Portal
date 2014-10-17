from flask import abort
from flask.ext.login import current_user
from functools import wraps
from flask import redirect, url_for

#decorator for admin; check if user role is Admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user is None:
            return redirect(url_for('home'))
        elif current_user.role != 'Admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#decorator for admin; check if user role is Agency Admin
def agency_or_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user is None:
            return redirect(url_for('home'))
        elif current_user.role == 'User':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function