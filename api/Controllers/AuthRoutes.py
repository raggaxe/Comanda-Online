import json

from flask import Blueprint, render_template, request, redirect, send_file, make_response, jsonify
from Repository.BaseRepository import BaseRepository
from Configs.MongoConfig import MongoConfig
from bson import json_util
import json
from Services.GerarOTP import generateOTP


mod = Blueprint('auth_routes', __name__)
repository = BaseRepository(MongoConfig().get_connect())



@mod.route('/login', methods=['POST'])
def login():
    data = request.json
    nome = data.get('nome')
    cpf_raw = data.get('CPF')
    cpf_formatted = cpf_raw[:3] + '.' + cpf_raw[3:6] + '.' + cpf_raw[6:9] + '-' + cpf_raw[9:]
    print()
    user_found = repository.find_one('clientes', {'CPF': str(cpf_formatted) })
    # Verifica se as credenciais estão corretas
    if user_found is not None:
        # Converte o objeto ObjectId para uma string
        user_found['_id'] = str(user_found['_id'])
        # Se as credenciais estiverem corretas, retorna um token de autenticação
        return json.loads(json_util.dumps(user_found))
    else:
        # Se as credenciais estiverem incorretas, retorna uma mensagem de erro
        return {'error': 'Credenciais inválidas'}, 401
