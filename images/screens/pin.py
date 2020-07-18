from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp, sp


class Pin:
    class Header:
        def create(self):
            header = Label(size_hint=(1, None), height=dp(50), halign='left', valign='center', font_size=sp(40), color=get_color_from_hex('#150470'), text='[font=assets/Inter-SemiBold.ttf]Pinned', markup=True)
            header.bind(size=header.setter('text_size'))
            return header

    def __init__(self):
        self._other = None

    def create(self):
        box_layout = BoxLayout(orientation='vertical', spacing=dp(30), padding=(dp(35), dp(35), dp(35), dp(35)))

        box_layout.add_widget(self.Header().create())
        box_layout.add_widget(Label(font_size=sp(40), color=get_color_from_hex('#150470'), text='[font=assets/Inter-SemiBold.ttf]', markup=True))

        pin_screen = Screen(name='Pin')
        pin_screen.add_widget(box_layout)

        return pin_screen
