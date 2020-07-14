from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button, ButtonBehavior
from kivy.lang.builder import Builder
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.dropdown import DropDown
from kivy.utils import get_color_from_hex
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.filemanager import MDFileManager
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.metrics import sp, dp
from kivy.uix.widget import Widget
from kivy.core.window import Window
from datetime import datetime

Window.softinput_mode = "below_target"

import requests
import json
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), '../KivyFile/report.kv'))


class FormLabel(ButtonBehavior, Widget):
    icon = StringProperty('')
    chevron = StringProperty('')
    type = StringProperty('')


class FormImage(ButtonBehavior, Widget):
    pass


class CustomButton(ButtonBehavior, Label):
    pass


class Report(MDApp):
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
            anchor_layout = AnchorLayout(size_hint=(1, 0.1), anchor_x='left', anchor_y='top')

            header = Label(halign='left', valign='top', font_size=sp(20), color=get_color_from_hex('#023b80'), text='[font=assets/Inter-SemiBold.ttf]Report a Pet', markup=True)
            header.bind(size=header.setter('text_size'))

            #'[font=assets/Inter-Regular.ttf][size='+str(int(dp(16)))+'][color=#6e7c97]\nEnter the details of the pet you wish to report. All fields are required.'

            anchor_layout.add_widget(header)
            return anchor_layout

    class Form:
        def __init__(self):
            self._name = None
            self._gender = None
            self._age = None
            self._breed = None
            self._color = None
            self._size = None
            self._status = None
            self._date = None
            self._state = None
            self._zip = None
            self._city = None
            self._image = None
            self._images_grid_layout = None
            self._files = None

        def get_states(self):
            list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',
                    'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND',
                    'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
            return list

        def get_date(self, date):
            self._date.ids.category.text = datetime.strptime(str(date), '%Y-%m-%d').strftime('%B %d, %Y')
            self._date.ids.category.color = get_color_from_hex('#023b80')
            self._date.ids.icon.color = get_color_from_hex('#023b80')

        def date_picker(self):
            date_dialog = MDDatePicker(callback=self.get_date)
            date_dialog.open()

        def load_files(self):
            self._files = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path)
            self._files.show('/')

        def select_path(self, path):
            self.exit_manager(path)
            self._image = Image(source=path)
            self._images_grid_layout.add_widget(self._image)

        def exit_manager(self, path):
            self._files.close()

        def create_drop_down(self, button, list=None):
            drop_down = DropDown()
            drop_down.bind(on_select=lambda instance, x: (setattr(button.ids.category, 'text', x), setattr(button.ids.category, 'color', get_color_from_hex('#023b80')), setattr(button.ids.icon, 'color', get_color_from_hex('#023b80'))))

            for text in list:
                new_item = Button(size_hint=(1, None), height=dp(45), text=text)
                new_item.bind(on_release=lambda item: drop_down.select(item.text))
                drop_down.add_widget(new_item)

            drop_down.open(button)

        def on_change_text(self, instance, value):
            print(value)
            self._zip.fbind('on_release', self.create_drop_down, list=['To', 'Do'])

        def create(self):
            main_grid_layout = GridLayout(size_hint=(1, None), cols=1, spacing=dp(10))
            main_grid_layout.bind(minimum_height=main_grid_layout.setter('height'))

            self._name = Button(size_hint=(1, None), height=dp(45), text='Name')
            self._breed = Button(size_hint=(1, None), height=dp(45), text='Breed')
            self._city = Button(size_hint=(1, None), height=dp(45), text='City')

            self._date = FormLabel(size_hint=(1, None), height=dp(45), icon='', type='Date', chevron='')
            self._date.on_release = lambda: self.date_picker()

            self._gender = FormLabel(size_hint=(1, None), height=dp(45), icon='', type='Gender')
            self._gender.fbind('on_release', self.create_drop_down, list=['Male', 'Female'])

            self._age = FormLabel(size_hint=(1, None), height=dp(45), icon='', type='Age')
            self._age.fbind('on_release', self.create_drop_down, list=['Puppy', 'Adult', 'Senior'])

            self._color = FormLabel(size_hint=(1, None), height=dp(45), icon='', type='Color')
            self._color.fbind('on_release', self.create_drop_down, list=['Black', 'Blue', 'Brown', 'Cream', 'Fawn', 'Gold', 'Grey', 'Orange', 'Red', 'Tan', 'White'])

            self._size = FormLabel(size_hint=(1, None), height=dp(45), icon='', type='Size')
            self._size.fbind('on_release', self.create_drop_down, list=['Small', 'Medium', 'Large'])

            self._status = FormLabel(size_hint=(1, None), height=dp(45), icon='', type='Status')
            self._status.fbind('on_release', self.create_drop_down, list=['Lost', 'Found'])

            self._state = FormLabel(size_hint=(1, None), height=dp(45), icon='', type='State')
            self._state.fbind('on_release', self.create_drop_down, list=self.get_states())
            self._state.ids.category.fbind('text', self.on_change_text)

            self._zip = FormLabel(size_hint=(1, None), height=dp(45), icon='', type='Zip')

            gender_and_age_grid_layout = GridLayout(size_hint=(1, None), cols=2, spacing=dp(10))
            gender_and_age_grid_layout.bind(minimum_height=gender_and_age_grid_layout.setter('height'))
            gender_and_age_grid_layout.add_widget(self._gender)
            gender_and_age_grid_layout.add_widget(self._age)

            color_and_size_grid_layout = GridLayout(size_hint=(1, None), cols=2, spacing=dp(10))
            color_and_size_grid_layout.bind(minimum_height=color_and_size_grid_layout.setter('height'))
            color_and_size_grid_layout.add_widget(self._color)
            color_and_size_grid_layout.add_widget(self._size)

            state_and_zip_grid_layout = GridLayout(size_hint=(1, None), cols=2, spacing=dp(10))
            state_and_zip_grid_layout.bind(minimum_height=state_and_zip_grid_layout.setter('height'))
            state_and_zip_grid_layout.add_widget(self._state)
            state_and_zip_grid_layout.add_widget(self._zip)

            status_and_date_grid_layout = GridLayout(size_hint=(1, None), cols=2, spacing=dp(10))
            status_and_date_grid_layout.bind(minimum_height=status_and_date_grid_layout.setter('height'))
            status_and_date_grid_layout.add_widget(self._status)
            status_and_date_grid_layout.add_widget(self._date)

            image_upload = FormImage(size_hint=(1, None), height=dp(150))
            image_upload.ids.svg.text = ''
            image_upload.ids.icon.text = ''
            image_upload.on_release = lambda: self.load_files()
            self._images_grid_layout = GridLayout(size_hint=(1, None), cols=3, spacing=dp(10))
            self._images_grid_layout.bind(minimum_height=self._images_grid_layout.setter('height'))
            self._images_grid_layout.add_widget(image_upload)

            main_grid_layout.add_widget(self._name)
            main_grid_layout.add_widget(gender_and_age_grid_layout)
            main_grid_layout.add_widget(self._breed)
            main_grid_layout.add_widget(color_and_size_grid_layout)
            main_grid_layout.add_widget(status_and_date_grid_layout)
            main_grid_layout.add_widget(state_and_zip_grid_layout)
            main_grid_layout.add_widget(self._city)
            main_grid_layout.add_widget(self._images_grid_layout)

            scroll_view = ScrollView(size_hint=(1, 0.9))
            scroll_view.add_widget(main_grid_layout)

            return scroll_view

    def __init__(self, reported_screen=None, **kwargs):
        super().__init__(**kwargs)
        self._reported_screen = reported_screen
        self.theme_cls.primary_palette = 'BlueGray'

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

        box_layout = BoxLayout(orientation='vertical', padding=(dp(20), dp(20), dp(20), dp(20)))

        header = self.Header().create()
        scroll_view = self.Form().create()

        box_layout.add_widget(header)
        box_layout.add_widget(scroll_view)

        report_screen = Screen(name='Report')
        report_screen.add_widget(box_layout)

        #submit_button = self.CustomButton(size_hint=(None, None), size=(dp(100), dp(50)))
        #submit_button.fbind('on_release', submit_button.on_submit, reported_screen=self._reported_screen, data=data)

        return report_screen
