from flask import session, request, send_from_directory, current_app, Blueprint, jsonify, redirect, \
    render_template, url_for
from werkzeug.utils import secure_filename
from Models.Cardapio import Cardapio
from Models.Categoria import Categoria
from Models.Comanda import Comanda
from Services import LoginRequired, Session
from Repository.BaseRepository import BaseRepository
from Configs.MongoConfig import MongoConfig
from Models.Mesa import *
import os
from bson.objectid import ObjectId
import datetime

from Services.CadastroLojista import CadastroLogista

mod = Blueprint('admin_routes', __name__)
repository = BaseRepository(MongoConfig().get_connect())

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@mod.route('/dashboard', methods=['GET', 'POST'])
@LoginRequired.login_required
def dashboard():
    if request.method == "GET":
        if '_id' in session:
            id_user = ObjectId(session['_id'])
            user_found = repository.find_one('users', {'_id': id_user})
            if user_found is not None:
                if user_found['CNPJ'] != '':
                    lista_cardapios = [item for item in repository.find('cardapios', {'_idUser': session['_id']})]
                    lista_comandas = [item for item in repository.find('comandas', {'_idUser': session['_id']})]
                    lista_pedidos = [item for item in repository.find('pedidos', {'_idUser': session['_id']})]
                    lista_mesas = [item for item in repository.find('mesas', {'_idUser': session['_id']})]
                    lista_clientes = [item for item in repository.find('clientes', {'_idUser': session['_id']})]
                    lista_categorias = [item for item in repository.find('categorias', {'_idUser': session['_id']})]

                    comandas_fechadas = set()
                    for comanda in lista_comandas:
                        if comanda['status'] == 'realizado':
                            comandas_fechadas.add(str(comanda['_id']))

                            # print(comandas_fechadas)
                    total_vendas = 0
                    if len(comandas_fechadas) > 0:
                        for pedido in lista_pedidos:
                            if str(pedido['_idComanda']) in comandas_fechadas:
                                _quantidade = int(pedido["quantidade"])
                                _valor = repository.find_one("cardapios", {"_id": ObjectId(pedido["_idCardapio"])})["valor"]

                                subTotal = int(_quantidade) * float(_valor.replace(',', '.'))
                                total_vendas = total_vendas + subTotal

                    return render_template('menu/dashboard.html',
                                           comandas=lista_comandas,
                                           pedidos=lista_pedidos,
                                           mesas=lista_mesas,
                                           cardapios=lista_cardapios,
                                           clientes=lista_clientes,
                                           categorias=lista_categorias,
                                           total_vendas="R$ {:.2f}".format(total_vendas).replace(".", ",")
                                           )
                else:
                    return redirect(url_for('admin_routes.novo_fornecedor'))
            else:
                return render_template('user/cadastro.html')
    return redirect(url_for('index_routes.index'))


@mod.route('/primeiro-acesso', methods=['POST', 'GET'])
@LoginRequired.login_required
def novo_fornecedor():
    return render_template('menu/primeiro_acesso.html')






# GERENCIAR MESAS
@mod.route('/mesas', methods=['POST', 'GET'])
@LoginRequired.login_required
def mesas():
    if request.method == "GET":
        mesas_ordenadas = sorted(repository.find('mesas', {'_idUser': session['_id']}),
                                 key=lambda x: int(x['numero_mesa']))
        user_found = repository.find_one('users', {'_id': ObjectId(session['_id'])})
        return render_template('user/mesas.html', mesas=mesas_ordenadas,
                               max_mesas=10 if not 'max_mesas' in user_found else user_found['max_mesas'])

    if request.method == "POST":
        mesa_found = repository.find_one('mesas',
                                         {'_idUser': session['_id'], 'numero_mesa': request.form['numero_mesa']})
        if mesa_found is None:
            new_Mesa = Mesa(request.form, session['_id'])
            repository.create(new_Mesa)
        else:
            print('mesa ja criada')
        return redirect(url_for('admin_routes.mesas'))


@mod.route('/remover_mesa', methods=['POST', 'GET'])
@LoginRequired.login_required
def remover_mesa():
    if request.method == "POST":
        repository.delete_one('mesas', {'_id': ObjectId(request.form['_idMesa'])})
        return redirect(url_for('admin_routes.mesas'))


@mod.route('/status_mesa', methods=['POST', 'GET'])
@LoginRequired.login_required
def status_mesa():
    if request.method == "POST":
        mesa_found = repository.find_one('mesas', {'_id': ObjectId(request.form['_id'])})
        status = True
        if mesa_found is not None:
            if request.form['no-ativo'] == 'true':
                status = False
            else:
                form = {
                    '_idMesa': str(mesa_found['_id']),
                    '_idCliente': str(mesa_found['_idUser']),
                    '_idUser': str(mesa_found['_idUser']),
                }
                new_comanda = Comanda(form)
                repository.create(new_comanda)

        repository.update_one('mesas', {'_id': ObjectId(request.form['_id'])},
                              {
                                  'status': status,
                              }
                              )
    return redirect(url_for('admin_routes.mesas'))


@mod.route('/max_mesas/<data>', methods=['POST'])
def receive_ajax(data):
    if request.method == "POST":
        repository.update_one('users', {'_id': ObjectId(session['_id'])}, {'max_mesas': data})
        return jsonify({'success': True})  # Retorna uma resposta em formato JSON


# GERENCIAR CARDAPIO
@mod.route('/cardapio', methods=['POST', 'GET'])
@LoginRequired.login_required
def cardapio():
    if request.method == "GET":
        lista_cardapios = [item for item in repository.find('cardapios', {'_idUser': session['_id']})]
        lista_categorias = [item for item in repository.find('categorias', {'_idUser': session['_id']})]
        return render_template('user/cardapio.html', cardapios=lista_cardapios, categorias=lista_categorias)
    if request.method == "POST":
        try:
            estoque = request.form.get('estoque') if not request.form.get('no-stock') else False
            categoria = False if request.form['categoria'] == 'Escolha a categoria' else request.form['categoria']
            filename = 'comum.jpg'
            file = request.files.get('file')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            new_cardapio = Cardapio(request.form, filename, estoque, categoria, session['_id'])
            repository.create(new_cardapio)
            return redirect(url_for('admin_routes.cardapio'))
        except Exception as e:
            return redirect(url_for('admin_routes.cardapio'))


@mod.route('/edit_cardapio', methods=['POST', 'GET'])
@LoginRequired.login_required
def edit_cardapio():
    cardapios = repository.find_one('cardapios', {"_id": ObjectId(request.form['produto_remove'])})
    if request.method == "POST":
        if cardapios is not None:
            file = request.files.get('file')
            filename = cardapios.get('filename')

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            estoque = request.form.get('estoque') if not request.form.get('no-stock') else False

            categoria_id = request.form.get('categoria')
            categoria = repository.find_one('categorias', {"_id": ObjectId(categoria_id)})[
                '_id'] if categoria_id and categoria_id != 'Escolha a categoria' else False

            repository.update_one('cardapios', {"_id": ObjectId(request.form['produto_remove'])},
                                  {
                                      'filename': filename,
                                      'nome_produto': request.form['nome'],
                                      'valor': request.form['valor'],
                                      'estoque': estoque,
                                      'categoria': categoria,
                                      'tempo_estimado': request.form['tempo'],
                                  })

            return redirect(url_for('admin_routes.cardapio'))


@mod.route('/status_cardapio', methods=['POST', 'GET'])
@LoginRequired.login_required
def status_cardapio():
    if request.method == "POST":
        cardapios = repository.find_one('cardapios', {"_id": ObjectId(request.form['produto_remove'])})
        status = True
        if cardapios is not None:
            if request.form['no-ativo'] == 'true':
                status = False
        repository.update_one('cardapios', {"_id": ObjectId(request.form['produto_remove'])},
                              {
                                  'status': status,
                              }
                              )
        return redirect(url_for('admin_routes.cardapio'))


# GERENCIAR CATEGORIA
@mod.route('/categoria', methods=['POST', 'GET'])
@LoginRequired.login_required
def categoria():
    if request.method == "POST":
        categoria_found = repository.find_one('categoria', {'nome': request.form['nome'], '_idUser': session['_id']})
        if categoria_found is None:
            new_categoria = Categoria(request.form, session['_id'])
            repository.create(new_categoria)
        return redirect(url_for('admin_routes.cardapio'))


@mod.route('/excluir_categoria', methods=['POST', 'GET'])
@LoginRequired.login_required
def excluir_categoria():
    if request.method == "POST":
        repository.delete_one('categorias', {'_id': ObjectId(request.form['_idCategoria'])})
        return redirect(url_for('admin_routes.cardapio'))


import datetime


@mod.route('/pedidos', methods=['POST', 'GET'])
@LoginRequired.login_required
def pedidos():
    if request.method == "GET":
        # Obter todas as comandas e pedidos do usuário atual
        lista_comandas = [item for item in repository.find('comandas', {'_idUser': session['_id']})]
        lista_pedidos = [item for item in repository.find('pedidos', {'_idUser': session['_id']})]

        # Fechar as comandas que foram abertas há mais de 24 horas e não possuem pedidos
        comandas_24h = set()
        for comanda in lista_comandas:
            hora_abertura = comanda['hora_abertura']
            if comanda['status'] == 'aberta' and datetime.datetime.now() - hora_abertura > datetime.timedelta(hours=24):
                comandas_24h.add(str(comanda['_id']))

        if len(comandas_24h) > 0:
            for pedido in lista_pedidos:
                if str(pedido['_idComanda']) in comandas_24h:
                    comandas_24h.discard(str(pedido['_idComanda']))

            for comanda_vazia in comandas_24h:
                repository.update_one('comandas', {'_id': ObjectId(comanda_vazia)}, {
                    'status': 'fechado',
                    'hora_fechamento': datetime.datetime.now(),
                    'tipo_pagamento': 'fechado'
                })
                print(f'Não existe pedido na comanda {comanda_vazia}')

        # Obter as vendas totais para cada dia da semana passada
        today = datetime.date.today()
        dates = []
        for i in range(0, 7):
            date = today - datetime.timedelta(days=i)
            dateString = date.strftime('%d-%m-%Y')
            dates.append(dateString)

        vendas_por_dia = {}
        for date in dates:
            vendas_por_dia[date] = 0

        # Obter comandas abertas para cada dia da semana passada
        comandas_abertas_por_dia = {}
        for date in dates:
            comandas_abertas_por_dia[date] = 0

        for comanda in lista_comandas:
            hora_abertura = comanda['hora_abertura']
            date_str = hora_abertura.strftime('%d-%m-%Y')
            if date_str in comandas_abertas_por_dia and comanda['status'] == 'aberta':
                comandas_abertas_por_dia[date_str] += 1

        for pedido in lista_pedidos:
            created_at = datetime.datetime.fromisoformat(str(pedido['created_at']))

            if created_at.date() >= today - datetime.timedelta(days=7):
                valor_total = 0
                cardapio = repository.find_one('cardapios', {'_id': ObjectId(pedido['_idCardapio'])})
                valor_total += int(pedido['quantidade']) * float(cardapio['valor'].replace(',', '.'))

                date_str = created_at.strftime('%d-%m-%Y')
                if date_str in vendas_por_dia:
                    vendas_por_dia[date_str] += valor_total

        links = [{'href': '#' + date, 'text': date, 'vendas': "R$ {:.2f}".format(vendas_por_dia[date]),
                  'comandas_abertas': comandas_abertas_por_dia[date]} for date in dates]
        return render_template('user/pedidos.html', comandas=lista_comandas, pedidos=lista_pedidos,
                               vendas_por_dia=vendas_por_dia, links=links)


@mod.route('/aceitar_pedidos', methods=['POST'])
@LoginRequired.login_required
def aceitar_pedidos():
    _idPedido = request.form['_idPedido']
    repository.update_one('pedidos', {'_id': ObjectId(_idPedido)}, {'status': 'Aceito'})
    return jsonify({'success': True})


@mod.route('/entregar_pedidos', methods=['POST', 'GET'])
@LoginRequired.login_required
def entregar_pedidos():
    if request.method == "POST":
        repository.update_one('pedidos', {'_id': ObjectId(request.form['_idPedido'])}, {'status': 'Entregue'})
        return jsonify({'success': True})


@mod.route('/comanda_info', methods=['GET'])
@LoginRequired.login_required
def comanda_info():
    try:
        _idMesa = request.args.get('_idMesa')
        comandas_info = repository.find_one('comandas', {'_idMesa': _idMesa, 'status': 'aberta'})
        is_admin_comanda = False
        if comandas_info is not None:
            lista_pedidos = [item for item in repository.find('pedidos', {'_idComanda': str(comandas_info['_id'])})]
            if comandas_info['_idUser'] != comandas_info['_idCliente']:
                user = repository.find_one('clientes', {'_id': ObjectId(comandas_info['_idCliente'])})
            else:
                is_admin_comanda = True
                user = {
                    "nome": "Cliente sem App",
                    "CPF": "Estabelecimento"

                }
            pedidos = []
            total = 0
            for pedido in lista_pedidos:
                quantidade = pedido['quantidade']
                cardapio = repository.find_one('cardapios', {'_id': ObjectId(pedido['_idCardapio'])})
                pedido['nome_produto'] = cardapio['nome_produto']
                pedido['valor'] = float(cardapio['valor']) * int(quantidade)
                total += pedido['valor']
                pedido['valor'] = "R$ {:.2f}".format(pedido['valor'])

                pedido['_id'] = str(pedido['_id'])
                pedidos.append(pedido)

            return jsonify({
                '_idMesa': _idMesa,
                '_idComanda': str(comandas_info['_id']),
                'nome_cliente': user['nome'],
                'CPF': user['CPF'],
                'hora_abertura': comandas_info['hora_abertura'].strftime('%d/%m/%Y %H:%M'),
                '_idCliente': str(comandas_info['_idCliente']),
                'pedidos': lista_pedidos,
                'total': "R$ {:.2f}".format(total),
                'is_admin_comanda': is_admin_comanda,
            })
        else:
            return jsonify({'erro': 'comanda nao encontrada'})
    except TypeError as e:
        return jsonify({'erro': e})


@mod.route('/comanda_admin', methods=['POST'])
@LoginRequired.login_required
def comanda_admin():
    try:
        if request.method == "POST":
            print(request.form)
            comanda = repository.find_one('comandas',
                                          {'_id': ObjectId(request.form['_idComanda']), 'status': 'aberta'})

            mesa = repository.find_one('mesas', {'_id': ObjectId(comanda['_idMesa'])})
            lista_cardapios = [item for item in repository.find('cardapios', {'_idUser': comanda['_idUser']})]
            lista_categorias = [item for item in repository.find('categorias', {'_idUser': comanda['_idUser']})]

            PEDIDOS_LIMITE = 10
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
        return redirect(url_for('admin_routes.mesas'))


# Gerenciar Pagamentos

@mod.route('/pagamentos', methods=['POST', 'GET'])
@LoginRequired.login_required
def pagamentos():
    if request.method == "GET":
        lista_comandas = [item for item in repository.find('comandas', {'_idUser': session['_id']})]
        lista_pedidos = [item for item in repository.find('pedidos', {'_idUser': session['_id']})]

        comandas_24h = set()
        comandas_fechadas = set()

        for comanda in lista_comandas:
            hora_abertura = comanda['hora_abertura']
            if comanda['status'] == 'aberta':
                if datetime.datetime.now() - hora_abertura > datetime.timedelta(hours=24):
                    comandas_24h.add(str(comanda['_id']))
            if comanda['status'] == 'realizado':
                comandas_fechadas.add(str(comanda['_id']))

        if len(comandas_24h) > 0:
            for pedido in lista_pedidos:
                if str(pedido['_idComanda']) in comandas_24h:
                    comandas_24h.discard(str(pedido['_idComanda']))
            for comanda_vazia in comandas_24h:
                lista_comandas = repository.update_one('comandas', {'_id': ObjectId(comanda_vazia)}, {
                    'status': 'fechado',
                    'hora_fechamento': datetime.datetime.now(),
                    'tipo_pagamento': 'fechado'
                })
                print(f'Não existe pedido na comanda {comanda_vazia}')
        total_vendas = 0
        if len(comandas_fechadas) > 0:
            for pedido in lista_pedidos:
                if str(pedido['_idComanda']) in comandas_fechadas:
                    _quantidade = int(pedido["quantidade"])
                    _valor = repository.find_one("cardapios", {"_id": ObjectId(pedido["_idCardapio"])})["valor"]

                    subTotal = int(_quantidade) * float(_valor.replace(".", ","))
                    total_vendas = total_vendas + subTotal

        today = datetime.date.today()

        links = []
        for i in range(0, 7):
            date = today - datetime.timedelta(days=i)
            dateString = date.strftime('%d-%m-%Y')
            links.append({'href': '#' + dateString, 'text': dateString})

        return render_template('user/pagamentos.html', comandas=lista_comandas, pedidos=lista_pedidos, links=links,
                               agora=datetime.datetime.now(),
                               total_vendas="R$ {:.2f}".format(total_vendas).replace(".", ","))


@mod.route('/finalizar_pagamento', methods=['POST', 'GET'])
@LoginRequired.login_required
def finalizar_pagamento():
    if request.method == "POST":
        comanda = repository.update_one('comandas', {'_id': ObjectId(request.form['_idComanda'])},
                                        {
                                            'status': 'realizado'
                                        }
                                        )
        repository.update_one('mesas',
                              {'_id': ObjectId(comanda['_idMesa'])},
                              {'status': False}
                              )
        response_data = {'redirect_url': url_for('admin_routes.dashboard'), '_idUser': str(comanda['_idUser'])}
        return jsonify(response_data)


# Gerenciar Clientes
@mod.route('/clientes', methods=['POST', 'GET'])
@LoginRequired.login_required
def clientes():
    if request.method == "GET":
        try:
            # Buscar dados do banco
            lista_pedidos = list(repository.find('pedidos', {'_idUser': session['_id']}))
            lista_comandas = list(repository.find('comandas', {'_idUser': session['_id']}))
            lista_clientes = list(repository.find('clientes', {'_idUser': session['_id']}))

            # Contar comandas por cliente
            comandas_por_cliente = {}
            for comanda in lista_comandas:
                id_cliente = comanda['_idCliente']
                if id_cliente not in comandas_por_cliente:
                    comandas_por_cliente[id_cliente] = {'num_comandas': 1, 'comandas': [comanda['_id']]}
                else:
                    comandas_por_cliente[id_cliente]['num_comandas'] += 1
                    comandas_por_cliente[id_cliente]['comandas'].append(comanda['_id'])

            # Contar pedidos por cliente
            pedidos_por_cliente = {}
            quantidade_itens = 0

            for pedido in lista_pedidos:
                id_comanda = pedido['_idComanda']
                comanda = repository.find_one('comandas', {'_id': ObjectId(id_comanda), '_idUser': session['_id']})
                id_cliente = comanda['_idCliente']
                id_pedido = pedido['_id']
                _quantidade = pedido['quantidade']
                _valor = \
                    repository.find_one('cardapios',
                                        {'_id': ObjectId(pedido['_idCardapio']), '_idUser': session['_id']})[
                        'valor']

                quantidade_itens = quantidade_itens + int(_quantidade)
                if comanda['status'] == 'realizado':
                    if id_cliente not in pedidos_por_cliente:
                        pedidos_por_cliente[id_cliente] = {'num_pedidos': 1, 'pedidos': [id_pedido],
                                                           'produtos': int(quantidade_itens),
                                                           'total': int(_quantidade) * float(_valor)}
                    else:
                        pedidos_por_cliente[id_cliente]['num_pedidos'] += 1
                        pedidos_por_cliente[id_cliente]['produtos'] += int(_quantidade)
                        pedidos_por_cliente[id_cliente]['total'] += int(_quantidade) * float(_valor)
                        pedidos_por_cliente[id_cliente]['pedidos'].append(id_pedido)

            # Renderizar template
            return render_template('user/clientes_cadastrados.html',
                                   comandas_por_cliente=comandas_por_cliente,
                                   pedidos_por_cliente=pedidos_por_cliente,
                                   lista_clientes=lista_clientes)

        except Exception as e:
            print('erro', e)
            return redirect(url_for('index_routes.index'))
