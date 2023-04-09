class Categoria:
    def __init__(self, form , _id):
        self.collection_name = 'categorias'
        self.nome =form['nome']
        self._idUser = _id
        self.status = True

    def to_dict(self):
        return self.__dict__