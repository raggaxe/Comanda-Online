from datetime import datetime
class Comanda:
    def __init__(self, form):
        self.collection_name = 'comandas'
        self._idMesa =''
        self.tipo_pedido = ''
        self._idCliente =form['_idCliente']
        self._idUser =form['_idUser']
        self.tipo_pagamento =''
        self.hora_abertura = datetime.now()
        self.hora_fechamento= ''
        self.valor=''
        self.status = 'aberta'

    def to_dict(self):
        return self.__dict__