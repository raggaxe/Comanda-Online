import json
import locale
import pprint

from flask import session, request, send_from_directory, current_app, Blueprint, jsonify, redirect, \
    render_template, url_for, flash
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
import re




mod = Blueprint('admin_routes', __name__)
repository = BaseRepository(MongoConfig().get_connect())

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Define a localidade para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.utf-8')

metricas = [
    {
        "tipo": 'unid',
        "nome": "Unidade (unid)"
    },
    {
        "tipo": 'cx',
        "nome": "Caixa(Cx)"
    },
    {
        "tipo": 'kg',
        "nome": "Kilo(Kg)"
    },
    {
        "tipo": 'ml',
        "nome": "Mililitro(ml)"
    },
]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_currency_format(value):
    # Remove o símbolo de moeda e substitui o separador de milhares e decimal
    value = re.sub(r'[^\d.,]', '', value)
    value = value.replace('.', '').replace(',', '.')
    return value
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


                    count_pedidos_aceito = sum(1 for comanda in lista_comandas if comanda['status'] == 'Aceito')
                    count_pedidos_checkout = sum(1 for comanda in lista_comandas if comanda['status'] == 'checkout')

                    comandas_fechadas = set()
                    for comanda in lista_comandas:
                        if comanda['status'] == 'realizado':
                            comandas_fechadas.add(str(comanda['_id']))

                    total_vendas = 0
                    if len(comandas_fechadas) > 0:
                        for pedido in lista_pedidos:
                            if str(pedido['_idComanda']) in comandas_fechadas:
                                _quantidade = int(pedido["quantidade"])
                                _valor = repository.find_one("cardapios", {"_id": ObjectId(pedido["_idCardapio"])})

                                if _valor is not None:
                                    subTotal = int(_quantidade) * float(remove_currency_format(_valor["valor"]))
                                    total_vendas = total_vendas + subTotal
                                else:
                                    total_vendas = 0


                    return render_template('menu/dashboard.html',
                                           comandas=lista_comandas,
                                           pedidos=lista_pedidos,
                                           mesas=lista_mesas,
                                           cardapios=lista_cardapios,
                                           clientes=lista_clientes,
                                           categorias=lista_categorias,
                                           count_pedidos_aceito=count_pedidos_aceito,
                                           count_pedidos_checkout=count_pedidos_checkout,
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

@mod.route('/cadastro-lojista', methods=['POST','GET'])
@LoginRequired.login_required
def cadastro_lojista():
    if request.method == "POST":
        user_found = repository.find_one('users', {'_id':ObjectId(session['_id'])})
        if user_found is not None:
            form_data = request.form.to_dict()
            repository.update_one('users', {'_id':ObjectId(session['_id'])}, form_data)
        return redirect(url_for('admin_routes.dashboard'))






# GERENCIAR MESAS
@mod.route('/mesas', methods=['POST', 'GET'])
@LoginRequired.login_required
def mesas():
    if request.method == "GET":
        # mesas_ordenadas = repository.find('mesas',{'_idUser': session['_id']})
        # for item in mesas_ordenadas:
        #     repository.update_one('mesas', {'_id': ObjectId(item['_id'])}, {'numero_mesa': 19})


        mesas_ordenadas = sorted(repository.find('mesas', {'_idUser': session['_id']}),
                                 key=lambda x: int(x['numero_mesa']))
        user_found = repository.find_one('users', {'_id': ObjectId(session['_id'])})
        return render_template('user/mesas.html', mesas=mesas_ordenadas,
                               max_mesas=10 if not 'max_mesas' in user_found else user_found['max_mesas'])
    if request.method == "POST":
        lista_mesas = request.form['numero_mesa'].split(',')
        for item in lista_mesas:
            mesa_found = repository.find_one('mesas',
                                             {'_idUser': session['_id'], 'numero_mesa': item})
            if mesa_found is None:
                new_Mesa = Mesa(item, session['_id'])
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

def json_encoder(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

# GERENCIAR CARDAPIO
@mod.route('/get-items', methods=['POST', 'GET'])
@LoginRequired.login_required
def get_items():
    if request.method == "GET":
        lista_cardapios = [item for item in repository.find('cardapios', {'_idUser': session['_id']})]
        items = []
        for item in lista_cardapios:
            item['_id'] = str(item['_id'])
            item['categoria'] = str(repository.find_one('categorias', {'_id': ObjectId(item['categoria']), '_idUser': session['_id']})['nome'])
            # item['valor'] =  "R$ " + locale.currency(float(item['valor'].replace(',','.')), grouping=True, symbol=True)[:-2]



            # if 'tipo_estoque' in item and item['tipo_estoque'] == 'Sim':
            #     item['tipo_estoque'] = f'{item["estoque_item"]} {item["estoque_metrica"]}'

            if 'tipo_estoque' in item and item['tipo_estoque'] != 'Sim':
                item['estoque_item'] = f'-'
                item['estoque_metrica'] = f'-'

            if 'tipo_estoque' not in item:
                item['estoque_item'] = f'-'
                item['estoque_metrica'] = f'-'



            if 'updated_at' in item:
                item['updated_at'] = item['updated_at'].strftime("%d-%m-%Y")
            if 'created_at' in item:
                item['created_at'] = str(item['created_at'].strftime("%Y-%m-%d"))
            items.append(item)
        return json.dumps(items, default=json_encoder)
    if request.method == "POST":




        return render_template('dashboard/modalItem.html',
                               metricas=metricas,
                               item= repository.find_one('cardapios', {"_id": ObjectId(request.form['_id'])}),
                               categorias = [item for item in repository.find('categorias', {'_idUser': session['_id']})]

                               )


@mod.route('/cardapio', methods=['POST', 'GET'])
@LoginRequired.login_required
def cardapio():
    if request.method == "GET":
        lista_cardapios = [item for item in repository.find('cardapios', {'_idUser': session['_id']})]
        lista_categorias = [item for item in repository.find('categorias', {'_idUser': session['_id']})]
        return render_template('user/cardapio.html', cardapios=lista_cardapios, categorias=lista_categorias, metricas=metricas)
    if request.method == "POST":
        try:
            form_data = request.form.to_dict()
            if '_id' in request.form:
                form_data.pop('_id', None)
                filename = 'comum.jpg'
                file = request.files.get('file')
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

                form_data.setdefault('filename', filename)
                repository.update_one('cardapios',{'_id': ObjectId(request.form['_id'])}, form_data)
                return jsonify({'msg': 'O Item foi atualizado com sucesso ', 'categoria': 'alert-success'})
            else:

                if request.form['nome_produto'] == '':
                    return jsonify({'erro': 'O nome do item precisa ser preenchido obrigatoriamente', 'categoria': 'alert-danger'})
                if request.form['descricao'] == '':
                    return jsonify(
                        {'erro': 'A descrição deve ser preenchida obrigatoriamente', 'categoria': 'alert-danger'})
                if 'categoria' not in request.form :
                    return jsonify(
                        {'erro': 'Uma categoria ser preenchida obrigatoriamente', 'categoria': 'alert-danger'})
                if request.form['valor'] == '':
                    return jsonify(
                        {'erro': 'Insira um valor de venda obrigatoriamente', 'categoria': 'alert-danger'})
                if 'estoque_item' not in request.form:
                    form_data['estoque_item'] = 0
                if 'temperatura' not in request.form:
                    form_data.setdefault('temperatura', False)
                if 'nutricional' not in request.form:
                    form_data.setdefault('nutricional', False)
                if 'calorias' not in request.form:
                    form_data.setdefault('calorias', False)

                filename = 'comum.jpg'
                file = request.files.get('file')
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))


                form_data.setdefault('filename', filename)
                form_data.setdefault('_idUser', session['_id'])
                new_cardapio = Cardapio(form_data)
                repository.create(new_cardapio)
                return jsonify({'msg':'OK', 'categoria':'alert-success'})
        except Exception as e:
            flash('Ocorreu um erro ao processar a requisição. Detalhes: {}'.format(str(e)))
            return jsonify({'erro':e , 'categoria': 'alert-danger'})




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


@mod.route('/delete_cardapio', methods=['POST', 'GET'])
@LoginRequired.login_required
def delete_cardapio():
    if request.method == "POST":
        repository.delete_one('cardapios', {"_id": ObjectId(request.form['_id'])})

        return jsonify({'msg': f'item excluído com sucesso', 'categoria': 'alert-success'})


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
                if cardapio is not None:
                    valor_total += int(pedido['quantidade']) * float( remove_currency_format (cardapio['valor']))

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
    if request.method == "POST":
        _idComanda = request.form['_idComanda']
        repository.update_one('comandas', {'_id': ObjectId(_idComanda)}, {'status': 'Aceito'})
        return jsonify({'success':'OK'})
@mod.route('/rejeitar_pedidos', methods=['POST'])
@LoginRequired.login_required
def rejeitar_pedidos():
    if request.method == "POST":
        _idComanda = request.form['_idComanda']
        repository.update_one('comandas', {'_id': ObjectId(_idComanda)}, {'status': 'Rejeitado'})
        return jsonify({'success': 'OK'})


@mod.route('/entregar_pedidos', methods=['POST', 'GET'])
@LoginRequired.login_required
def entregar_pedidos():
    if request.method == "POST":
        repository.update_one('comandas', {'_id': ObjectId(request.form['_idComanda'])}, {'status': 'Entregue'})
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




#templates
@mod.route('/pedido_componente/<_id>', methods=['POST', 'GET'])
@LoginRequired.login_required
def pedido_componente(_id):
    if request.method == "GET":

            return render_template('dashboard/pedido_componente.html', _id=_id)





