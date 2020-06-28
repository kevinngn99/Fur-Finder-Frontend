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
from kivymd.toast.kivytoast.kivytoast import toast
from card_view import Card
import requests
import json


class ImageButton(ButtonBehavior, Image):
    pass


class BackgroundBox(BoxLayout):
    pass

class TopPage(BoxLayout):
    pass


class LoginView(Screen):
    pass


class ReportView(Screen):
    gender_button = ObjectProperty(None)
    size_button = ObjectProperty(None)
    age_button = ObjectProperty(None)
    state_button = ObjectProperty(None)
    zip_button = ObjectProperty(None)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_button = None
        gender_items = [{'viewclass': 'MDMenuItem', 'text': 'Female'},
                        {'viewclass': 'MDMenuItem', 'text': 'Male'}]
        self.gender_menu = MDDropdownMenu(caller=self.gender_button, items=gender_items, width_mult=3,
                                          use_icon_item=False)

        age_items = [{'viewclass': 'MDMenuItem', 'text': f"{i+1}"} for i in range(20)]

        self.age_menu = MDDropdownMenu(caller=self.age_button, items=age_items, width_mult=2,
                                        use_icon_item=False)

        size_items = [{'viewclass': 'MDMenuItem', 'text': 'Small'},
                      {'viewclass': 'MDMenuItem', 'text': 'Middle'},
                      {'viewclass': 'MDMenuItem', 'text': 'Large'}]

        self.size_menu = MDDropdownMenu(caller=self.size_button, items=size_items, width_mult=2,
                                        use_icon_item=False)

        state_items = [
            {'viewclass': 'MDMenuItem', 'text': 'AL'},
            {'viewclass': 'MDMenuItem', 'text': 'AK'},
            {'viewclass': 'MDMenuItem', 'text': 'AS'},
            {'viewclass': 'MDMenuItem', 'text': 'AZ'},
            {'viewclass': 'MDMenuItem', 'text': 'AR'},
            {'viewclass': 'MDMenuItem', 'text': 'CA'},
            {'viewclass': 'MDMenuItem', 'text': 'CO'},
            {'viewclass': 'MDMenuItem', 'text': 'CT'},
            {'viewclass': 'MDMenuItem', 'text': 'DE'},
            {'viewclass': 'MDMenuItem', 'text': 'DC'},
            {'viewclass': 'MDMenuItem', 'text': 'FL'},
            {'viewclass': 'MDMenuItem', 'text': 'GA'},
            {'viewclass': 'MDMenuItem', 'text': 'GU'},
            {'viewclass': 'MDMenuItem', 'text': 'HI'},
            {'viewclass': 'MDMenuItem', 'text': 'ID'},
            {'viewclass': 'MDMenuItem', 'text': 'IL'},
            {'viewclass': 'MDMenuItem', 'text': 'IN'},
            {'viewclass': 'MDMenuItem', 'text': 'IA'},
            {'viewclass': 'MDMenuItem', 'text': 'KS'},
            {'viewclass': 'MDMenuItem', 'text': 'KY'},
            {'viewclass': 'MDMenuItem', 'text': 'LA'},
            {'viewclass': 'MDMenuItem', 'text': 'ME'},
            {'viewclass': 'MDMenuItem', 'text': 'MD'},
            {'viewclass': 'MDMenuItem', 'text': 'MA'},
            {'viewclass': 'MDMenuItem', 'text': 'MI'},
            {'viewclass': 'MDMenuItem', 'text': 'MN'},
            {'viewclass': 'MDMenuItem', 'text': 'MS'},
            {'viewclass': 'MDMenuItem', 'text': 'MO'},
            {'viewclass': 'MDMenuItem', 'text': 'MT'},
            {'viewclass': 'MDMenuItem', 'text': 'NE'},
            {'viewclass': 'MDMenuItem', 'text': 'NV'},
            {'viewclass': 'MDMenuItem', 'text': 'NH'},
            {'viewclass': 'MDMenuItem', 'text': 'NJ'},
            {'viewclass': 'MDMenuItem', 'text': 'NM'},
            {'viewclass': 'MDMenuItem', 'text': 'NY'},
            {'viewclass': 'MDMenuItem', 'text': 'NC'},
            {'viewclass': 'MDMenuItem', 'text': 'ND'},
            {'viewclass': 'MDMenuItem', 'text': 'MP'},
            {'viewclass': 'MDMenuItem', 'text': 'OH'},
            {'viewclass': 'MDMenuItem', 'text': 'OK'},
            {'viewclass': 'MDMenuItem', 'text': 'OR'},
            {'viewclass': 'MDMenuItem', 'text': 'PA'},
            {'viewclass': 'MDMenuItem', 'text': 'PR'},
            {'viewclass': 'MDMenuItem', 'text': 'RI'},
            {'viewclass': 'MDMenuItem', 'text': 'SC'},
            {'viewclass': 'MDMenuItem', 'text': 'SD'},
            {'viewclass': 'MDMenuItem', 'text': 'TN'},
            {'viewclass': 'MDMenuItem', 'text': 'TX'},
            {'viewclass': 'MDMenuItem', 'text': 'UT'},
            {'viewclass': 'MDMenuItem', 'text': 'VT'},
            {'viewclass': 'MDMenuItem', 'text': 'VI'},
            {'viewclass': 'MDMenuItem', 'text': 'VA'},
            {'viewclass': 'MDMenuItem', 'text': 'WA'},
            {'viewclass': 'MDMenuItem', 'text': 'WV'},
            {'viewclass': 'MDMenuItem', 'text': 'WI'},
            {'viewclass': 'MDMenuItem', 'text': 'WY'}
        ]

        self.state_menu = MDDropdownMenu(caller=self.state_button, items=state_items, width_mult=2,
                                        use_icon_item=False)

    datestr = "date"
    def get_date(self, date):
        self.datestr = str(date)
        toast("Date Missing: " + self.datestr, duration=3)
        #print(date)

    def date_picker(self):
        date_dialog = MDDatePicker(callback=self.get_date)
        date_dialog.open()

    def set_item(self):
        print("set_item")

    def post_report(self):
        print("post report")
        print(self.gender_button.text)
        print(self.size_button.text)
        print(self.datestr)
        print(self.age_button.text)
        print(self.state_button.text)
        print(self.zip_button.text)
        print(self.location_button.text)
        #TO DO
        #number authentication
        #blank authentication
        #default authentication
        #data = {}
        #requests.post(url=, data)

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

    def set_item(self, instance):
        print("set item")

    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        screen_manager = ScreenManager()
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='bottom')

        login_screen = LoginView(name='login')
        report_screen = ReportView(name='Report')

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
