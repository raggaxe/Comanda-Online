class Favorito:
    def __init__(self, form):
        self.collection_name = 'favoritos'
        self._idUser = form['_idUser']
        self._idCliente = form['_idCliente']
        self.status = True

    def to_dict(self):
        return self.__dict__