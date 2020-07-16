from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button, ButtonBehavior
from kivy.lang.builder import Builder
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
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
from kivy.uix.stacklayout import StackLayout
from kivy.uix.stencilview import StencilView
from kivy.metrics import sp, dp
from kivy.uix.widget import Widget
from kivy.core.window import Window
from datetime import datetime

Window.softinput_mode = "below_target"

import requests
import json
import os
import re

Builder.load_file(os.path.join(os.path.dirname(__file__), '../KivyFile/report.kv'))


class CustomStencilView(FloatLayout, StencilView):
    def on_size(self, *args):
        self.children[0].adjust_image_size(self)


class CustomImage(Image):
    def adjust_image_size(self, stencil):
        stencil_ratio = stencil.width / float(stencil.height)
        if self.image_ratio > stencil_ratio:
            self.width = stencil.height * self.image_ratio
            self.height = stencil.height
        else:
            self.width = stencil.width
            self.height = stencil.width / self.image_ratio


class FormInput(Widget):
    icon = StringProperty('')
    type = StringProperty('')
    input_type = StringProperty('text')


class FormLabel(ButtonBehavior, Widget):
    icon = StringProperty('')
    chevron = StringProperty('')
    type = StringProperty('')


class CustomMenu(ButtonBehavior, Label):
    pass


class FormImage(ButtonBehavior, Widget):
    pass


class CustomButton(ButtonBehavior, Label):
    pass


class CustomAnchorLayout(AnchorLayout):
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
            self._states = None
            self._zip_codes = None
            self._cities = None

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
            self._image = ''
            self._image_upload = None
            self._images_grid_layout = None
            self._files = None
            self._button_submit = None

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
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                self._files = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path, ext=['png', 'jpg', 'jpeg'])
                self._files.show(PythonActivity.storagePath)
            except:
                self._files = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path, ext=['png', 'jpg', 'jpeg'])
                self._files.show('/')

        def select_path(self, path):
            self._image_upload.ids.svg.color = get_color_from_hex('#023b80')
            self._image_upload.ids.icon.color = get_color_from_hex('#023b80')
            self.exit_manager(path)
            self._image = path
            anchor_layout = CustomAnchorLayout(size_hint=(None, None), size=(dp(95), dp(85)))
            layout = CustomStencilView()
            layout.add_widget(CustomImage(size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, keep_ratio=True, allow_stretch=True, source=path))
            anchor_layout.add_widget(layout)
            self._images_grid_layout.add_widget(anchor_layout)

        def exit_manager(self, path):
            self._files.close()

        def create_drop_down(self, button, list=None):
            drop_down = DropDown()
            drop_down.bind(on_select=lambda instance, x: (setattr(button.ids.category, 'text', x), setattr(button.ids.category, 'color', get_color_from_hex('#023b80')), setattr(button.ids.icon, 'color', get_color_from_hex('#023b80'))))

            for text in list:
                new_item = CustomMenu(size_hint=(1, None), height=dp(45), text=text)
                new_item.bind(on_release=lambda item: drop_down.select(item.text))
                drop_down.add_widget(new_item)

            drop_down.open(button)

        def on_change_text(self, instance, value):
            for state, list in self._states.items():
                if state == value:
                    self._zip_codes = []
                    self._cities = []

                    for item in list:
                        self._zip_codes.append(item['zip'])
                        self._cities.append(item['city'])

        def on_focus(self, instance, value, icon=None):
            if instance.text == '':
                if value:
                    icon.color = get_color_from_hex('#023b80')
                else:
                    icon.color = get_color_from_hex('#c9d0dc')

        def on_cities(self, instance, value):
            try:
                for city in self._cities:
                    if city.lower().startswith(value.lower()):
                        diff = re.split(value, city, flags=re.IGNORECASE)[1]
                        if diff != '':
                            self._city.ids.category.suggestion_text = diff
                        break
            except:
                pass

        def on_zip_codes(self, instance, value):
            try:
                for zip in self._zip_codes:
                    if zip.startswith(value):
                        diff = re.split(value, zip)[1]
                        if diff != '':
                            self._zip.ids.category.suggestion_text = diff
                        break
            except:
                pass

        def submit_data(self):
            name = self._name.ids.category.text.replace('Name', '')
            gender = self._gender.ids.category.text.replace('Gender', '')
            age = self._age.ids.category.text.replace('Age', '')
            breed = self._breed.ids.category.text.replace('Breed', '')
            color = self._color.ids.category.text.replace('Color', '')
            size = self._size.ids.category.text.replace('Size', '')
            status = self._status.ids.category.text.replace('Status', '')
            date = self._date.ids.category.text.replace('Date', '')
            state = self._state.ids.category.text.replace('State', '')
            zip = self._zip.ids.category.text.replace('Zip', '')
            city = self._city.ids.category.text.replace('City', '')
            image = self._image

            #print('Name: ', name)
            #print('Gender: ', gender)
            #print('Age: ', age)
            #print('Breed: ', breed)
            #print('Color: ', color)
            #print('Size: ', size)
            #print('Status: ', status)
            #print('Date: ', date)
            #print('State: ', state)
            #print('Zip: ', zip)
            #print('City: ', city)
            #print('Image: ', image)

            dict = {
                'age': age.strip(),
                'breed': breed.strip(),
                'city': city.strip(),
                'color': color.strip(),
                'date': date.strip(),
                'gender': gender.strip(),
                'image': image.strip(),
                'name': name.strip(),
                'petid': 'N/A',
                'size': size.strip(),
                'state': state.strip(),
                'status': status.strip(),
                'zip': zip.strip()
            }

            successful = True

            for key, value in dict.items():
                if value == '':
                    successful = False
                    print(key + ' is missing.')
                    break

            if successful:
                print('All fields satisfied.')
                with open(image, 'rb') as img:
                    del dict['image']
                    print(dict)
                    result = requests.post(url='http://127.0.0.1:8000/api/pets//', data=dict, files={'image': img})
                    print(result.text)

        def create(self):
            with open(os.path.join(os.path.dirname(__file__), '../states.json')) as file:
                self._states = json.load(file)

            main_grid_layout = GridLayout(size_hint=(1, None), cols=1, spacing=dp(20))
            main_grid_layout.bind(minimum_height=main_grid_layout.setter('height'))

            self._name = FormInput(size_hint=(1, None), height=dp(45), icon='', type='Name')
            self._name.ids.category.fbind('focus', self.on_focus, icon=self._name.ids.icon)

            self._breed = FormInput(size_hint=(1, None), height=dp(45), icon='', type='Breed')
            self._breed.ids.category.fbind('focus', self.on_focus, icon=self._breed.ids.icon)

            self._city = FormInput(size_hint=(1, None), height=dp(45), icon='', type='City')
            self._city.ids.category.fbind('focus', self.on_focus, icon=self._city.ids.icon)
            self._city.ids.category.fbind('text', self.on_cities)

            self._zip = FormInput(size_hint=(1, None), height=dp(45), icon='', type='Zip', input_type='number')
            self._zip.ids.category.fbind('focus', self.on_focus, icon=self._zip.ids.icon)
            self._zip.ids.category.fbind('text', self.on_zip_codes)

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

            self._button_submit = Button(text='Submit', size_hint=(None, None), size=(dp(100), dp(50)))
            self._button_submit.on_release = lambda: self.submit_data()

            gender_and_age_grid_layout = GridLayout(size_hint=(1, None), cols=2, spacing=dp(20))
            gender_and_age_grid_layout.bind(minimum_height=gender_and_age_grid_layout.setter('height'))
            gender_and_age_grid_layout.add_widget(self._gender)
            gender_and_age_grid_layout.add_widget(self._age)

            color_and_size_grid_layout = GridLayout(size_hint=(1, None), cols=2, spacing=dp(20))
            color_and_size_grid_layout.bind(minimum_height=color_and_size_grid_layout.setter('height'))
            color_and_size_grid_layout.add_widget(self._color)
            color_and_size_grid_layout.add_widget(self._size)

            state_and_zip_grid_layout = GridLayout(size_hint=(1, None), cols=2, spacing=dp(20))
            state_and_zip_grid_layout.bind(minimum_height=state_and_zip_grid_layout.setter('height'))
            state_and_zip_grid_layout.add_widget(self._state)
            state_and_zip_grid_layout.add_widget(self._zip)

            status_and_date_grid_layout = GridLayout(size_hint=(1, None), cols=2, spacing=dp(20))
            status_and_date_grid_layout.bind(minimum_height=status_and_date_grid_layout.setter('height'))
            status_and_date_grid_layout.add_widget(self._status)
            status_and_date_grid_layout.add_widget(self._date)

            self._image_upload = FormImage(size_hint=(None, None), size=(dp(95), dp(85)))
            self._image_upload.ids.svg.text = ''
            self._image_upload.ids.icon.text = ''
            self._image_upload.on_release = lambda: self.load_files()
            self._images_grid_layout = StackLayout(size_hint=(1, None), spacing=dp(20))
            self._images_grid_layout.bind(minimum_height=self._images_grid_layout.setter('height'))
            self._images_grid_layout.add_widget(self._image_upload)

            main_grid_layout.add_widget(self._name)
            main_grid_layout.add_widget(gender_and_age_grid_layout)
            main_grid_layout.add_widget(self._breed)
            main_grid_layout.add_widget(color_and_size_grid_layout)
            main_grid_layout.add_widget(status_and_date_grid_layout)
            main_grid_layout.add_widget(state_and_zip_grid_layout)
            main_grid_layout.add_widget(self._city)
            main_grid_layout.add_widget(self._images_grid_layout)
            main_grid_layout.add_widget(self._button_submit)

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
