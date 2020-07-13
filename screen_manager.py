from kivy.uix.screenmanager import ScreenManager
from screens.home import Home
from screens.report import Report
from screens.message import Message
from screens.reported import Reported


class Screens:
    def create(self):
        screen_manager = ScreenManager(size_hint=(1, 0.9))

        home_screen = Home().create()
        report_screen = Report().create()
        message_screen = Message().create()
        reported_screen = Reported().create()

        screen_manager.add_widget(home_screen)
        screen_manager.add_widget(report_screen)
        screen_manager.add_widget(message_screen)
        screen_manager.add_widget(reported_screen)

        return screen_manager
