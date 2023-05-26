from datetime import datetime
class Comanda:
    def __init__(self, form):
        self.collection_name = 'comandas'
        self._idMesa =''

        self._idCliente =form['_idCliente']
        self._idUser =form['_idUser']
        self.tipo_pagamento =''
        self.hora_abertura = datetime.now()
        self.hora_fechamento= ''
        self.valor=''
        self.status = form['status']
        self.tipo_atendimento = ''
        self.gorjeta = ''
        self.tx_entrega = ''


    def to_dict(self):
        return self.__dict__