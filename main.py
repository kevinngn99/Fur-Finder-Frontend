import kivy
kivy.require('1.11.1')

from kivy.config import Config

Config.set('graphics', 'width', '375')
Config.set('graphics', 'height', '812')
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'multisamples', '5')

from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.animation import Animation
from kivy.metrics import dp
from custom_carousel import CustomCarousel
from card_view import Card
import requests
import json
from jnius import cast
from jnius import autoclass
from navigation import Navigation
from screen_manager import Screens


class ImageButton(ButtonBehavior, Image):
    pass


class SearchBox(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rect = None
        self._scale = None

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale

    def prepare(self):
        with self.canvas.before:
            Color(rgb=get_color_from_hex('#F2F3FB'))
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15*self._scale])


class Search(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._scale = None

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale

    def on_focus(self, instance, value):
        if value:
            anim = Animation(x=self.parent.x, y=self.parent.y - (100*self._scale), duration=0.1)
            anim.start(self.parent)
        else:
            anim = Animation(x=self.parent.x, y=self.parent.y + (100*self._scale), duration=0.1)
            anim.start(self.parent)


class MyApp(App):
    def callback_pos(self, instance, value):
        instance.rect.pos = value

    #def tab(self):
        #anchor_layout = AnchorLayout(anchor_x='center', anchor_y='bottom')
        #carousel = CustomCarousel(direction='right', pos=(0, 100), size=(375, 200), size_hint=(None, None))
        #data = json.loads(requests.get('https://fur-finder.herokuapp.com/api/pets/').text)
        #for dict in data[:10]:
            #card = Card(dict['name'], dict['gender'], dict['image'], dict['breed'], dict['color'], dict['date']).build()
            #carousel.add_widget(card)
        #for i in range(10):
            #card = Card('Waffles', 'Male', 'images/corgi.jpg', 'Corgi', 'Gold', 'Lost').build()
            #carousel.add_widget(card)
        #home_screen.add_widget(carousel)
        #return anchor_layout

    def scale(self):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            DisplayMetrics = autoclass('android.util.DisplayMetrics')
            displayMetrics = DisplayMetrics()
            currentActivity.getWindowManager().getDefaultDisplay().getMetrics(displayMetrics)

            width = displayMetrics.widthPixels
            height = displayMetrics.heightPixels - dp(24)

            print('The width of this android device is:', width)
            print('The height of this android device is:', height)

            ratio_width = width / 375
            ratio_height = height / 812

            return width, height, ratio_height, ratio_width
        except:
            print('Not an android device')
            return 375, 812, 1, 1

    def build(self):
        box_layout = BoxLayout(orientation='vertical')
        screens = Screens().create()
        navigation = Navigation(screens).create()

        box_layout.add_widget(screens)
        box_layout.add_widget(navigation)

        return box_layout

if __name__ == '__main__':
    MyApp().run()

#return Label(text='[color=150470]Fur Finder', font_name='DM-Serif-Display-Regular.ttf', font_size='50', markup=True)
