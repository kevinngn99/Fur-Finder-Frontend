from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button, ButtonBehavior
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp, sp

import requests
import json


class Report:
    class CustomButton(Button):
        def on_submit(self, instance, reported_screen=None, data=None):
            reported_screen.listen(data)
            #requests.post(url='https://fur-finder.herokuapp.com/api/pets//', data=dict)
        '''
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            with self.canvas:
                Color(rgb=get_color_from_hex('#023b80'))
                RoundedRectangle(size_hint=self.size_hint, size=self.size, radius=(dp(7), dp(7), dp(7), dp(7)))
        '''

    class Header:
        def create(self):
            header = Label(size_hint=(1, 0.1), halign='left', valign='top', font_size=sp(20), color=get_color_from_hex('#023b80'), text='[font=assets/Inter-SemiBold.ttf]Report a Pet', markup=True)
            header.bind(size=header.setter('text_size'))
            return header

    def __init__(self, reported_screen):
        self._reported_screen = reported_screen

    def create(self):
        data = {
            'name': 'This',
            'gender': 'is',
            'size': 'a',
            'date': 'test',
            'age': 'from',
            'state': 'the',
            'zip': 'frontend',
            'location': 'k',
            'breed': 'bye',
            'image': ':D'
        }

        anchor_layout = AnchorLayout(anchor_x='left', anchor_y='top', padding=(dp(20), dp(20), dp(0), dp(0)))
        anchor_layout.add_widget(self.Header().create())

        submit_button = self.CustomButton(size_hint=(None, None), size=(dp(100), dp(50)))
        submit_button.fbind('on_release', submit_button.on_submit, reported_screen=self._reported_screen, data=data)

        report_screen = Screen(name='Report')
        report_screen.add_widget(anchor_layout)
        report_screen.add_widget(submit_button)

        return report_screen
