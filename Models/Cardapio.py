class Cardapio:
    def __init__(self, form,filename,estoque,categoria,_id):
        self.collection_name = 'cardapios'
        self.filename=filename
        self.nome_produto =form['nome']
        self.valor =form['valor']
        self._idUser = _id
        self.estoque = estoque
        self.categoria = categoria
        self.tempo_estimado =form['tempo']
        self.status = True

    def to_dict(self):
        return self.__dict__