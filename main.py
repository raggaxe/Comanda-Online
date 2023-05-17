from bson import ObjectId
from flask import Flask, render_template, request, session, stream_with_context, Response
from flask_socketio import *
from dotenv import load_dotenv
from datetime import datetime, timedelta
import locale
from Configs.MongoConfig import MongoConfig
from Controllers import AdminRoutes, AuthRoutes, IndexRoutes, UserRoutes, SettingsRoutes, DefaultRoutes
from flask_dance.contrib.facebook import make_facebook_blueprint
from pymongo import MongoClient
from jinja2 import Environment, FileSystemLoader
from babel.numbers import format_currency

env = Environment(loader=FileSystemLoader('templates'))
env.filters['format_currency'] = format_currency
env.globals['getLocale'] = None

from Repository.BaseRepository import BaseRepository
repository = BaseRepository(MongoConfig().get_connect())
load_dotenv()
app = Flask(__name__)

# app settings
UPLOAD_FOLDER = './static/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

load_dotenv()
FACEBOOK_OAUTH_CLIENT_ID = os.getenv('FACEBOOK_OAUTH_CLIENT_ID')
FACEBOOK_OAUTH_CLIENT_SECRET = os.getenv('FACEBOOK_OAUTH_CLIENT_SECRET')

app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SECRET_KEY'] = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=500)


# Define a localidade para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.utf-8')


if os.getenv("APP_SETTINGS") == 'development':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

facebookbp = make_facebook_blueprint(
    client_id=FACEBOOK_OAUTH_CLIENT_ID,
    client_secret=FACEBOOK_OAUTH_CLIENT_SECRET,
    scope='email',
)

app.register_blueprint(facebookbp, url_prefix="/login")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.jinja_env.add_extension('jinja2.ext.do')

socketio = SocketIO(app, async_handlers=True)

blueprints = [
    AdminRoutes.mod,
    AuthRoutes.mod,
    IndexRoutes.mod,
    UserRoutes.mod,

    SettingsRoutes.mod,
]

for bp in blueprints:
    app.register_blueprint(bp)

app.errorhandler(400)(DefaultRoutes.errorhandler)
app.errorhandler(401)(DefaultRoutes.errorhandler)
app.errorhandler(403)(DefaultRoutes.errorhandler)
app.errorhandler(404)(DefaultRoutes.errorhandler)
app.errorhandler(500)(DefaultRoutes.errorhandler)

repository = BaseRepository(MongoConfig().get_connect())
@app.route('/discordJosh', methods=['GET', 'POST'])
def josh():
    return render_template('controladores/joshGudwin.html')


# users_in_room = {}
# rooms_sid = {}
# names_sid = {}
#



@socketio.on("connect-admin")
def on_connect():
    sid = request.sid
    # print("Admin Conecetado Browser sid: ",sid)
@socketio.on("join-room-admin")
def on_join_room(data):
    join_room(str(session["_id"]))

@socketio.on("connect")
def on_connect():
    sid = request.sid
    # print("New socket connected ", sid)

@socketio.on("join-room")
def on_join_room(data):
    _idComanda = data["_idComanda"]
    _idUser = data["_idUser"]
    # register sid to the room
    join_room(_idComanda)
    join_room(_idUser)

@socketio.on("join-room-pagamentos")
def on_join_room(data):
    _idComanda = data["_idComanda"]
    _idUser = data["_idUser"]
    # register sid to the room
    room_id = str(_idUser)+str(_idComanda)
    join_room(room_id)


@socketio.on("pedido-cliente-solicitado")
def on_pedido_cliente_solicitado(data, room):
    # faça o processamento desejado com os dados recebidos

    pedido = repository.find_one('pedidos', {'_id': ObjectId(data['_idPedido']) })
    cardapio = repository.find_one('cardapios', {'_id': ObjectId(data['_idCardapio']) })

    _idUser = data['_idUser']

    emit("pedido-cliente-solicitado", {
        "nome_produto": cardapio["nome_produto"],
        "created_at":str(pedido['created_at']),
        "_idCardapio": data["_idCardapio"],
        "quantidade": data["quantidade"],
        "_idPedido":str(pedido['_id']),

    }, room=_idUser)

@socketio.on('pedido-aceito')
def handle_pedido_aceito(data):
    _idPedido = data['_idPedido']
    pedido = repository.find_one('pedidos', {'_id': ObjectId(data['_idPedido'])})
    emit('pedido-aceito-confirmacao',
         {
             'tempo': str(pedido['updated_at']),
             'status': pedido['status'],
             '_idPedido':str(pedido['_id'])
         }, room=pedido['_idComanda']
         )


@socketio.on('pedido-entregue')
def handle_pedido_entregue(data):
    _idPedido = data['_idPedido']
    pedido = repository.find_one('pedidos', {'_id': ObjectId(data['_idPedido'])})
    emit('pedido-aceito-confirmacao',
         {
             'tempo': str(pedido['updated_at']),
             'status': pedido['status'],
             '_idPedido':str(pedido['_id'])
         }, room=pedido['_idComanda']
         )

@socketio.on('pedido-cliente-pagamento')
def handle_pedido_cliente_pagamento(data):
    id_comanda = data['_idComanda']
    comanda = repository.find_one('comandas', {'_id': ObjectId(id_comanda)})
    valor = data['valor']
    forma_pagamento = data['formaPagamento']
    # Envia mensagem para o admin sobre o pagamento
    emit('pedido-admin-pagamento', {'updated_at':str(comanda['updated_at']),'id_comanda': str(id_comanda), 'valor': valor, 'tipo_pagamento': forma_pagamento, '_idMesa':str(comanda['_idMesa'])},
         room=str(comanda['_idUser']))


@socketio.on('pagamento-realizado')
def handle_pagamento_realizado(data):
    comanda = repository.find_one('comandas', {'_id': ObjectId(data['_idComanda'])})
    room_id = str( comanda['_idUser'] ) + str( comanda['_id'] )
    emit("pagamento", {
        'room_id': room_id,
        'status': comanda['status']
    }, room=room_id)


@socketio.on('mesa-ocupada')
def handle_mesa_ocupada(data):
    _idMesa = data['_idMesa']
    repository.update_one('mesas',{'_id':ObjectId(_idMesa)},{'status':True})
    lista_mesas = [item for item in repository.find('mesas', {'_idUser': data['_idUser'], 'status': True})]
    print(f"Mesa {data['numero_mesa']} está ocupada agora.")
    num_mesas = len(lista_mesas)
    emit('update-mesas-ocupadas', {'num_mesas': num_mesas ,'_idMesa':_idMesa }, room=data['_idUser'] )



@app.context_processor
def my_utility_processor():

    def get_time_now():
        from datetime import datetime
        # datetime object containing current date and time
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        return dt_string

    def timerDisplay(secs):
        hours, remainder = divmod(int(secs), 3600)
        minutes, seconds = divmod(remainder, 60)
        return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

    def getCardapio(_idCardapio):
        cardapio = repository.find_one('cardapios', {'_id': ObjectId(_idCardapio)})
        return cardapio

    def getMesa(_idMesa):
        if _idMesa != '':
            Mesa = repository.find_one('mesas', {'_id': ObjectId(_idMesa)})
            return Mesa
        else:
            return _idMesa

    def getCliente(_idCliente):
        cliente = repository.find_one('clientes', {'_id': ObjectId(_idCliente)})
        return cliente

    def getCategoria(_idCategoria):
        categoria = repository.find_one('categorias', {'_id': ObjectId(_idCategoria)})
        return categoria

    def getEstabelecimento(_idUser):
        user = repository.find_one('users', {'_id': ObjectId(_idUser)})
        return user
    def MoneyFormatter(valor):
        return "R$ " +  locale.currency(valor, grouping=True, symbol=True)[:-2]

        # def format_datetime2(value, format='medium'):
        #     if format == 'full':
        #         format = "EEEE, d. MMMM y 'at' HH:mm"
        #     elif format == 'medium':
        #         format = "EE dd.MM.y HH:mm"
        #     return format_datetime(value, format,locale='pt_BR')

    return dict(get_time_now=get_time_now,
                timerDisplay=timerDisplay,
                getCardapio=getCardapio,
                getCliente=getCliente,
                getMesa=getMesa,
                getCategoria=getCategoria,
                MoneyFormatter=MoneyFormatter,
                getEstabelecimento=getEstabelecimento
                )

    # def format_datetime2(value, format='medium'):
    #     if format == 'full':
    #         format = "EEEE, d. MMMM y 'at' HH:mm"
    #     elif format == 'medium':
    #         format = "EE dd.MM.y HH:mm"
    #     return format_datetime(value, format,locale='pt_BR')


if __name__ == '__main__':
    socketio.run(app, port=5000,
                 debug=True)
