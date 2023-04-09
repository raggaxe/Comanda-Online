from functools import wraps
from flask import redirect, session, flash,url_for

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Precisa fazer o Login",'danger')
            return redirect(url_for('index_routes.index'))
    return wrap


