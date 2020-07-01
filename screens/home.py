from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
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
from kivy.uix.textinput import TextInput
from kivy.metrics import dp, sp
from kivy.uix.widget import Widget
import requests
import json


class CustomScrollView(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._lock_h = False
        self._lock_v = False

    def on_touch_up(self, touch):
        self._lock_h = False
        self._lock_v = False
        return super(CustomScrollView, self).on_touch_up(touch)

    def on_touch_move(self, touch):
        x, y = self.children[0].to_widget(*self.to_window(*touch.pos))

        if not self.children[0].children[len(self.children[0].children) - 4].collide_point(x, y):
            return super(CustomScrollView, self).on_touch_move(touch)
        else:
            if abs(touch.dx) > abs(touch.dy) and not self._lock_h:
                touch.pos = (x, y)
                self._lock_v = True
                return self.children[0].children[len(self.children[0].children) - 4].on_touch_down(touch)
            elif abs(touch.dy) > abs(touch.dx) and not self._lock_v:
                self._lock_h = True
                return super(CustomScrollView, self).on_touch_move(touch)
            else:
                if not self._lock_v:
                    return super(CustomScrollView, self).on_touch_move(touch)
                elif not self._lock_h:
                    touch.pos = (x, y)
                    return self.children[0].children[len(self.children[0].children) - 4].on_touch_down(touch)

    def on_touch_down(self, touch):
        return super(CustomScrollView, self).on_touch_down(touch)

class Home:
    class Profile(Image):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.rect = None

        def create(self):
            with self.canvas.before:
                stencil_instructions.StencilPush()
                self.rect = RoundedRectangle(pos=self.pos, size_hint=(None, None), size=(dp(54), dp(54)), radius=(dp(27), dp(27), dp(27), dp(27)))
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
                    self._rect = RoundedRectangle(size_hint=self.size_hint, size=self.size, radius=(dp(30), dp(30), dp(30), dp(30)))

            def pos_callback(self, instance, value):
                self._rect.pos = value

        def create(self):
            anchor_layout = AnchorLayout(size_hint=(1, None), height=dp(85), anchor_x='right', anchor_y='center', padding=(dp(35), dp(35), dp(35), dp(0)))

            border = self.Border(size_hint=(None, None), size=(dp(60), dp(60)))
            border.bind(pos=border.pos_callback)

            box_layout = BoxLayout(size_hint=(1, None), height=dp(60), orientation='vertical')
            name = Label(size_hint=(1, None), height=dp(36), halign='left', valign='center', font_size=sp(30), color=get_color_from_hex('#150470'), text='[font=assets/Inter-SemiBold.ttf]Hello, Kevin', markup=True)
            name.bind(size=name.setter('text_size'))
            location = Label(size_hint=(1, None), height=dp(24), halign='left', valign='center', color=get_color_from_hex('#150470'), text='[size='+str(int(dp(24)))+'][font=assets/Feather.ttf]'+'[size='+str(int(dp(18)))+'][font=assets/Inter-Medium.ttf] Gainesville, FL', markup=True)
            location.bind(size=location.setter('text_size'))
            box_layout.add_widget(name)
            box_layout.add_widget(location)

            anchor_layout.add_widget(box_layout)
            anchor_layout.add_widget(border)
            return anchor_layout

    class Search:
        class Box(Widget):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                with self.canvas.before:
                    Color(rgb=get_color_from_hex('#F2F3FB'))
                    self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=(dp(15), dp(15), dp(15), dp(15)))

            def pos_callback(self, instance, value):
                self._rect.pos = value

            def size_callback(self, instance, value):
                self._rect.size = value

        # def on_focus(self, instance, value):
            # if value:
                # anim = Animation(x=self.parent.x, y=self.parent.y - (100*self._scale), duration=0.1)
                # anim.start(self.parent)
            # else:
                # anim = Animation(x=self.parent.x, y=self.parent.y + (100*self._scale), duration=0.1)
                # anim.start(self.parent)

        def create(self):
            anchor_layout = AnchorLayout(size_hint=(1, None), height=dp(60), anchor_x='center', anchor_y='center', padding=(dp(35), dp(0), dp(35), dp(0)))

            search = AnchorLayout(size_hint=(1, None), height=dp(60), anchor_x='center', anchor_y='center', padding=(dp(40), dp(0), dp(40), dp(0)))
            text_input = TextInput(size_hint=(1, None), height=dp(60), padding=(dp(8), dp(17), dp(0), dp(17)), background_active='', background_normal='',
                               cursor_color=(184 / 255, 179 / 255, 212 / 255, 1), cursor_width='2sp',
                               background_color=(242 / 255, 243 / 255, 251 / 255, 1),
                               selection_color=(184 / 255, 179 / 255, 212 / 255, 0.5),
                               foreground_color=(21 / 255, 4 / 255, 112 / 255, 1),
                               hint_text_color=(184 / 255, 179 / 255, 212 / 255, 1),
                               multiline=False,  hint_text='Search',
                               font_size=sp(20), font_name='assets/Inter-SemiBold.ttf')
            search.add_widget(text_input)

            icon = AnchorLayout(size_hint=(1, None), height=dp(60), anchor_x='center', anchor_y='center', padding=(dp(15), dp(0), dp(15), dp(0)))
            text = Label(size_hint=(1, None), height=dp(60), halign='left', valign='center', font_size=sp(24), color=get_color_from_hex('#150470'), text='[font=assets/Feather.ttf]', markup=True)
            text.bind(size=text.setter('text_size'))
            icon.add_widget(text)

            box = self.Box(size_hint=(1, None), height=dp(60))
            box.bind(pos=box.pos_callback)
            box.bind(size=box.size_callback)

            anchor_layout.add_widget(box)
            anchor_layout.add_widget(search)
            anchor_layout.add_widget(icon)
            return anchor_layout

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
        new_pos = (value[0] + dp(3), value[1] + dp(3))

        profile.pos = new_pos
        profile.rect.pos = new_pos
        anchor.pos = new_pos

    def create(self):
        box_layout = BoxLayout(orientation='vertical', spacing=dp(30))

        scroll_view = CustomScrollView(do_scroll_x=False, size_hint=(1, 1))
        grid_layout = GridLayout(cols=1, size_hint=(1, None), spacing=dp(30))
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        featured_text_layout = AnchorLayout(size_hint=(1, None), height=dp(30), anchor_x='center', anchor_y='center')
        featured_text = Label(padding=(dp(35), dp(0)), halign='left', valign='center', font_size=dp(30), text='[color=150470][font=assets/Inter-SemiBold.ttf]Featured', markup=True)
        featured_text.bind(size=featured_text.setter('text_size'))
        featured_text_layout.add_widget(featured_text)
        grid_layout.add_widget(featured_text_layout)
        grid_layout.add_widget(self.Featured().create())
        carousel = CustomCarousel(ignore_perpendicular_swipes=True, direction='right', size_hint=(1, None), height=dp(200))
        for i in range(2):
            card = Card('Waffles', 'Male', 'images/corgi.jpg', 'Corgi', 'Gold', 'Lost').build()
            carousel.add_widget(card)
        #data = json.loads(requests.get('https://fur-finder.herokuapp.com/api/pets/').text)
        #for dict in data[:10]:
            #card = Card(dict['name'], dict['gender'], dict['image'], dict['breed'], dict['color'], dict['date']).build()
            #carousel.add_widget(card)
        recent_text_layout = AnchorLayout(size_hint=(1, None), height=dp(30), anchor_x='center', anchor_y='center')
        recent_text = Label(padding=(dp(35), dp(0)), halign='left', valign='center', font_size=dp(30), text='[color=150470][font=assets/Inter-SemiBold.ttf]Recent', markup=True)
        recent_text.bind(size=recent_text.setter('text_size'))
        see_all_text = Label(padding=(dp(35), dp(0)), halign='right', valign='center', font_size=dp(18), text='[color=B9B7C1][font=assets/Inter-SemiBold.ttf]See All', markup=True)
        see_all_text.bind(size=see_all_text.setter('text_size'))
        recent_text_layout.add_widget(recent_text)
        recent_text_layout.add_widget(see_all_text)
        grid_layout.add_widget(recent_text_layout)
        carousel_layout = AnchorLayout(size_hint=(1, None), height=dp(200))
        carousel_layout.add_widget(carousel)
        grid_layout.add_widget(carousel_layout)
        for i in range(10):
            grid_layout.add_widget(Button(text='Button', size_hint=(1, None), height=dp(40)))
        scroll_view.add_widget(grid_layout)

        box_layout.add_widget(self.Header().create())
        box_layout.add_widget(self.Search().create())
        box_layout.add_widget(scroll_view)

        profile = self.Profile(source='images/me.jpg')
        if profile.image_ratio < 1:
            profile.size_hint = (profile.image_ratio + 1, profile.image_ratio + 1)
        else:
            profile.size_hint = (profile.image_ratio, profile.image_ratio)
        profile.create()

        anchor_layout = AnchorLayout(size_hint=(None, None), anchor_x='center', anchor_y='center', size=(dp(54), dp(54)))
        anchor_layout.add_widget(profile)
        box_layout.children[2].children[0].fbind('pos', self.update_pos, profile=profile, anchor=anchor_layout)

        home_screen = Screen(name='Home')
        home_screen.add_widget(box_layout)
        home_screen.add_widget(anchor_layout)

        return home_screen
