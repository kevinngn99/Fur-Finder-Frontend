from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.snackbar import Snackbar
from screens.profile import Profile
from screens.login import LoginView

import os
import requests
import re

Builder.load_file(os.path.join(os.path.dirname(__file__), '../KivyFile/register.kv'))


class BackgroundBox2(BoxLayout):
    pass


class RegisterView(Screen):

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

    def getText(self):
        print(self.email_text.text)
        print(self.username_text.text)
        print(self.password_text.text)
        print(self.password2_text.text)

    def postUser(self):
        data = {'email': self.email_text.text, 'username': self.username_text.text, 'password': self.password_text.text, 'password2': self.password2_text.text}
        if self.password2_text.text != self.password_text.text:
            Snackbar(text="Passwords must match").show()
        else:
            res = requests.post(url='https://fur-finder.herokuapp.com/api/register//', data=data)
            print(res.status_code)
            print(res.text)
            if res.status_code == 201:
                data = {'username': self.username_text.text, 'password': self.password_text.text}
                login_res = requests.post(url='https://fur-finder.herokuapp.com/api/login/', data=data)
                print(login_res.text)

                pet_list = []
                username = self.email_text.text.split('@', 1)[0]
                regex = re.compile('[^a-zA-Z]')
                self.m.token = regex.sub('', username)
                LoginView.usr = self.m.token
                print(self.m.token)
                print(LoginView.usr)
                LoginView.pets_list = pets_list
                LoginView.author = self.email_text.text

                self.screens.add_widget(Profile().create(pet_list, LoginView.author))
                LoginView.token = login_res.json()['token']
                print(LoginView.token)
                self.sm.current = 'App'
            else:
                dictionary = res.json()
                if 'email' in dictionary:
                    if dictionary['email'][0] == 'account with this email already exists.':
                        Snackbar(text='Account with this email already exists.').show()
                    else:
                        Snackbar(text='Enter a valid email address.').show()
                elif 'username' in dictionary:
                    Snackbar(text='Account with this username already exists.').show()
                else:
                    Snackbar(text='Account creation error, try again.').show()

class Register:
    def __init__(self, sm=None, screens=None, m=None):
        super().__init__()
        self.sm = sm
        self.m = m
        self.screens = screens

    def create(self):
        register_screen = RegisterView(sm=self.sm, screens=self.screens, m=self.m, name="register")
        return register_screen
