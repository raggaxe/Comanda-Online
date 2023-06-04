
from flask import Blueprint, render_template, request, redirect, url_for, make_response, jsonify,session,current_app
from Repository.BaseRepository import BaseRepository
from Configs.MongoConfig import MongoConfig
from bson.objectid import ObjectId
from Services import LoginRequired
from werkzeug.utils import secure_filename
import os
mod = Blueprint('settings_routes', __name__)
repository = BaseRepository(MongoConfig().get_connect())

@mod.route('/settings', methods=['GET', 'POST'])
@LoginRequired.login_required
def settings():
    if request.method == "GET":
        id_user = ObjectId(session['_id'])
        user_found = repository.find_one('users', {'_id': id_user})
        if user_found is not None:
            return render_template('dashboard/settings/settings.html', empresa=user_found)
        return redirect(url_for('admin_routes.dashboard'))


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@mod.route('/cadastro-edit', methods=['POST','GET'])
@LoginRequired.login_required
def cadastro_edit():
    if request.method == "POST":

        user_found = repository.find_one('users', {'_id':ObjectId(session['_id'])})
        if user_found is not None:
            form_data = request.form.to_dict()
            filename = 'comum.jpg'
            file = request.files.get('file')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            print(filename)
            form_data.setdefault('filename', filename)

            repository.update_one('users', {'_id':ObjectId(session['_id'])}, form_data)
        return redirect(url_for('settings_routes.settings'))