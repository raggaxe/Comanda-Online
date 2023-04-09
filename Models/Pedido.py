from datetime import datetime
class Pedido:
    def __init__(self, form):
        self.collection_name = 'pedidos'
        self._idComanda =form['_idComanda']
        self._idCardapio =form['_idCardapio']
        self._idUser =form['_idUser']
        self.quantidade =form['quantidade']
        self.tempo_espera =''
        self.created_at = datetime.now()
        self.status = True

    def to_dict(self):
        return self.__dict__