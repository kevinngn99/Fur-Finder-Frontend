from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.graphics import stencil_instructions
from kivy.metrics import dp, sp
from kivy.uix.widget import Widget


class Home:
    class Profile(Image):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.rect = None

        def create(self):
            with self.canvas.before:
                stencil_instructions.StencilPush()
                self.rect = RoundedRectangle(pos=self.pos, size_hint=(None, None), size=(dp(50), dp(50)), radius=(dp(25), dp(25), dp(25), dp(25)))
                stencil_instructions.StencilUse()
            with self.canvas.after:
                stencil_instructions.StencilUnUse()
                stencil_instructions.StencilPop()

    class Header:
        class Border(Widget):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                with self.canvas.after:
                    Color(rgb=get_color_from_hex('#150470'))
                    self._rect = RoundedRectangle(pos=self.pos, size_hint=self.size_hint, size=self.size, radius=(dp(25), dp(25), dp(25), dp(25)))

            def pos_callback(self, instance, value):
                self._rect.pos = value

        def create(self):
            anchor_layout = AnchorLayout(size_hint=(1, None), height=dp(85), anchor_x='right', anchor_y='center', padding=(dp(35), dp(35), dp(35), dp(0)))
            header = Label(size_hint=(1, None), height=dp(50), halign='left', valign='center', font_size=sp(40), color=get_color_from_hex('#150470'), text='[font=assets/Inter-SemiBold.ttf]Home', markup=True)
            header.bind(size=header.setter('text_size'))
            border = self.Border(size_hint=(None, None), size=(dp(50), dp(50)))
            border.bind(pos=border.pos_callback)
            anchor_layout.add_widget(header)
            anchor_layout.add_widget(border)
            return anchor_layout

    class Person:
        def create(self):
            box_layout = BoxLayout(size_hint=(1, None), height=dp(60), orientation='vertical', padding=(dp(35), dp(0), dp(35), dp(0)))
            name = Label(size_hint=(1, None), height=dp(36), halign='left', valign='center', font_size=sp(30), color=get_color_from_hex('#150470'), text='[font=assets/Inter-SemiBold.ttf]Welcome, Kevin', markup=True)
            name.bind(size=name.setter('text_size'))
            location = Label(size_hint=(1, None), height=dp(24), halign='left', valign='center', color=get_color_from_hex('#150470'), text='[size='+str(int(dp(24)))+'][font=assets/Feather.ttf]'+'[size='+str(int(dp(18)))+'][font=assets/Inter-Medium.ttf] Gainesville, FL', markup=True)
            location.bind(size=location.setter('text_size'))
            box_layout.add_widget(name)
            box_layout.add_widget(location)
            return box_layout

    class Featured:
        def create(self):
            anchor_layout = AnchorLayout(size_hint=(1, None), height=dp(200), anchor_x='center', anchor_y='center')
            return anchor_layout

    def __init__(self, header=None, person=None, search=None, featured=None, recent=None):
        self._header = header
        self._person = person
        self._search = search
        self._featured = featured
        self._recent = recent

    def update_pos(self, instance, value, profile=None, anchor=None):
        profile.pos = value
        profile.rect.pos = value
        anchor.pos = value

    def create(self):
        box_layout = BoxLayout(orientation='vertical', spacing=30)

        scroll_view = ScrollView(size_hint=(1, 1))
        grid_layout = GridLayout(cols=1, size_hint=(1, None))
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        for i in range(50):
            grid_layout.add_widget(Button(text=str(i), size_hint_y=None, height=dp(40)))
        scroll_view.add_widget(grid_layout)

        box_layout.add_widget(self.Header().create())
        box_layout.add_widget(self.Person().create())
        box_layout.add_widget(scroll_view)

        profile = self.Profile(source='images/corgi.jpg')
        if profile.image_ratio < 1:
            profile.size_hint = (profile.image_ratio + 1, profile.image_ratio + 1)
        else:
            profile.size_hint = (profile.image_ratio, profile.image_ratio)
        profile.create()

        anchor_layout = AnchorLayout(size_hint=(None, None), anchor_x='center', anchor_y='center', size=(dp(50), dp(50)))
        anchor_layout.add_widget(profile)
        box_layout.children[2].children[0].fbind('pos', self.update_pos, profile=profile, anchor=anchor_layout)

        home_screen = Screen(name='Home')
        home_screen.add_widget(box_layout)
        home_screen.add_widget(anchor_layout)

        return home_screen
