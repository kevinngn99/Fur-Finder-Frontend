import kivy

kivy.require('1.11.1')# replace with your current kivy version !



from kivy.lang import Builder

from kivy.config import Config
from kivy.core.window import Window
Window.clearcolor = (1, 1, 1, 1)

from kivymd.app import MDApp

Builder.load_string("""
#:include KivyFile/login.kv
#:include KivyFile/report.kv
""")
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.screenmanager import Screen, ScreenManager
from custom_carousel import CustomCarousel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.picker import MDDatePicker
from kivy.properties import ObjectProperty
from card_view import Card
import requests
import json


class ImageButton(ButtonBehavior, Image):
    pass


class BackgroundBox(BoxLayout):
    pass


class LoginView(Screen):
    pass


class ReportView(Screen):
    gender_button = ObjectProperty(None)

    #def __init__(self, **kwargs):
    #    super().__init__(**kwargs)
     #   gender_items = [{'viewclass': 'MDMenuItem', 'text': 'key'}]
    #    gender_menu = MDDropdownMenu(caller=self.gender_button, items=gender_items)


    def gender_menu(self):
        print("we are here")
        gender_items = [{'viewclass': 'MDMenuItem', 'text': 'key'}]
        print("we are further")
        return MDDropdownMenu(caller=self.gender_button, items=gender_items)

    def set_item(self, text):
        print("set_item")
        print(text)


class MyApp(MDApp):
    def home_callback(self, screen_manager):
        print('The home button is being pressed')
        screen_manager.current = 'Home'

    def report_callback(self, screen_manager):
        print('The report button is being pressed')
        screen_manager.current = 'Report'

    def message_callback(self, screen_manager):
        print('The message button is being pressed')
        screen_manager.current = 'Message'

    def pin_callback(self, screen_manager):
        print('The pin button is being pressed')
        screen_manager.current = 'Pin'

    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='bottom')


        screen_manager = ScreenManager()
        login_screen = LoginView(name='login')
        report_screen = ReportView(name='Report')
        #report page stuff
        gender_items = [{'viewclass': 'MDMenuItem', 'text': 'Female'}, {'viewclass': 'MDMenuItem', 'text': 'Male'}]
        self.gender_menu = MDDropdownMenu(caller=report_screen.gender_button, items=gender_items, width_mult=2,
                                          use_icon_item=False)

        size_items = [{'viewclass': 'MDMenuItem', 'text': 'Small'}, {'viewclass': 'MDMenuItem', 'text': 'Middle'}
                        , {'viewclass': 'MDMenuItem', 'text': 'Large'}]
        self.size_menu = MDDropdownMenu(caller=report_screen.size_button, items=size_items, width_mult=2,
                                          use_icon_item=False)
        home_screen = Screen(name='Home')
        home_screen.add_widget(Label(text='[color=150470]Home Screen', font_name='assets/Inter-SemiBold.ttf', font_size='40sp', markup=True))

        carousel = CustomCarousel(direction='right', pos=(0, 100), size=(375, 200), size_hint=(None, None))
        #data = json.loads(requests.get('http://10.0.0.30:8000/api/pets/').text)
        #for dict in data[:10]:
        #    card = Card(dict['name'], dict['gender'], dict['image'], dict['breed'], dict['color'], dict['date']).build()
        #    carousel.add_widget(card)
        #home_screen.add_widget(carousel)

        #report_screen = Screen(name='Report')
        #report_screen.add_widget(Label(text='[color=150470]Report Screen', font_name='assets/Inter-SemiBold.ttf', font_size='40sp', markup=True))

        message_screen = Screen(name='Message')
        message_screen.add_widget(Label(text='[color=150470]Message Screen', font_name='assets/Inter-SemiBold.ttf', font_size='40sp', markup=True))

        pin_screen = Screen(name='Pin')
        pin_screen.add_widget(Label(text='[color=150470]Pin Screen', font_name='assets/Inter-SemiBold.ttf', font_size='40sp', markup=True))

        screen_manager.add_widget(login_screen)
        screen_manager.add_widget(home_screen)
        screen_manager.add_widget(report_screen)
        screen_manager.add_widget(message_screen)
        screen_manager.add_widget(pin_screen)

        home_button = ImageButton(source='images/home.png', on_press=lambda b: self.home_callback(screen_manager))
        report_button = ImageButton(source='images/report.png', on_press=lambda b: self.report_callback(screen_manager))
        message_button = ImageButton(source='images/message.png', on_press=lambda b: self.message_callback(screen_manager))
        pin_button = ImageButton(source='images/heart.png', on_press=lambda b: self.pin_callback(screen_manager))

        box_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), size=('375dp', '50dp'))
        box_layout.add_widget(home_button)
        box_layout.add_widget(report_button)
        box_layout.add_widget(message_button)
        box_layout.add_widget(pin_button)

        anchor_layout.add_widget(screen_manager)
        anchor_layout.add_widget(box_layout)

        return anchor_layout

if __name__ == '__main__':
    kivy.require('1.11.1')
    Config.set('graphics', 'resizable', False)
    Config.set('graphics', 'multisamples', '5')
    Window.clearcolor = (1, 1, 1, 1)
    Window.size = (375, 812)
    MyApp().run()

#return Label(text='[color=150470]Fur Finder', font_name='DM-Serif-Display-Regular.ttf', font_size='50', markup=True)
