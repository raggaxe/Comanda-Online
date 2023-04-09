from flask import session 

def set_session(user):
    session['logged_in'] = True
    session['_id'] = str(user['_id'])
    session['email'] = user['email']
    session['status'] = user['status']
    session['token'] = user['token']
    # session['foto'] = user['foto'] if user['foto'] else "/static/uploads/comum.jpg"
    session.permanent = True

def set_session_client(user):
    session['logged_in'] = True
    session['_idCliente'] = str(user['_id'])
    session.permanent = True