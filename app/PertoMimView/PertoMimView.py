
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.swiper import MDSwiperItem
from kivy.network.urlrequest import UrlRequest
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.button import MDIconButton
from kivy.properties import ObjectProperty
from kivy.lang import Builder


Builder.load_file('./PertoMimView/pertoview.kv')
class MenuHeader(MDBoxLayout):
    '''An instance of the class that will be added to the menu header.'''
    pass

from kivy.metrics import dp


class PertoMimView(MDScreen):
    cards = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._window = Window

    def on_pre_enter(self, *args):
        # Make a request to the API
        url = "http://localhost:8080/favoritos"
        req = UrlRequest(url, on_success=self.on_request_success)

    def on_request_success(self, req, result):
        # Process the response and display the data in the carousel

        self.ids.fav_cards.clear_widgets()
        for data in result:
            print(data)
            box = MDBoxLayout()
            box.orientation = "vertical"
            box.size_hint_x = None
            box.width = self.ids.fav_cards.width - 10
            image = Image(source='./assets/images/comum.jpg', size_hint=(None, None), size=(500, 300))
            box.add_widget(image)
            label = MDLabel(text=data['email'], halign="center")
            box.add_widget(label)

            card = MDCard(size_hint=(None, None), size=(500, 400))
            card.add_widget(box)

            self.ids.fav_cards.add_widget(card)