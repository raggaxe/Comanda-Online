from bson import ObjectId
from flask import Flask, session, Markup, Response, flash, url_for
from flask import Blueprint, render_template, request, redirect, send_file, make_response, jsonify
from flask_dance.contrib.facebook import facebook
from Models.User import Usuario
from Configs.MongoConfig import MongoConfig
from Services import Session
from Repository.BaseRepository import BaseRepository

mod = Blueprint('index_routes', __name__)
repository = BaseRepository(MongoConfig().get_connect())
import locale

# Define a localização padrão para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.utf-8')

@mod.route('/', methods=['GET', 'POST'])
def index():
    # estabelecimentos = repository.find('users',{})
    # lista_estabelecimentos = []
    # for item in  estabelecimentos:
    #     item['_id'] = str(item['_id'])  # Converte o ObjectId em uma string
    #     lista_estabelecimentos.append(item)
    if 'logged_in' in session:
        return redirect(url_for('user_routes.dashboardCliente'))
    return render_template('shared/index.html')


@mod.route('/loja/<_id>')
def loja(_id):
    loja_found = repository.find('users',{'_id': ObjectId(_id)})
    estabelecimento = []
    cardapios = []
    cardapio_found = repository.find('cardapios',{'_idUser': _id})
    categorias= repository.find('categorias',{'_idUser': _id})
    check = repository.find_one('favoritos', {'_idUser': _id , '_idCliente': session['_id']})
    for card in cardapio_found:
        card['_id'] = str(card['_id'])  # Converte o ObjectId em uma string
        cardapios.append(card)

    for item in loja_found:
        item['_id'] = str(item['_id'])  # Converte o ObjectId em uma string
        estabelecimento.append(item)
    return render_template('shared/loja.html', estabelecimento=estabelecimento,cardapios=cardapios,categorias=categorias,check=check)

@mod.route('/produto/<_id>')
def produto(_id):
    cardapio = []
    cardapio_found = repository.find_one('cardapios',{'_id':ObjectId(_id)})
    cardapio_found['_id'] = str(cardapio_found['_id'])  # Converte o ObjectId em uma string
    # cardapio_found['valor'] =  locale.currency(float(cardapio_found['valor']), grouping=True, symbol=None)
    return render_template('shared/produto.html', produto=cardapio_found)






@mod.route('/discordJosh',methods=['GET', 'POST'])
def josh():
    return render_template('controladores/joshGudwin.html')

@mod.route('/privacidade',methods=['GET', 'POST'])
def privacidade():
    return render_template('privacidade.html')

@mod.route('/termos',methods=['GET', 'POST'])
def termos():
    return render_template('termos.html')

@mod.route('/politicaDeConduta')
def politica_de_conduta():
    return render_template('politica_de_conduta.html')
