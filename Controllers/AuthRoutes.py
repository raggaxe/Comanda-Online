from flask import Flask, session, Markup, Response, flash, url_for
from flask import Blueprint, render_template, request, redirect, send_file, make_response, jsonify
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, PasswordField, validators

from Models.Cliente import Cliente
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


@mod.route('/check_email', methods=['POST'])
def check_email():
    if request.method == "POST":
        email_found = repository.find_one('users', {'email': request.form['email']})
        if email_found is not None:
            return jsonify({'error': 'usuário já cadastrado com esse email'})
        else:
            return jsonify({'status': 'OK'})


@mod.route('/signup', methods=['POST', 'GET'])
def signUpUser():
    if request.method == "GET":
        return render_template('user/signup.html')


@mod.route('/login-cliente', methods=['POST', 'GET'])
def login_clientes():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            user_found = repository.find_one('clientes', {'email': form.email.data})
            if user_found is not None:
                if sha256_crypt.verify(form.password.data, user_found['senha']):
                    if 'token' not in user_found:
                        user_found['token'] = generateOTP()
                    Session.set_session(user_found)
                    return redirect(url_for('user_routes.dashboardCliente'))
                else:
                    flash('Usuário/Senha não corresponde! Tente novamente')
            else:
                flash('Usuário/Senha não corresponde! Tente novamente')
        except Exception as e:
            flash('Algo deu errado, tente novamente')
    return render_template('shared/login-cliente.html', form=form)


class RegistrationForm(Form):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Senha', validators=[validators.DataRequired()])
    confirm_password = PasswordField('Confirmar Senha', validators=[validators.DataRequired(),
                                                                    validators.EqualTo('password',
                                                                                       message='As senhas devem ser iguais')])

class LoginForm(Form):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Senha', validators=[validators.DataRequired()])



@mod.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        email = form.email.data
        user_found = repository.find_one('clientes', {'email': email})
        if user_found is None and email != "":
            user = Cliente(form)
            if user.check_re_password(form):
                new_user = repository.create(user)
                print('criou')
                # token = user.token
                # tagEmail = render_template('bodyEmail.html',
                #                            body=f'BEM-VINDO! VOCE FEZ UMA SOLICITAÇÃO DE TOKEN! TOKEN:{token}')
                # enviar_email(request.form['email'], 'Pedido de TOKEN', tagEmail)
                Session.set_session(new_user)
        return redirect(url_for('user_routes.dashboardCliente'))
    return render_template('shared/register.html', form=form)


@mod.route('/registrar-user', methods=['GET', 'POST'])
def registrar_user():
    if request.method == "POST":
        user_found = repository.find_one('users', {'email': request.form['email']})
        if user_found is None:
            print('resre')
            if request.form['email'] != "":
                user = Usuario(request.form)
                if user.check_re_password(request.form):
                    new_user = repository.create(user)
                    # token = user.token
                    # tagEmail = render_template('bodyEmail.html',
                    #                            body=f'BEM-VINDO! VOCE FEZ UMA SOLICITAÇÃO DE TOKEN! TOKEN:{token}')
                    #
                    # enviar_email(request.form['email'], 'Pedido de TOKEN', tagEmail)
                    Session.set_session(new_user)
                    print(f"BEM-VINDO! VOCE FEZ UMA SOLICITAÇÃO DE TOKEN! TOKEN:{''}")

                    return jsonify({'resp': 'cadasrada'})

                else:
                    flash('Usuário/Senha não está correto, tente novamente.')
                    return jsonify({'erro': 'Usuário/Senha não está correto, tente novamente.'})
        else:
            flash('Usuário já cadastrado.')
            return jsonify({'erro': 'Usuário já cadastrado.'})


@mod.route('/cadastrar-user', methods=['POST', 'GET'])
def cadastro_user():
    if request.method == "GET":
        if 'token' in session:
            return redirect(url_for('auth_routes.login'))

        else:
            return render_template('user/cadastro_user.html')


@mod.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "GET":
        return render_template('user/login.html')
    if request.method == "POST":
        user_found = repository.find_one('users', {'email': request.form['email']})
        if user_found is not None:
            if sha256_crypt.verify(request.form['password'], user_found['senha']):
                Session.set_session(user_found)
                return redirect(url_for('admin_routes.dashboard'))
            else:
                flash('Senha invalida')
                return redirect(url_for('auth_routes.login'))

        if user_found is None:
            flash('Usuario não cadastrado')
            return redirect(url_for('auth_routes.login'))


@mod.route('/logout')
@LoginRequired.login_required
def logout():
    session.clear()
    return redirect(url_for('index_routes.index'))


@mod.route('/esqueci-senha', methods=['POST', 'GET'])
def esqueci_senha():
    if request.method == "GET":
        session.clear()

        return render_template('user/esqueci_senha.html')
    if request.method == "POST":
        userFound = repository.find_one('users', {'email': request.form['email']})
        tagEmail = render_template('senhaEmail.html',
                                   token=f'{userFound["token"]}')

        enviar_email(request.form['email'], 'Criar nova Senha', tagEmail)

        flash('Nova senha enviado para seu email')
        return render_template('user/esqueci_senha.html')


@mod.route('/criar_senha/<token>', methods=['POST', 'GET'])
def nova_senha(token):
    if request.method == "GET":
        return render_template('user/nova_senha.html', token=token)
    if request.method == "POST":
        userFound = repository.find_one('users', {'token': token})
        if userFound is not None:
            repository.update_one('users', {'token': userFound['token']},
                                  {'senha': sha256_crypt.hash(str(request.form['password']))})
            return redirect(url_for('auth_routes.login'))


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
            if request.form['token'] == user_found['token']:
                Session.set_session(user_found)
                if 'is_new_user' not in user_found:
                    return redirect(url_for('admin_routes.novo_fornecedor'))
                else:
                    # do something with the image, nome and detalhes
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
