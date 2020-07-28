from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivymd.icon_definitions import md_icons
from kivymd.toast import toast
from kivy.properties import StringProperty
import os
import requests
import json

Builder.load_file(os.path.join(os.path.dirname(__file__), '../KivyFile/login.kv'))


class BackgroundBox(BoxLayout):
    pass


class LoginView(Screen):
    access_token = StringProperty('')

    def __init__(self, sm=None, m=None, **kw):
        super().__init__(**kw)
        global token
        token = None
        self.sm = sm
        self.m = m

    def getText(self):
        print(self.username_text.text)
        print(self.password_text.text)

    def getUser(self):
        data = {'username': self.username_text.text, 'password': self.password_text.text}
        res = requests.post(url='https://fur-finder.herokuapp.com/api/login/', data=data)
        if res.status_code == 400:
            rmv = "['.]"
            dict = json.loads(res.text)
            print("we here")
            if "username" in dict:
                text = str(dict.get("username"))
                for ch in rmv:
                    text = text.replace(ch, "")
                toast(text)
            elif "password" in dict:
                text = str(dict.get("password"))
                for ch in rmv:
                    text = text.replace(ch, "")
                toast(text)
        else:
            self.sm.current = 'App'
            LoginView.token = res.json()['token']
            self.access_token = LoginView.token
            print(LoginView.token)
            self.m.token = LoginView.token


class Login:
    def __init__(self, sm=None, m=None):
        super().__init__()
        self.sm = sm
        self.m = m

    def create(self):
        login_screen = LoginView(sm=self.sm, m=self.m, name="login")
        return login_screen
