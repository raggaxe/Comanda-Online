
from flask import Blueprint, render_template, request, redirect, url_for, make_response, jsonify,session
from Repository.BaseRepository import BaseRepository
from Configs.MongoConfig import MongoConfig
from bson.objectid import ObjectId
from Services import LoginRequired

mod = Blueprint('settings_routes', __name__)
repository = BaseRepository(MongoConfig().get_connect())

@mod.route('/settings', methods=['GET', 'POST'])
@LoginRequired.login_required
def settings():
    if request.method == "GET":
        id_user = ObjectId(session['_id'])
        user_found = repository.find_one('users', {'_id': id_user})
        if user_found is not None:
            empresa = repository.find_one('empresas', {'_idUser': session['_id']})
            if empresa is not None:
                return render_template('menu/settings.html', empresa=empresa)
            else:
                return render_template('user/cadastro.html')
    return redirect(url_for('index_routes.index'))