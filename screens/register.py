from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
import os
import requests
import json

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
        data = {'email': self.email_text.text, 'username': self.username_text.text,
                'password': self.password_text.text, 'password2': self.password2_text.text}
        if self.password2_text.text != self.password_text.text:
            toast("Passwords must match")
        else:
            res = requests.post(url='https://fur-finder.herokuapp.com/api/register//', data=data)
            print(res.status_code)
            print(res.text)
            if res.status_code == 400:
                rmv = "['.]"
                dict = json.loads(res.text)
                print("we here")
                if "email" in dict:
                    text = str(dict.get("email"))
                    for ch in rmv:
                        text = text.replace(ch,"")
                    toast(text)
                elif "username" in dict:
                    text = str(dict.get("username"))
                    for ch in rmv:
                        text = text.replace(ch, "")
                    toast(text)
            else:
                print("registered")
                self.manager.current = 'App'


class Register:
    def __init__(self, sm=None, screens=None, m=None):
        super().__init__()
        self.sm = sm
        self.m = m
        self.screens = screens

    def create(self):
        register_screen = RegisterView(sm=self.sm, screens=self.screens, m=self.m, name="register")
        return register_screen
