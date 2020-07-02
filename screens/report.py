from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp, sp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.widget import Widget
import base64

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.picker import MDDatePicker
from kivymd.toast.kivytoast.kivytoast import toast

import requests
import json
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), '../KivyFile/report.kv'))


class TopPage(BoxLayout):
    pass


class MDMenuItem(Widget):
    menu_button = ObjectProperty(None)

    def on_release(self):
        print(self.text)
        self.menu_button.text = self.text


class ReportView(Screen):
    name_button = ObjectProperty(None)
    gender_button = ObjectProperty(None)
    size_button = ObjectProperty(None)
    age_button = ObjectProperty(None)
    state_button = ObjectProperty(None)
    zip_button = ObjectProperty(None)
    breed_button = ObjectProperty(None)
    calendar_button = ObjectProperty(None)
    menu_button = ObjectProperty(None)

    def set_gender(self, instance):
        self.gender_button.text = instance.text

    def set_age(self, instance):
        self.age_button.text = instance.text

    def set_size(self, instance):
        self.size_button.text = instance.text

    def set_state(self, instance):
        self.state_button.text = instance.text

    postlist = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        gender_items = [{'viewclass': 'MDMenuItem', 'text': 'Female'}, {'viewclass': 'MDMenuItem', 'text': 'Male'}]
        self.gender_menu = MDDropdownMenu(caller=self.gender_button, callback=self.set_gender, items=gender_items, width_mult=3, use_icon_item=False)

        age_items = [{'viewclass': 'MDMenuItem', 'text': f"{i+1}"} for i in range(20)]
        self.age_menu = MDDropdownMenu(caller=self.age_button, callback=self.set_age, items=age_items, width_mult=2, use_icon_item=False)

        size_items = [{'viewclass': 'MDMenuItem', 'text': 'Small'}, {'viewclass': 'MDMenuItem', 'text': 'Medium'}, {'viewclass': 'MDMenuItem', 'text': 'Large'}]
        self.size_menu = MDDropdownMenu(caller=self.size_button, callback=self.set_size, items=size_items, width_mult=2, use_icon_item=False)

        state_items = [
            {'viewclass': 'MDMenuItem', 'text': 'AL'},
            {'viewclass': 'MDMenuItem', 'text': 'AK'},
            {'viewclass': 'MDMenuItem', 'text': 'AS'},
            {'viewclass': 'MDMenuItem', 'text': 'AZ'},
            {'viewclass': 'MDMenuItem', 'text': 'AR'},
            {'viewclass': 'MDMenuItem', 'text': 'CA'},
            {'viewclass': 'MDMenuItem', 'text': 'CO'},
            {'viewclass': 'MDMenuItem', 'text': 'CT'},
            {'viewclass': 'MDMenuItem', 'text': 'DE'},
            {'viewclass': 'MDMenuItem', 'text': 'DC'},
            {'viewclass': 'MDMenuItem', 'text': 'FL'},
            {'viewclass': 'MDMenuItem', 'text': 'GA'},
            {'viewclass': 'MDMenuItem', 'text': 'GU'},
            {'viewclass': 'MDMenuItem', 'text': 'HI'},
            {'viewclass': 'MDMenuItem', 'text': 'ID'},
            {'viewclass': 'MDMenuItem', 'text': 'IL'},
            {'viewclass': 'MDMenuItem', 'text': 'IN'},
            {'viewclass': 'MDMenuItem', 'text': 'IA'},
            {'viewclass': 'MDMenuItem', 'text': 'KS'},
            {'viewclass': 'MDMenuItem', 'text': 'KY'},
            {'viewclass': 'MDMenuItem', 'text': 'LA'},
            {'viewclass': 'MDMenuItem', 'text': 'ME'},
            {'viewclass': 'MDMenuItem', 'text': 'MD'},
            {'viewclass': 'MDMenuItem', 'text': 'MA'},
            {'viewclass': 'MDMenuItem', 'text': 'MI'},
            {'viewclass': 'MDMenuItem', 'text': 'MN'},
            {'viewclass': 'MDMenuItem', 'text': 'MS'},
            {'viewclass': 'MDMenuItem', 'text': 'MO'},
            {'viewclass': 'MDMenuItem', 'text': 'MT'},
            {'viewclass': 'MDMenuItem', 'text': 'NE'},
            {'viewclass': 'MDMenuItem', 'text': 'NV'},
            {'viewclass': 'MDMenuItem', 'text': 'NH'},
            {'viewclass': 'MDMenuItem', 'text': 'NJ'},
            {'viewclass': 'MDMenuItem', 'text': 'NM'},
            {'viewclass': 'MDMenuItem', 'text': 'NY'},
            {'viewclass': 'MDMenuItem', 'text': 'NC'},
            {'viewclass': 'MDMenuItem', 'text': 'ND'},
            {'viewclass': 'MDMenuItem', 'text': 'MP'},
            {'viewclass': 'MDMenuItem', 'text': 'OH'},
            {'viewclass': 'MDMenuItem', 'text': 'OK'},
            {'viewclass': 'MDMenuItem', 'text': 'OR'},
            {'viewclass': 'MDMenuItem', 'text': 'PA'},
            {'viewclass': 'MDMenuItem', 'text': 'PR'},
            {'viewclass': 'MDMenuItem', 'text': 'RI'},
            {'viewclass': 'MDMenuItem', 'text': 'SC'},
            {'viewclass': 'MDMenuItem', 'text': 'SD'},
            {'viewclass': 'MDMenuItem', 'text': 'TN'},
            {'viewclass': 'MDMenuItem', 'text': 'TX'},
            {'viewclass': 'MDMenuItem', 'text': 'UT'},
            {'viewclass': 'MDMenuItem', 'text': 'VT'},
            {'viewclass': 'MDMenuItem', 'text': 'VI'},
            {'viewclass': 'MDMenuItem', 'text': 'VA'},
            {'viewclass': 'MDMenuItem', 'text': 'WA'},
            {'viewclass': 'MDMenuItem', 'text': 'WV'},
            {'viewclass': 'MDMenuItem', 'text': 'WI'},
            {'viewclass': 'MDMenuItem', 'text': 'WY'}
        ]

        self.state_menu = MDDropdownMenu(caller=self.state_button, callback=self.set_state, items=state_items, width_mult=2, use_icon_item=False)

        self.manager_open = False
        self.file_manager = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path)
        self.datestr = "date"

    def file_manager_open(self):
        self.file_manager.show('/')
        self.manager_open = True

    def select_path(self, path):
        self.exit_manager(path)
        toast(path)

    def exit_manager(self, path):
        self.imgPath=path
        self.manager_open = False
        self.file_manager.close()
        return Image(source=path)

    def get_date(self, date):
        self.datestr = str(date)
        toast("Date Missing: " + self.datestr, duration=3)

    def date_picker(self):
        date_dialog = MDDatePicker(callback=self.get_date)
        date_dialog.open()

    def set_item(self):
        print("set_item")

    def post_report(self):
        print("post report")
        print(self.name_button.text)
        print(self.gender_button.text)
        print(self.size_button.text)
        print(self.datestr)
        print(self.age_button.text)
        print(self.state_button.text)
        print(self.zip_button.text)
        print(self.location_button.text)
        print(self.breed_button.text)
        self.postlist.append(self.name_button.text)
        self.postlist.append(self.gender_button.text)
        self.postlist.append(self.size_button.text)
        self.postlist.append(self.datestr)
        self.postlist.append(self.age_button.text)
        self.postlist.append(self.state_button.text)
        self.postlist.append(self.zip_button.text)
        self.postlist.append(self.location_button.text)
        self.postlist.append(self.breed_button.text)
        #TO DO
        #number authentication
        #blank authentication
        #default authentication
        with open(self.imgPath, mode='rb') as file:
             img = file.read()
        imageString=base64.encodebytes(img).decode("utf-8")
        self.postlist.append(imageString)

        post_data = {
            'name': self.postlist[0],
            'gender': self.postlist[1],
            'size': self.postlist[2],
            'date': self.postlist[3],
            'age': self.postlist[4],
            'state': self.postlist[5],
            'zip': self.postlist[6],
            'location': self.postlist[7],
            'breed': self.postlist[8],
            'image': self.postlist[9]
        }
        requests.post(url='https://fur-finder.herokuapp.com/api/pets//', data=post_data)


class Report(MDApp):
    class Header:
        def create(self):
            header = Label(size_hint=(1, None), height=dp(50), halign='left', valign='center', font_size=sp(40), color=get_color_from_hex('#150470'), text='[font=assets/Inter-SemiBold.ttf]Report A Pet', markup=True)
            header.bind(size=header.setter('text_size'))
            return header

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create(self):
        self.theme_cls.primary_palette = "DeepPurple"
        report_screen = ReportView(name='Report')

        return report_screen
