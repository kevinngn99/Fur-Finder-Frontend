from kivy.uix.anchorlayout import AnchorLayout
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp, sp


class Reported:
    class Header:
        def create(self):
            header = Label(size_hint=(1, 0.1), halign='left', valign='top', font_size=sp(20), color=get_color_from_hex('#023b80'), text='[font=assets/Inter-SemiBold.ttf]Reported Pets', markup=True)
            header.bind(size=header.setter('text_size'))
            return header

    def create(self):
        anchor_layout = AnchorLayout(anchor_x='left', anchor_y='top', padding=(dp(20), dp(20), dp(0), dp(0)))
        anchor_layout.add_widget(self.Header().create())

        reported_screen = Screen(name='Reported')
        reported_screen.add_widget(anchor_layout)

        return reported_screen
