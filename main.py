import kivy
kivy.require('1.11.1') # replace with your current kivy version !

from kivy.config import Config
Config.set('graphics', 'width', '375')
Config.set('graphics', 'height', '812')
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'multisamples', '5')

from kivy.core.window import Window
Window.clearcolor = (1, 1, 1, 1)

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.screenmanager import Screen, ScreenManager
from custom_carousel import CustomCarousel
from card_view import Card


class ImageButton(ButtonBehavior, Image):
    pass


class MyApp(App):
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
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='bottom')
        screen_manager = ScreenManager()

        home_screen = Screen(name='Home')
        home_screen.add_widget(Label(text='[color=150470]Home Screen', font_name='Inter-SemiBold.ttf', font_size='40', markup=True))

        carousel = CustomCarousel(direction='right', pos=(0, 100), size=(375, 200), size_hint=(None, None))
        for i in range(10):
            card = Card().build((0, 0))
            carousel.add_widget(card)
        home_screen.add_widget(carousel)

        report_screen = Screen(name='Report')
        report_screen.add_widget(Label(text='[color=150470]Report Screen', font_name='Inter-SemiBold.ttf', font_size='40', markup=True))

        message_screen = Screen(name='Message')
        message_screen.add_widget(Label(text='[color=150470]Message Screen', font_name='Inter-SemiBold.ttf', font_size='40', markup=True))

        pin_screen = Screen(name='Pin')
        pin_screen.add_widget(Label(text='[color=150470]Pin Screen', font_name='Inter-SemiBold.ttf', font_size='40', markup=True))

        screen_manager.add_widget(home_screen)
        screen_manager.add_widget(report_screen)
        screen_manager.add_widget(message_screen)
        screen_manager.add_widget(pin_screen)

        home_button = ImageButton(source='home.png', on_press=lambda b: self.home_callback(screen_manager))
        report_button = ImageButton(source='report.png', on_press=lambda b: self.report_callback(screen_manager))
        message_button = ImageButton(source='message.png', on_press=lambda b: self.message_callback(screen_manager))
        pin_button = ImageButton(source='heart.png', on_press=lambda b: self.pin_callback(screen_manager))

        box_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(375, 50))
        box_layout.add_widget(home_button)
        box_layout.add_widget(report_button)
        box_layout.add_widget(message_button)
        box_layout.add_widget(pin_button)

        anchor_layout.add_widget(screen_manager)
        anchor_layout.add_widget(box_layout)

        return anchor_layout

if __name__ == '__main__':
    MyApp().run()

#return Label(text='[color=150470]Fur Finder', font_name='DM-Serif-Display-Regular.ttf', font_size='50', markup=True)
