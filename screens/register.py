#remeber to add this to the screen manager py
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.icon_definitions import md_icons
from kivymd.toast import toast
import os
import requests
import json
from kivymd.app import MDApp

Builder.load_file(os.path.join(os.path.dirname(__file__), '../KivyFile/register.kv'))


class BackgroundBox(BoxLayout):
    pass


class RegisterView(Screen):

    def getText(self):
        print(self.email_text.text)
        print(self.username_text.text)
        print(self.password_text.text)
        print(self.password2_text.text)

    def postUser(self):
        #checks:
        #no other username or email like that exists
        #password1 and 2 are the same
        #email is legit
        #data = {'username': self.username_text.text, 'password': self.password_text.text}
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

class Register:

    def __init__(self):
        super().__init__

    def create(self):
       register_screen = RegisterView(name="register")

       return register_screen
