from kivy.properties import ListProperty
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.core.window import Window
import requests
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp

from mobile.HomeView.HomeView import HomeView
from mobile.MainWindow import MainWindowView
from kivy.uix.label import Label
from kivy.core.text import LabelBase

from mobile.PertoMimView.PertoMimView import PertoMimView

LabelBase.register(name='Montserrat',
                   fn_regular='assets/fonts/Montserrat/Montserrat-Regular.ttf',
                   fn_bold='assets/fonts/Montserrat/Montserrat-Bold.ttf')

# class CreateAccountWindow(Screen):
#     namee = ObjectProperty(None)
#     email = ObjectProperty(None)
#     password = ObjectProperty(None)
#
#     def submit(self):
#         if self.namee.text != "" and self.email.text != "" and self.email.text.count(
#                 "@") == 1 and self.email.text.count(".") > 0:
#             if self.password != "":
#
#                 self.reset()
#
#                 sm.current = "login"
#             else:
#                 invalidForm()
#         else:
#             invalidForm()
#
#     def login(self):
#         self.reset()
#         sm.current = "login"
#
#     def reset(self):
#         self.email.text = ""
#         self.password.text = ""
#         self.namee.text = ""

class LoginWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        pass

    def reset(self):
        self.username_input.text = ""
        self.CPF_input.text = ""

    def on_login_button_press(self, instance):
        nome = self.username_input.text
        cpf = self.CPF_input.text
        url = 'http://localhost:8080/login'
        # Define os dados da requisição POST
        data = {'nome': nome, 'CPF': cpf}
        # Envia a requisição POST para a API
        response = requests.post(url, json=data)
        # Verifica se a resposta da API foi bem sucedida
        if response.ok:
            # Se as credenciais estiverem corretas, mostra uma mensagem de sucesso
            MainWindowView.current = self.CPF_input.text
            response_json = response.json()
            self.store.put('user_id', id=response_json['_id'])
            self.reset()
            if response_json['_id']:
                self.manager.set_user_id(response_json['_id'])  # define o user_id no WindowManager
                self.manager.current = 'main'
        else:
            # Se as credenciais estiverem incorretas, mostra uma mensagem de erro
            self.error_label.text = 'Nome de usuário ou senha inválidos.'
            invalidLogin()


def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()

def invalidForm():
    pop = Popup(title='Invalid Form',
                content=Label(text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()

class WindowManager(ScreenManager):
    pass

class MyMainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = WindowManager()
        self.user_id = None
    def build(self):
        self.theme_cls.material_style = 'M3'
        self.theme_cls.theme_style= 'Light'
        self.theme_cls.primary_palette = 'Brown'
        Window.size = (dp(360), dp(600))
        Window.minimum_width = 360
        Window.minimum_height = 600
        screens = [
            LoginWindow(name="login"),
            HomeView(name="HomeView"),
            PertoMimView(name="PertoMim"),
            # CreateAccountWindow(name="create"),
            MainWindowView(name="main")
        ]
        for screen in screens:
            self.sm.add_widget(screen)
        # define the store attribute here
        self.store = JsonStore('user_session.json')
        if 'user_id' in self.store:
            # passa os dados para a classe CardListView
            self.cards = ListProperty([])  # Definição do atributo cards
            self.sm.current = 'main'
        else:
            self.sm.current = 'login'
        return self.sm

    def on_resize(self, window, width, height):
        self.rect.size = Window.size
if __name__ == "__main__":
    MyMainApp().run()

