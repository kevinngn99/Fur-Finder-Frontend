from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
from kivy.metrics import sp


class Navigation:
    class TextButton(ButtonBehavior, Label):
        pass

    def __init__(self, screen_manager):
        self._screen_manager = screen_manager

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

    def create(self):
        box_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))

        home_button = self.TextButton(size_hint=(0.25, 1), font_size=sp(24), color=get_color_from_hex('#150470'), text='[font=assets/Feather.ttf]', markup=True)
        report_button = self.TextButton(size_hint=(0.25, 1), font_size=sp(24), color=get_color_from_hex('#B8B3D4'), text='[font=assets/Feather.ttf]', markup=True)
        message_button = self.TextButton(size_hint=(0.25, 1), font_size=sp(24), color=get_color_from_hex('#B8B3D4'), text='[font=assets/Feather.ttf]', markup=True)
        pin_button = self.TextButton(size_hint=(0.25, 1), font_size=sp(24), color=get_color_from_hex('#B8B3D4'), text='[font=assets/Feather.ttf]', markup=True)

        dict = {'Home': home_button, 'Report': report_button, 'Message': message_button, 'Pin': pin_button}

        home_button.on_release = lambda: self.home_callback(self._screen_manager, dict)
        report_button.on_release = lambda: self.report_callback(self._screen_manager, dict)
        message_button.on_release = lambda: self.message_callback(self._screen_manager, dict)
        pin_button.on_release = lambda: self.pin_callback(self._screen_manager, dict)

        box_layout.add_widget(home_button)
        box_layout.add_widget(report_button)
        box_layout.add_widget(message_button)
        box_layout.add_widget(pin_button)

        return box_layout
