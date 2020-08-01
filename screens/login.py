from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.snackbar import Snackbar
from screens.profile import Profile
from kivy.core.window import Window

Window.softinput_mode = "below_target"

import os
import requests
import re

Builder.load_file(os.path.join(os.path.dirname(__file__), '../KivyFile/login.kv'))


class BackgroundBox(BoxLayout):
    pass


class LoginView(Screen):
    def __init__(self, sm=None, screens=None, m=None, **kw):
        super().__init__(**kw)
        global token
        global usr
        global pets_list
        global author
        token = None
        usr = None
        pets_list = None
        author = None
        self.sm = sm
        self.m = m
        self.screens = screens

    def get_pets_by_author(self):
        print(self.username_text.text)
        headers = {
            'Authorization': 'Token 9a5de7d01e1ce563e4a08a862bf68268128d6f87'
        }
        pets = requests.get(url='https://fur-finder.herokuapp.com/api/pets//', headers=headers).json()
        users = requests.get(url='https://fur-finder.herokuapp.com/api/register//').json()
        pets_list = []

        for user in users:
            if user['username'] == self.username_text.text:
                author = user['email']

        for pet in pets:
            if pet['author'] == author:
                pets_list.append(pet)

        print(pets_list)
        username = author.split('@', 1)[0]
        regex = re.compile('[^a-zA-Z]')
        self.m.token = regex.sub('', username)
        LoginView.usr = self.m.token
        print(self.m.token)
        LoginView.pets_list = pets_list
        LoginView.author = author
        return pets_list

    def getUser(self):
        data = {'username': self.username_text.text, 'password': self.password_text.text}
        res = requests.post(url='https://fur-finder.herokuapp.com/api/login/', data=data)
        print(res.status_code)
        if res.status_code == 200:
            pet_list = self.get_pets_by_author()
            self.screens.add_widget(Profile().create(pet_list, LoginView.author))
            LoginView.token = res.json()['token']
            print(LoginView.token)
            self.sm.current = 'App'
        else:
            Snackbar(text='Invalid credentials, try again.').show()


class Login:
    def __init__(self, sm=None, screens=None, m=None):
        super().__init__()
        self.sm = sm
        self.m = m
        self.screens = screens

    def create(self):
        login_screen = LoginView(sm=self.sm, screens=self.screens, m=self.m, name="login")
        return login_screen
