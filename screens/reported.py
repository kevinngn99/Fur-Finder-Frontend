from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp, sp


class Reported:
    class CustomScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def listen(self, data):
            print(data)

            btn = Button(text=str(data), size_hint=(1, None), height=dp(40))
            self.children[0].children[0].children[0].add_widget(btn)

    class Header:
        def create(self):
            anchor_layout = AnchorLayout(size_hint=(1, 0.1), anchor_x='left', anchor_y='top', padding=(dp(20), dp(20), dp(0), dp(0)))

            header = Label(halign='left', valign='top', font_size=sp(20), color=get_color_from_hex('#023b80'), text='[font=assets/Inter-SemiBold.ttf]Reported Pets', markup=True)
            header.bind(size=header.setter('text_size'))

            anchor_layout.add_widget(header)
            return anchor_layout

    class ScrollView:
        def create(self):
            grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
            grid_layout.bind(minimum_height=grid_layout.setter('height'))

            scroll_view = ScrollView(size_hint=(1, 0.9))
            scroll_view.add_widget(grid_layout)
            return scroll_view

    def create(self):
        box_layout = BoxLayout(orientation='vertical')

        header = self.Header().create()
        scroll_view = self.ScrollView().create()

        box_layout.add_widget(header)
        box_layout.add_widget(scroll_view)

        reported_screen = self.CustomScreen(name='Reported')
        reported_screen.add_widget(box_layout)

        return reported_screen
