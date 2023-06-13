from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.clock import Clock

Clock.max_iteration = 60

Builder.load_file('./HomeView/homeview.kv')
class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
class HomeView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._window = Window



