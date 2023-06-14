class Mesa:
    def __init__(self, item, _id):
        self.collection_name = 'mesas'
        self.numero_mesa =item
        self._idUser = _id
        self.status = False

    def to_dict(self):
        return self.__dict__