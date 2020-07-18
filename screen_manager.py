from kivy.uix.screenmanager import ScreenManager
from screens.home import Home
from screens.report import Report
from screens.message import Message
<<<<<<< HEAD
from screens.reported import Reported
from screens.login import Login
from screens.register import Register
class Screens:
    def create(self):
        screen_manager = ScreenManager(size_hint=(1, 0.9))

        login_screen = Login().create()
        home_screen = Home().create()
        reported_screen = Reported().create()
        report_screen = Report(reported_screen).create()
        message_screen = Message().create()
        register_screen = Register().create()

        #screen_manager.add_widget(register_screen)
        #screen_manager.add_widget(login_screen)
        screen_manager.add_widget(home_screen)
        screen_manager.add_widget(report_screen)
        screen_manager.add_widget(message_screen)
        screen_manager.add_widget(reported_screen)
=======
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
>>>>>>> e631afbba8826dae696c418f8027cfbf7d24c340

        return screen_manager
