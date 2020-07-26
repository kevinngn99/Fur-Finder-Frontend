from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.icon_definitions import md_icons
import os
import requests

Builder.load_file(os.path.join(os.path.dirname(__file__), '../KivyFile/login.kv'))


class BackgroundBox(BoxLayout):
    pass


class LoginView(Screen):

    def getText(self):
        print(self.username_text.text)
        print(self.password_text.text)

    def getUser(self):
        data = {'username': self.username_text.text, 'password': self.password_text.text}
        res = requests.post(url='https://fur-finder.herokuapp.com/api/login/', data = data)
        print(res.text)


class Login:

    def __init__(self):
        super().__init__

    def create(self):
       login_screen = LoginView(name="login")

       return login_screen
