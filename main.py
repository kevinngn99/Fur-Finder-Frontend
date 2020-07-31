from kivy.config import Config

Config.set('graphics', 'width', '432')
Config.set('graphics', 'height', '768')
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'multisamples', '5')

from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from navigation import Navigation
from screen_manager import Screens
from kivy.uix.screenmanager import Screen, ScreenManager
from screens.login import Login
from screens.register import Register


class MyClass(MDApp):
    class CustomBoxLayout(BoxLayout):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            with self.canvas:
                Color(rgb=get_color_from_hex('#f6f7fb'))
                self._rect = Rectangle(size_hint=(None, None))

        def size_callback(self, instance, value):
            self._rect.size = value

    def build(self):
        sm = ScreenManager()

        box_layout = self.CustomBoxLayout(orientation='vertical')
        box_layout.fbind('size', box_layout.size_callback)

        screens = Screens().create()
        navigation = Navigation(screens).create()
        register_screen = Register().create()
        login_screen = Login(sm, screens, screens.get_screen('Message')).create()

        box_layout.add_widget(screens)
        box_layout.add_widget(navigation)

        app = Screen(name='App')
        app.add_widget(box_layout)

        sm.add_widget(login_screen)
        sm.add_widget(register_screen)
        sm.add_widget(app)

        return sm

    def on_start(self):
        print('APP LOADED')


if __name__ == '__main__':
    MyClass().run()
