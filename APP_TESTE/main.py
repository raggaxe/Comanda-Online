from kivy.lang import Builder
from kivy.properties import ObjectProperty

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.snackbar import Snackbar

KV = '''

'''

class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class LoginScreen(MDScreen):
    pass


from kivy.uix.screenmanager import ScreenManager, Screen

class RootWidget(ScreenManager):
    pass

class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"

        # Definindo o atributo theme_cls para as instâncias de MDScreen
        LoginScreen.theme_cls = self.theme_cls

        # Carregando a tela de login
        login_screen = Builder.load_file('login.kv')
        self.root.add_widget(login_screen)

        # Carregando a tela de registro
        register_screen = Builder.load_file('cadastro.kv')
        self.root.add_widget(register_screen)

        return RootWidget()


    def login(self):
        email = self.root.ids.email_field.text
        password = self.root.ids.password_field.text

        # Aqui, você pode adicionar a lógica de verificação de email e senha
        # Se o login for bem-sucedido, navegue para a tela inicial
        self.root.current = "home"

    def register(self):
        email = self.root.ids.email_field.text
        password = self.root.ids.password_field.text

        # Aqui, você pode adicionar a lógica de verificação de email e senha
        # Se o registro for bem-sucedido, navegue para a tela de login
        self.root.current = "login"

MyApp().run()



