from datetime import datetime


class Cardapio:
    def __init__(self, form):
        self.collection_name = 'cardapios'
        self.nome_produto = form['nome_produto']
        self.filename=form['filename']
        self.descricao = form['descricao']
        self.categoria = form['categoria']
        self.tipo_preco = form['tipo_preco']
        self.valor =form['valor']
        self.tipo_estoque = form['tipo_estoque']
        self.estoque_item = form['estoque_item']
        self.estoque_metrica = form['estoque_metrica']

        self.temperatura=form['temperatura']
        self.nutricional =form['nutricional']


        self._idUser = form['_idUser']


        self.calorias = form['calorias']
        self.quilojoules = form['quilojoules']

        # self.tempo_estimado =form['tempo']
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.status = True

    def to_dict(self):
        return self.__dict__