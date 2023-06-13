
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.button import MDIconButton



class BottomMenu(MDBottomNavigation):
    def __init__(self, **kwargs):
        super(BottomMenu, self).__init__(**kwargs)
        # self.background_color = (1, 0, 0, 1)  # define a cor de fundo como vermelho
        # self.size_hint = (1, 1)
        # self.background_color = (0, 0, 1, 1)  # set background color to blue
        # # rest of your code
        #
        # account_item = MDBottomNavigationItem(name="account", text="Account", icon="account")
        # account_button = MDIconButton(icon="account-circle", theme_text_color="Custom",
        #                               text_color=(1, 1, 1, 1), font_size="50sp",
        #                               pos_hint={'center_x': 0.5, 'center_y': 0.5},
        #                               on_release=lambda x: print("Account pressed"))
        # account_item.md_bg_color =(0, 0, 1, 1)
        # account_item.add_widget(account_button)
        # self.add_widget(account_item)
        #
        # bell_item = MDBottomNavigationItem(name="bell", text="Bell", icon="bell")
        # bell_button = MDIconButton(icon="bell", theme_text_color="Custom",
        #                            text_color=(1, 1, 1, 1), font_size="50sp",
        #                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        #                            on_release=lambda x: print("Bell pressed"))
        # bell_item.add_widget(bell_button)
        # bell_item.md_bg_color = (2, 3, 4, 1)
        # self.add_widget(bell_item)
        #
        # message_item = MDBottomNavigationItem(name="message", text="Message", icon="message")
        # message_button = MDIconButton(icon="message-text", theme_text_color="Custom",
        #                               text_color=(1, 1, 1, 1), font_size="50sp",
        #                               pos_hint={'center_x': 0.5, 'center_y': 0.5},
        #                               on_release=lambda x: print("Message pressed"))
        # message_item.add_widget(message_button)
        # self.add_widget(message_item)
        #
        # settings_item = MDBottomNavigationItem(name="settings", text="Settings", icon="settings")
        # settings_button = MDIconButton(icon="cog-outline", theme_text_color="Custom",
        #                                text_color=(1, 1, 1, 1), font_size="50sp",
        #                                pos_hint={'center_x': 0.5, 'center_y': 0.5},
        #                                on_release=lambda x: print("Settings pressed"))
        # settings_item.add_widget(settings_button)
        # self.add_widget(settings_item)
        #
        # help_item = MDBottomNavigationItem(name="help", text="Help", icon="help")
        # help_button = MDIconButton(icon="help-circle-outline", theme_text_color="Custom",
        #                            text_color=(1, 1, 1, 1), font_size="50sp",
        #                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        #                            on_release=lambda x: print("Help pressed"))
        # help_item.add_widget(help_button)
        # self.add_widget(help_item)