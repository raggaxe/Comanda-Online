from Services.GerarOTP import generateOTP


class Usuario:
    def __init__(self, form):
        self.collection_name = 'users'
        self.email = form['email']
        self.token = generateOTP()
        self.max_mesas = 20
        self.status = True
    def to_dict(self):
        return self.__dict__




