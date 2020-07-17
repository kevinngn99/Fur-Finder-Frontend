from kivy.uix.screenmanager import ScreenManager, SlideTransition
from screens.home import Home
from screens.report import Report
from screens.message import Message
from screens.reported import Reported


class Screens:
    def create(self):
        screen_manager = ScreenManager(transition=SlideTransition(), size_hint=(1, 0.9))

        home_screen = Home().create()
        reported_screen = Reported().create()
        report_screen = Report(reported_screen).create()
        message_screen = Message().create()

        screen_manager.add_widget(home_screen)
        screen_manager.add_widget(report_screen)
        screen_manager.add_widget(message_screen)
        screen_manager.add_widget(reported_screen)

        return screen_manager
