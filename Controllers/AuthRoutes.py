from flask import Flask, session, Markup, Response, flash, url_for
from flask import Blueprint, render_template, request, redirect, send_file, make_response, jsonify
from passlib.hash import sha256_crypt
from Services import EnviarEmail, GerarOTP, LoginRequired, MaskEmail, Session, Google
from Services.EnviarEmail import enviar_email
from Repository.BaseRepository import BaseRepository
from Configs.MongoConfig import MongoConfig
from flask_dance.contrib.facebook import facebook
from bson.objectid import ObjectId
from Models.User import Usuario
from Services.GerarOTP import generateOTP


mod = Blueprint('auth_routes', __name__)
repository = BaseRepository(MongoConfig().get_connect())






@mod.route('/signup', methods=['POST','GET'])
def signUpUser():
    if request.method == "GET":
        return render_template('user/signup.html')


@mod.route('/login', methods=['POST','GET'])
def login():
    if request.method == "GET":
        if 'token' in session:
            return redirect(url_for('admin_routes.dashboard'))

        else:
            return render_template('user/login.html')



    # if request.method == "POST":
    #     user_found = repository.find_one('users', {'username': request.form['username']})
    #     if user_found is not None:
    #         if sha256_crypt.verify(request.form['pwd'], user_found['password']):
    #             Session.set_session(user_found)
    #             return make_response(jsonify({'resp': user_found['status']}), 200)
    #         else:
    #             return make_response(jsonify({'erro': 'Usuário/Senha não está correto, tente novamente.'}), 200)
    #
    #     if user_found is None:
    #         return make_response(jsonify({'erro': 'Usuário/Senha não está correto, tente novamente.'}), 200)


@mod.route('/logout')
@LoginRequired.login_required
def logout():
    session.clear()
    return redirect(url_for('index_routes.index'))


######## GERAR TOKEN #######

@mod.route('/ativar', methods=['POST'])
def getToken():
    if request.method == "POST":
     try:
         user_found = repository.find_one('users', {'email': request.form['email']})

         session['email'] = request.form['email']
         if user_found is not None:
             token = generateOTP()
             repository.update_one('users', {'email': request.form['email']}, {'token': token})

         else:
             user = Usuario(request.form)
             repository.create(user)
             token = user.token
         tagEmail = render_template('user/email.html',
                                    token=f'{token}')
         enviar_email(request.form['email'], 'Pedido de TOKEN', tagEmail)
         print(f"BEM-VINDO! VOCE FEZ UMA SOLICITAÇÃO DE TOKEN! TOKEN:{token}")
         return render_template('user/token.html', email=request.form['email'])
         # return  render_template('user/token.html',email=request.form['email'])
     except Exception as e:
         print(e)
         return redirect(url_for('auth_routes.login'))



@mod.route('/validar', methods=['POST'])
def validarToken():
    if request.method == "POST":
        user_found = repository.find_one('users', {'email': session['email']})
        if user_found is not None:
            print(user_found)
            if request.form['token'] == user_found['token']:
                Session.set_session(user_found)
                return redirect(url_for('admin_routes.dashboard'))
            else:
                return redirect(url_for('auth_routes.login'))
        else:
            return redirect(url_for('auth_routes.login'))

    return redirect(url_for('index_routes.index'))

@mod.route('/resetarToken', methods=['GET', 'POST'])
def resetarToken():
    if request.method == "GET":
        new_token = GerarOTP.generateOTP()
        user = repository.update_one('users', {'_id': ObjectId(session['idUser'])}, {'token', new_token})

        tagEmail = render_template('bodyEmail.html', body=f'NOVO TOKEN GERADO {user.token}')
        enviar_email(user['email'], 'NOVO TOKEN', tagEmail)

        return render_template('gestao_user/sucessoToken.html', email=MaskEmail.maskEmail(user['email']))

