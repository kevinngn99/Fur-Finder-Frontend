from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button, ButtonBehavior
from card_view import Card
from custom_carousel import CustomCarousel
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


class Carousel(CustomCarousel, ButtonBehavior):
    pass


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
                    self._rect = RoundedRectangle(size_hint=self.size_hint, size=self.size, radius=(dp(25), dp(25), dp(25), dp(25)))

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
        class Card(Image):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                with self.canvas.before:
                    Color(rgb=get_color_from_hex('#FFB2D1'))
                    self._rect = RoundedRectangle(size_hint=self.size_hint, size=self.size, radius=(dp(15), dp(15), dp(15), dp(15)))

            def pos_callback(self, instance, value):
                self._rect.pos = value

        class SmallButton(AnchorLayout):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                with self.canvas.before:
                    Color(rgb=get_color_from_hex('#150470'))
                    self._rect = RoundedRectangle(size_hint=self.size_hint, size=self.size, radius=(dp(10), dp(10), dp(10), dp(10)))

            def pos_callback(self, instance, value):
                self._rect.pos = value

        def create(self):
            anchor_layout = AnchorLayout(size_hint=(1, None), height=dp(238), anchor_x='center', anchor_y='top')

            card = self.Card(source='images/hearts.png', allow_stretch=True, size_hint=(None, None), size=(dp(321), dp(200)))
            card.bind(pos=card.pos_callback)

            text_layout = AnchorLayout(size_hint=(None, None), size=(dp(321), dp(200)), anchor_x='center', anchor_y='center')
            text = Label(padding=(dp(20), dp(20)), halign='left', valign='top', text='[color=150470][size='+str(int(dp(22)))+'][font=assets/Inter-SemiBold.ttf]Reunited Animals\n'+'[color=150470][size='+str(int(dp(16)))+'][font=assets/Inter-Regular.ttf]View animals that have been reunited with their owners', markup=True)
            text.bind(size=text.setter('text_size'))
            text_layout.add_widget(text)

            button_layout = AnchorLayout(size_hint=(None, None), size=(dp(321), dp(200)), padding=dp(20), anchor_x='left', anchor_y='bottom')
            button = self.SmallButton(size_hint=(None, None), size=(dp(140), dp(45)))
            button.bind(pos=button.pos_callback)
            view = Label(halign='center', valign='center', text='[color=FFFFFF][size='+str(int(dp(16)))+'][font=assets/Inter-SemiBold.ttf]View', markup=True)
            view.bind(size=view.setter('text_size'))
            button.add_widget(view)
            button_layout.add_widget(button)

            image = AnchorLayout(size_hint=(None, None), size=(dp(321), dp(238)), anchor_x='right', anchor_y='bottom')
            image.add_widget(Image(source='images/featured.png', allow_stretch=True, size_hint=(None, None), size=(dp(151), dp(136))))

            anchor_layout.add_widget(card)
            anchor_layout.add_widget(text_layout)
            anchor_layout.add_widget(button_layout)
            anchor_layout.add_widget(image)
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

    def press_callback(self):
        print('carousel touched')

    def create(self):
        box_layout = BoxLayout(orientation='vertical', spacing=dp(30))

        scroll_view = ScrollView(do_scroll_x=False, size_hint=(1, 1))
        grid_layout = GridLayout(cols=1, size_hint=(1, None), spacing=dp(0))
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        grid_layout.add_widget(Button(text='Featured', size_hint=(1, None), height=dp(40)))
        grid_layout.add_widget(self.Featured().create())
        carousel = Carousel(direction='right', size_hint=(1, None), height=dp(200))
        carousel.on_press = lambda: self.press_callback()
        for i in range(10):
            card = Card('Waffles', 'Male', 'images/corgi.jpg', 'Corgi', 'Gold', 'Lost').build()
            carousel.add_widget(card)
        grid_layout.add_widget(Button(text='Recent', size_hint=(1, None), height=dp(40)))
        carousel_layout = AnchorLayout(size_hint=(1, None), height=dp(200))
        carousel_layout.add_widget(carousel)
        grid_layout.add_widget(carousel_layout)
        for i in range(10):
            grid_layout.add_widget(Button(text='Button', size_hint=(1, None), height=dp(40)))
        scroll_view.add_widget(grid_layout)

        box_layout.add_widget(self.Header().create())
        box_layout.add_widget(self.Person().create())
        box_layout.add_widget(scroll_view)

        profile = self.Profile(source='images/me.jpg')
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
