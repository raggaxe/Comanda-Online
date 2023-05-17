from passlib.handlers.sha2_crypt import sha256_crypt

from Services.GerarOTP import generateOTP


class Usuario:
    def __init__(self, form):
        self.collection_name = 'users'
        self.email = form['email']
        self.senha = sha256_crypt.hash(str(form['password']))
        self.token = generateOTP()
        self.max_mesas = 20
        self.status = True

        # INFORMACOES DA LOJA
        self.CNPJ = ''
        self.tipo_empresa = ''
        self.razao_social = ''
        self.modelo_negocio = ''

        self.nome_comercial = ''
        self.telefone_comercial = ''
        self.detalhes_comercial = ''

        # ENDERECO LOJA
        self.CEP = ''
        self.cidade = ''
        self.estado = ''
        self.bairro = ''
        self.endereco = ''
        self.numero = ''
        self.complemento = ''

        # RESPONSAVEL LOJA
        self.nome_responsavel = ''
        self.cpf_responsavel = ''
        self.email_responsavel = ''

        # PLANO SELECIONADO LOJA
        self.plano = ''

        # DADOS BANCARIOS
        self.tipo_banco = ''
        self.banco = ''
        self.agencia = ''
        self.conta = ''
        self.digito = ''

    def to_dict(self):
        return self.__dict__

    def check_re_password(self, form):
        return form['password'] == form['Rpassword']







