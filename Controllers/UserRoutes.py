from flask import session, request, Blueprint, jsonify, redirect, send_from_directory, render_template, url_for, \
    current_app
from flask_socketio import emit

from Models.Cliente import Cliente
from Models.Comanda import Comanda
from Models.Pedido import Pedido

from Services import LoginRequired, Session
from Repository.BaseRepository import BaseRepository
from Configs.MongoConfig import MongoConfig
from bson.objectid import ObjectId
import datetime
mod = Blueprint('user_routes', __name__)
repository = BaseRepository(MongoConfig().get_connect())


############### fotos uploads ##################
@mod.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@mod.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == "GET":
        if '_idCliente' in session:
            comanda_aberta = repository.find_one('comandas',
                                          {'_idCliente': ObjectId(session['_idCliente']), 'status': 'aberta'})
            comanda_pendente = repository.find_one('comandas',
                                          {'_idCliente': ObjectId(session['_idCliente']), 'status': 'pendente'})
            if comanda_aberta is not None:
                return redirect(url_for('user_routes.comanda'))
            if comanda_pendente is not None:
                return redirect(url_for('user_routes.pendente'))
            else:
                return render_template('user/cadastro.html', users=repository.find('users', {}))
        else:

            return render_template('user/cadastro.html', users=repository.find('users', {}))

@mod.route('/cliente', methods=['POST', 'GET'])
def handle_client_request():
    if request.method == "GET":
        try:
            if '_idCliente' not in session:
                return redirect(url_for('user_routes.cadastro'))
            cliente = repository.find_one('clientes', {'_id': ObjectId(session['_idCliente'])})
            if cliente is None:
                return redirect(url_for('user_routes.cadastro'))
            comanda = repository.find_one('comandas', {'_idCliente': cliente['_id'], 'status': 'aberta'})
            if comanda is not None:
                return redirect(url_for('user_routes.comanda'))
            return redirect(url_for('user_routes.cadastro'))
        except Exception as e:
            print('erro', e)
            return redirect(url_for('index_routes.index'))

    if request.method == "POST":
        try:
            cpf = request.form['CPF']
            user_id = request.form['estabelecimento']
            mesa_id = ObjectId(request.form['mesa'])

            cliente = repository.find_one('clientes', {'CPF': cpf, '_idUser': user_id})
            if cliente is None:
                new_cliente = Cliente(request.form)
                cliente = repository.create(new_cliente)

            new_form = {'_idMesa': mesa_id, '_idCliente': cliente['_id'], '_idUser': user_id}
            new_comanda = Comanda(new_form)
            repository.create(new_comanda)

            Session.set_session_client(cliente)
            repository.update_one('mesas', {'_idUser': user_id, '_id': mesa_id}, {'status': True})

            return redirect(url_for('user_routes.comanda'))

        except Exception as e:
            print(e)
            return redirect(url_for('user_routes.cliente'), code=404)


@mod.route('/mesas_disponiveis/<user>', methods=['POST', 'GET'])
def mesas_disponiveis(user):
    if request.method == "GET":
        mesas_ordenadas = sorted(repository.find('mesas', {'_idUser': user}),
                                 key=lambda x: int(x['numero_mesa']))
        # Transforme cada objeto ObjectId em uma string antes de retornar a resposta em JSON
        for mesa in mesas_ordenadas:
            mesa['_id'] = str(mesa['_id'])

        return jsonify({'data': mesas_ordenadas})


@mod.route('/comanda', methods=['POST', 'GET'])
@LoginRequired.login_required
def comanda():
    try:
        if request.method == "GET":
            comanda = repository.find_one('comandas',
                                          {'_idCliente': ObjectId(session['_idCliente']), 'status': 'aberta'})
            mesa = repository.find_one('mesas', {'_id': ObjectId(comanda['_idMesa'])})
            lista_cardapios = [item for item in repository.find('cardapios', {'_idUser': comanda['_idUser']})]
            lista_categorias = [item for item in repository.find('categorias', {'_idUser': comanda['_idUser']})]

            PEDIDOS_LIMITE= 10
            for pedido in repository.find('pedidos', {'_idComanda': str(comanda['_id'])}):
                hora_abertura = pedido['created_at']
                if pedido['status'] == True:
                    if datetime.datetime.now() - hora_abertura > datetime.timedelta(minutes=PEDIDOS_LIMITE):
                        repository.update_one('pedidos', {'_id': pedido['_id']}, {
                            'status': 'Tempo Limite',
                        })

            lista_pedidos = [item for item in repository.find('pedidos', {'_idComanda': str(comanda['_id'])})]

            if comanda is not None:

                return render_template('user/comanda.html', comanda=comanda, mesa=mesa, cardapios=lista_cardapios,
                                       categorias=lista_categorias, pedidos=lista_pedidos)

    except Exception as e:
        print(e)
        return redirect(url_for('user_routes.cliente'))

@mod.route('/pendente', methods=['POST', 'GET'])
@LoginRequired.login_required
def pendente():
    try:
        if request.method == "GET":
            comanda_pendente = repository.find_one('comandas',
                                                   {'_idCliente': ObjectId(session['_idCliente']),
                                                    'status': 'pendente'})
            if comanda_pendente is not None:
                return render_template('user/pendente.html', comanda=comanda_pendente)
            else:
                return redirect(url_for('auth_routes.logout'))

    except Exception as e:
        print(e)
        return redirect(url_for('user_routes.cliente'))

@mod.route('/pedido', methods=['POST', 'GET'])
@LoginRequired.login_required
def pedido():
    if request.method == "POST":
        try:
            new_pedido = Pedido(request.form)
            pedido = repository.create(new_pedido)
            return jsonify({'_id': str(pedido['_id'])})

        except Exception as e:
            print(e)
            return redirect(url_for('user_routes.comanda'))

@mod.route('/get_mesa/<string:_idMesa>', methods=['GET'])
def get_mesa(_idMesa):

    mesa = repository.find_one('mesas', {'_id': ObjectId(_idMesa)})
    print(f'getMesa {mesa["numero_mesa"] }')

    return jsonify({'numero_mesa':mesa['numero_mesa']})

@mod.route('/realizar_pagamento', methods=['POST'])
def realizar_pagamento():
    if request.method == "POST":
        try:
            # Acessar os dados enviados pelo AJAX
            forma_pagamento = request.form['btnradio']
            valor = request.form['valor']
            repository.update_one('comandas', {'_id': ObjectId(request.form['_idComanda'])},
                                  {
                                      'valor':valor,
                                      'tipo_pagamento':forma_pagamento,
                                      'status' : 'pendente'
                                   }
                                  )
            response_data = {'redirect_url': url_for('user_routes.pendente')}
            return jsonify(response_data)

        except Exception as e:
            print(e)
            return redirect(url_for('user_routes.comanda'))
