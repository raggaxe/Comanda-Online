import datetime

from flask import Blueprint,request,jsonify
from Repository.BaseRepository import BaseRepository
from Configs.MongoConfig import MongoConfig
from bson import json_util, ObjectId
import json
mod = Blueprint('clientes_routes', __name__)
repository = BaseRepository(MongoConfig().get_connect())



@mod.route('/clientes', methods=['POST'])
def clientes():
    data = request.json
    _idCliente = data.get('_id')

    user_found = repository.find_one('clientes', {'_id': ObjectId(_idCliente)})
    # Verifica se as credenciais estão corretas
    if user_found is not None:

        # Converte o objeto ObjectId para uma string
        user_found['_id'] = str(user_found['_id'])
        if 'created_at' not in user_found:
            user_found = repository.update_one('clientes', {'_id': ObjectId(_idCliente) },
                                               {'created_at': datetime.datetime.now()})
        # Se as credenciais estiverem corretas, retorna um token de autenticação
        return json.loads(json_util.dumps(user_found))
    else:
        # Se as credenciais estiverem incorretas, retorna uma mensagem de erro
        return {'error': 'Credenciais inválidas'}, 401


@mod.route('/favoritos', methods=['GET'])
def favoritos():
    print('Buscando Favoritos....')
    empresas = repository.find('users', {})
    # Verifica se as credenciais estão corretas
    if empresas is not None:
        empresas_list = []
        for empresa in empresas:
            empresa['_id'] = str(empresa['_id'])
            empresas_list.append(empresa)

        return jsonify(empresas_list)
    else:
        # Se as credenciais estiverem incorretas, retorna uma mensagem de erro
        return {'error': 'Credenciais inválidas'}, 401