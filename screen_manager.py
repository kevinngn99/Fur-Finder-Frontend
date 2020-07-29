from kivy.uix.screenmanager import ScreenManager, SlideTransition, Screen
from screens.home import Home
from screens.report import Report
from screens.message import Message
from screens.reported import Reported
from screens.login import Login
from screens.register import Register


class Screens:
    def create(self):
        screen_manager = ScreenManager(transition=SlideTransition(), size_hint=(1, 0.9))

        home_screen = Home().create()
        reported_screen = Reported(root_sm=screen_manager).create()
        report_screen = Report(reported_screen).create()
        message_screen = Message(name='Message')
        profile_screen = Screen(name='Profile')

        screen_manager.add_widget(home_screen)
        screen_manager.add_widget(report_screen)
        screen_manager.add_widget(message_screen)
        screen_manager.add_widget(reported_screen)
        screen_manager.add_widget(profile_screen)

        return screen_manager


class ScreensLogin:
    def create(self):
        screen_manager = ScreenManager(transition=SlideTransition(), size_hint=(1, 0.9))

        register_screen = Register().create()
        login_screen = Login().create()

        screen_manager.add_widget(login_screen)
        screen_manager.add_widget(register_screen)

        return screen_manager
