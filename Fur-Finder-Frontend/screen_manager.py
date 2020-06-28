from kivy.uix.screenmanager import ScreenManager
from screens.home import Home
from screens.report import Report
from screens.message import Message
from screens.pin import Pin


class Screens:
    def __init__(self, home=None, report=None, message=None, pin=None):
        self._home = home,
        self._report = report,
        self._message = message,
        self._pin = pin

    def create(self):
        screen_manager = ScreenManager(size_hint=(1, 0.9))

        home_screen = Home().create()
        report_screen = Report().create()
        message_screen = Message().create()
        pin_screen = Pin().create()

        screen_manager.add_widget(home_screen)
        screen_manager.add_widget(report_screen)
        screen_manager.add_widget(message_screen)
        screen_manager.add_widget(pin_screen)

        return screen_manager
