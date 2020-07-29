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
        self.dict = None

    def on_switch(self, instance, value):
        current = value

        self.dict['Home'].color = get_color_from_hex('#c9d0dc')
        self.dict['Report'].color = get_color_from_hex('#c9d0dc')
        self.dict['Message'].color = get_color_from_hex('#c9d0dc')
        self.dict['Reported'].color = get_color_from_hex('#c9d0dc')
        self.dict[current].color = get_color_from_hex('#023b80')

    def home_callback(self, screen_manager):
        print('The home button is being pressed')
        screen_manager.current = 'Home'

    def report_callback(self, screen_manager):
        print('The report button is being pressed')
        screen_manager.current = 'Report'

    def message_callback(self, screen_manager):
        print('The message button is being pressed')
        screen_manager.current = 'Message'

    def reported_callback(self, screen_manager):
        print('The reported button is being pressed')
        screen_manager.current = 'Reported'

    def create(self):
        self._screen_manager.fbind('current', self.on_switch)

        box_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))

        home_button = self.TextButton(size_hint=(0.25, 1), font_size=sp(20), color=get_color_from_hex('#023b80'), text='[font=assets/Font-Awesome.ttf]', markup=True)
        report_button = self.TextButton(size_hint=(0.25, 1), font_size=sp(20), color=get_color_from_hex('#c9d0dc'), text='[font=assets/Font-Awesome.ttf]', markup=True)
        message_button = self.TextButton(size_hint=(0.25, 1), font_size=sp(20), color=get_color_from_hex('#c9d0dc'), text='[font=assets/Font-Awesome.ttf]', markup=True)
        reported_button = self.TextButton(size_hint=(0.25, 1), font_size=sp(20), color=get_color_from_hex('#c9d0dc'), text='[font=assets/Font-Awesome.ttf]', markup=True)

        self.dict = {'Home': home_button, 'Report': report_button, 'Message': message_button, 'Reported': reported_button}

        home_button.on_release = lambda: self.home_callback(self._screen_manager)
        report_button.on_release = lambda: self.report_callback(self._screen_manager)
        message_button.on_release = lambda: self.message_callback(self._screen_manager)
        reported_button.on_release = lambda: self.reported_callback(self._screen_manager)

        box_layout.add_widget(home_button)
        box_layout.add_widget(report_button)
        box_layout.add_widget(message_button)

        box_layout.add_widget(reported_button)

        return box_layout
