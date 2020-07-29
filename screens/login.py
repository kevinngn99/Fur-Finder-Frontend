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
import re

Builder.load_file(os.path.join(os.path.dirname(__file__), '../KivyFile/login.kv'))


class BackgroundBox(BoxLayout):
    pass


class LoginView(Screen):
    access_token = StringProperty('')

    def __init__(self, sm=None, m=None, **kw):
        super().__init__(**kw)
        global token
        global usr
        token = None
        usr = None
        self.sm = sm
        self.m = m

    def get_pets_by_author(self):
        print(self.username_text.text)
        # print(self.password_text.text)
        headers = {
            'Authorization': 'Token 9a5de7d01e1ce563e4a08a862bf68268128d6f87'
        }
        pets = requests.get(url='https://fur-finder.herokuapp.com/api/pets//', headers=headers).json()
        users = requests.get(url='https://fur-finder.herokuapp.com/api/register//').json()
        author = ''
        pets_list = []

        for user in users:
            if user['username'] == self.username_text.text:
                author = user['email']

        for pet in pets:
            if pet['author'] == author:
                pets_list.append(pet)

        print(pets_list)
        regex = re.compile('[^a-zA-Z]')
        self.m.token = regex.sub('', author)
        LoginView.usr = self.m.token
        print(self.m.token)
        return pets_list

    def getUser(self):
        self.get_pets_by_author()
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


class Login:
    def __init__(self, sm=None, m=None):
        super().__init__()
        self.sm = sm
        self.m = m

    def create(self):
        login_screen = LoginView(sm=self.sm, m=self.m, name="login")
        return login_screen
