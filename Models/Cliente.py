from datetime import datetime
from passlib.hash import sha256_crypt

from Services.GerarOTP import generateOTP


class Cliente:
    def __init__(self, form):
        self.collection_name = 'clientes'
        self.CPF =''
        self.nome =''
        self.senha = sha256_crypt.hash(str(form.password.data))
        self.email = form.email.data
        self.token = generateOTP()
        self.status = True
        self.created_at = datetime.now()

    def to_dict(self):
        return self.__dict__

    def check_re_password(self, form):
        return form.password.data == form.confirm_password.data