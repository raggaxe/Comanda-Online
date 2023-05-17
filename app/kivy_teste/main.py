from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager


#
#
#
# class Incrementador(BoxLayout):
#     pass
#
# class Menu(Screen):
#     pass
#
# class Tarefas(Screen):
#     def __int__(self, tarefas=[],**kwargs):
#         super(Tarefas, self).__int__()
#
#
# class Gerenciador(ScreenManager):
#     pass
#
#
# class Test(MDApp):
#     def build(self):
#         return Gerenciador()
#
# Test().run()

from app.kivy_teste.Main_screen.MainScreen import MainScreenView

class MainApp(MDApp):
    def __int__(self, **kwargs):
        super().__int__(**kwargs)
        self.sm = MDScreenManager()
    def build(self):
        self.sm.add_widget(MainScreenView)
        return self.sm

MainApp().run()
