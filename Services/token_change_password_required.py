from functools import wraps
from flask import redirect, session, flash,url_for

def token_change_password_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'changePass' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return wrap

