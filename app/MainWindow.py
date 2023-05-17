import json
import requests
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore
from kivy.app import App
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView

from kivy.lang import Builder
import geocoder
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

Builder.load_file('mainwindow.kv')
Builder.load_file('card.kv')
from kivy.properties import StringProperty

from kivymd.uix.card import MDCard


class Card(MDCard):
    source = StringProperty()
    text = StringProperty()
# class CardWidget(BoxLayout):
#     image_source = StringProperty()
#     nome = StringProperty()
#     description = StringProperty()
#
#     def view_details(self):
#         print(f"Viewing details of {self.nome}")
#
#
# class CardListView(RecycleView):
#     cards = ListProperty([])
#
#     def __init__(self, **kwargs):
#         super(CardListView, self).__init__(**kwargs)
#         # rest of the code
#
#
#         # Define o layout dos cards
#         self.viewclass = 'CardWidget'
#         self.orientation = 'vertical'
#         self.spacing = 10
#         self.padding = 10
#
#         # Define o tipo de layout do RecycleView
#         self.layout = RecycleBoxLayout(
#             spacing=self.spacing,
#             size_hint_y=None,
#             height=self.height,
#             orientation='vertical'
#         )
#         self.add_widget(self.layout)
#
#         # Atualiza a altura do layout do RecycleView quando o tamanho da janela muda
#         self.bind(height=self.update_height)
#
#
#     def update_height(self, instance, height):
#         self.layout.height = height
#
#     def add_cards(self, cards):
#         for card in cards:
#             card_widget = CardWidget(nome=str(card['email']), description=str(card['max_mesas']),
#                                      image_source=str(card['status']))
#             self.ids.card_list_view.add_widget(card_widget)

class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
    nome = StringProperty('')




    def getUser(self, **kwargs):
        self.store = JsonStore('user_session.json')
        if 'user_id' in self.store:
            url = 'http://localhost:8080/clientes'
            data = {'_id': self.store['user_id']['id']}
            response = requests.post(url, json=data)
            response_json = response.json()
            nome = response_json.get('nome', '')
            return nome
        return ''


class CustomMDScreen(Screen):
    pass

is_open = False
class MainWindowView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def on_drawer_status(self, instance, value):

        if value == 'closing_with_animation':
            icon_menu = self.ids.icon_menu
            icon_menu.icon = 'menu'



    def managerIcon(self, icon ):
        new_icon = ''
        if icon == 'menu':
            new_icon= 'arrow-left'
        if icon == 'arrow-left':
            new_icon = 'menu'
        return new_icon

    def on_enter(self, *args):
        try:
            self.store = JsonStore('user_session.json')
            if 'user_id' in self.store:
                url = 'http://localhost:8080/clientes'
                data = {'_id': self.store['user_id']['id']}
                response = requests.post(url, json=data)
                response_json = response.json()
                # self.ids.user_label.text = response_json['nome']

                # self.n.text = "Account Name: " + response_json['nome']
                # self.email.text = "CPF: " + response_json['CPF']
                # converte a data do formato UTC para o formato local
                created_at = response_json.get('created_at')

                # if created_at:
                #     created_at_dt = parser.isoparse(created_at['$date'])
                #     created_at_str = created_at_dt.strftime('%Y-%m-%d %H:%M:%S')
                #     # self.created.text = "Created On: " + created_at_str
                # else:
                #     self.created.text = "Created On: N/A"






        except json.decoder.JSONDecodeError as e:
            print(f"Erro de decodificação JSON: {e}")
            return {'error': 'Erro de decodificação JSON'}, 500

    def logOut(self, *args):
        self.sm.current = "login"
