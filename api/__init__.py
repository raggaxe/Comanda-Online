from flask import Flask
from flask_socketio import *
from dotenv import load_dotenv
from datetime import timedelta
from api.Controllers import AuthRoutes, ClientesRoutes
load_dotenv()
api= Flask(__name__)
load_dotenv()
api.secret_key = os.getenv("APP_SECRET_KEY")
api.config['SECRET_KEY'] = os.getenv("APP_SECRET_KEY")
api.config['SESSION_COOKIE_NAME'] = 'google-login-session'
api.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=500)
blueprints = [
    AuthRoutes.mod,
    ClientesRoutes.mod,
]
for bp in blueprints:
    api.register_blueprint(bp)

if __name__ == '__main__':
    api.run(port=8080,
                 debug=True)
