from flask import Flask, session, Markup, Response, flash
from flask import Blueprint, render_template, request, redirect, send_file, make_response, jsonify
from flask_dance.contrib.facebook import facebook
from Models.User import Usuario
from Configs.MongoConfig import MongoConfig
from Services import Session
from Repository.BaseRepository import BaseRepository

mod = Blueprint('index_routes', __name__)
repository = BaseRepository(MongoConfig().get_connect())

@mod.route('/', methods=['GET', 'POST'])
def index():
    # if not 'logged_in' in session and facebook.authorized:
    #     resp = facebook.get("/me?fields=id,name,email,first_name,middle_name,last_name")
    #     user_info = resp.json()
    #     user_found = repository.find_one('users', {'email': user_info['email']})
    #
    #     if user_found:
    #         Session.set_session(user_found)
    #     else:
    #         user = User(user_info, user_from='facebook')
    #         new_user = repository.create(user)
    #         Session.set_session(user_found)
    #
    # RECAPTCHA_PUBLIC_KEY = '6Ldbc2IaAAAAAIXz8v1j1sc750ChDtJHJyM0jDlL'

    return render_template('shared/index.html')




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
