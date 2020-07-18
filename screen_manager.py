from kivy.uix.screenmanager import ScreenManager
from screens.home import Home
from screens.report import Report
from screens.message import Message
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

        return screen_manager
