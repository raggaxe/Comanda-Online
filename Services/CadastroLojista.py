from Repository.BaseRepository import BaseRepository
from Configs.MongoConfig import MongoConfig
from bson.objectid import ObjectId
from werkzeug.datastructures import ImmutableMultiDict
repository = BaseRepository(MongoConfig().get_connect())

def CadastroLogista(form, _idUser):
    user_form= repository.find_one('users',{'_id': ObjectId(_idUser) })
    if user_form is not None:
        return repository.update_one('users',{'_id': user_form['_id']},form.to_dict())
