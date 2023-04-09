class Mesa:
    def __init__(self, form, _id):
        self.collection_name = 'mesas'
        self.numero_mesa =form['numero_mesa']
        self._idUser = _id
        self.status = False

    def to_dict(self):
        return self.__dict__