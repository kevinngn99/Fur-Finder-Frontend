from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivymd.icon_definitions import md_icons
from kivymd.toast import toast
import os
import requests
import json

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
        #print(res.text)
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



class Login:
    """
        screen_manager = ScreenManager(transition=SlideTransition(), size_hint=(1, 1))
    login_screen = LoginView(name='login')
    screen_manager.add_widget(login_screen)
    """

    def __init__(self):
        super().__init__

    def create(self):
       login_screen = LoginView(name="login")

       return login_screen

