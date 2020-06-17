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
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.animation import Animation
from custom_carousel import CustomCarousel
from card_view import Card
import requests
import json
from jnius import cast
from jnius import autoclass


class FLColor(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(rgb=get_color_from_hex('#ffffff'))
            Rectangle(pos=self.pos, size=self.size)


class SMColor(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(rgb=get_color_from_hex('#ffffff'))
            Rectangle(pos=self.pos, size=self.size)


class BLColor(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(rgb=get_color_from_hex('#ffffff'))
            Rectangle(pos=self.pos, size=self.size)


class TextButton(ButtonBehavior, Label):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


class SearchBox(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgb=get_color_from_hex('#F2F3FB'))
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])


class Search(TextInput):
    def on_focus(self, instance, value):
        if value:
            anim = Animation(x=self.parent.x, y=self.parent.y - 100, duration=0.1)
            anim.start(self.parent)
        else:
            anim = Animation(x=self.parent.x, y=self.parent.y + 100, duration=0.1)
            anim.start(self.parent)


class MyApp(App):
    def home_callback(self, screen_manager, dict):
        print('The home button is being pressed')
        dict[screen_manager.current].color = get_color_from_hex('#B8B3D4')
        screen_manager.current = 'Home'
        dict[screen_manager.current].color = get_color_from_hex('#150470')

    def report_callback(self, screen_manager, dict):
        print('The report button is being pressed')
        dict[screen_manager.current].color = get_color_from_hex('#B8B3D4')
        screen_manager.current = 'Report'
        dict[screen_manager.current].color = get_color_from_hex('#150470')

    def message_callback(self, screen_manager, dict):
        print('The message button is being pressed')
        dict[screen_manager.current].color = get_color_from_hex('#B8B3D4')
        screen_manager.current = 'Message'
        dict[screen_manager.current].color = get_color_from_hex('#150470')

    def pin_callback(self, screen_manager, dict):
        print('The pin button is being pressed')
        dict[screen_manager.current].color = get_color_from_hex('#B8B3D4')
        screen_manager.current = 'Pin'
        dict[screen_manager.current].color = get_color_from_hex('#150470')

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
            currentActivity.getWindowManager().getDefaultDisplay().getMetrics(displayMetrics)\

            width = displayMetrics.widthPixels
            height = displayMetrics.heightPixels

            print('The width of this android device is:', width)
            print('The height of this android device is:', height)

            ratio_width = width / 375
            ratio_height = height / 812

            if ratio_width < ratio_height:
                print('Scaling this app by:', ratio_width)
                return width, height, ratio_width
            else:
                print('Scaling this app by:', ratio_height)
                return width, height, ratio_height
        except:
            print('Not an android device')
            return 375, 812, 1

    def build(self):
        width, height, scale = self.scale()
        float_layout = FLColor(pos=(0, (height-812*scale)/2), size_hint=(None, None), size=(width, 812*scale))

        screen_manager = SMColor(pos=(float_layout.x, float_layout.y + 95*scale), size_hint=(None, None), size=(width, 717*scale))
        home_screen = Screen(name='Home')
        home_screen.add_widget(Label(text='[color=150470]Home Screen', font_name='assets/Inter-SemiBold.ttf', font_size=40*scale, markup=True))
        search_box = SearchBox(size_hint=(None, None), size=(321*scale, 60*scale), pos=((width-321*scale)/2, (height-60*scale-95*scale)))
        search_box.add_widget(Search(pos=search_box.pos, size_hint=(None, None), padding=(7*scale, 18*scale), cursor_color=(184/255, 179/255, 212/255, 1), cursor_width='2sp', background_active='', background_normal='', background_color=(242/255, 243/255, 251/255, 1), multiline=False, selection_color=(184/255, 179/255, 212/255, 0.5), foreground_color=(21/255, 4/255, 112/255, 1), size=(240*scale, 60*scale), font_size=20*scale, font_name='assets/Inter-SemiBold.ttf', hint_text='Search', hint_text_color=(184/255, 179/255, 212/255, 1)))
        search_box.bind(pos=self.callback_pos)
        search_icon = Label(padding=(15*scale, 0), halign='left', valign='center', markup=True, text='[color=150470][size='+str(int(24*scale))+'][font=assets/Feather.ttf]')
        search_icon.bind(size=search_icon.setter('text_size'))
        search_box.add_widget(search_icon)
        home_screen.add_widget(search_box)
        report_screen = Screen(name='Report')
        report_screen.add_widget(Label(text='[color=150470]Report Screen', font_name='assets/Inter-SemiBold.ttf', font_size=40*scale, markup=True))
        message_screen = Screen(name='Message')
        message_screen.add_widget(Label(text='[color=150470]Message Screen', font_name='assets/Inter-SemiBold.ttf', font_size=40*scale, markup=True))
        pin_screen = Screen(name='Pin')
        pin_screen.add_widget(Label(text='[color=150470]Pin Screen', font_name='assets/Inter-SemiBold.ttf', font_size=40*scale, markup=True))
        screen_manager.add_widget(home_screen)
        screen_manager.add_widget(report_screen)
        screen_manager.add_widget(message_screen)
        screen_manager.add_widget(pin_screen)

        box_layout = BLColor(orientation='horizontal', pos=(float_layout.x, float_layout.y), size_hint=(None, None), size=(width, 95*scale))
        home_button = TextButton(color=get_color_from_hex('#150470'), text='[size='+str(int(24*scale))+'][font=assets/Feather.ttf]', markup=True)
        report_button = TextButton(color=get_color_from_hex('#B8B3D4'), text='[size='+str(int(24*scale))+'][font=assets/Feather.ttf]', markup=True)
        message_button = TextButton(color=get_color_from_hex('#B8B3D4'), text='[size='+str(int(24*scale))+'][font=assets/Feather.ttf]', markup=True)
        pin_button = TextButton(color=get_color_from_hex('#B8B3D4'), text='[size='+str(int(24*scale))+'][font=assets/Feather.ttf]', markup=True)
        dict = {
            'Home': home_button,
            'Report': report_button,
            'Message': message_button,
            'Pin': pin_button
        }
        home_button.on_release = lambda: self.home_callback(screen_manager, dict)
        report_button.on_release = lambda: self.report_callback(screen_manager, dict)
        message_button.on_release = lambda: self.message_callback(screen_manager, dict)
        pin_button.on_release = lambda: self.pin_callback(screen_manager, dict)

        box_layout.add_widget(home_button)
        box_layout.add_widget(report_button)
        box_layout.add_widget(message_button)
        box_layout.add_widget(pin_button)

        float_layout.add_widget(screen_manager)
        float_layout.add_widget(box_layout)
        return float_layout

if __name__ == '__main__':
    MyApp().run()

#return Label(text='[color=150470]Fur Finder', font_name='DM-Serif-Display-Regular.ttf', font_size='50', markup=True)
