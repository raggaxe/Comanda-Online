class Cliente:
    def __init__(self, form):
        self.collection_name = 'clientes'
        self.CPF =form['CPF']
        self.nome =form['nome']
        self._idUser=form['estabelecimento']
        self.status = True

    def to_dict(self):
        return self.__dict__