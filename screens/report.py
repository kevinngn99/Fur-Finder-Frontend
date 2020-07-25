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
from kivymd.uix.button import MDFlatButton
from kivymd.uix.filemanager import MDFileManager
from kivy.properties import StringProperty, ColorProperty, ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivymd.uix.snackbar import Snackbar
from kivy.uix.stacklayout import StackLayout
from kivy.uix.stencilview import StencilView
from kivy.metrics import sp, dp
from kivy.uix.widget import Widget
from kivy.core.window import Window
from datetime import datetime

Window.softinput_mode = "below_target"

import requests
from threading import Thread
import json
import os
import re

Builder.load_file(os.path.join(os.path.dirname(__file__), '../KivyFile/report.kv'))


class CustomStencilView(FloatLayout, StencilView):
    def on_size(self, *args):
        self.children[0].adjust_image_size(self)


class CustomImageUpload(Image):
    def adjust_image_size(self, stencil):
        stencil_ratio = stencil.width / float(stencil.height)
        if self.image_ratio > stencil_ratio:
            self.width = stencil.height * self.image_ratio
            self.height = stencil.height
        else:
            self.width = stencil.width
            self.height = stencil.width / self.image_ratio


class CancelImage(ButtonBehavior, AnchorLayout):
    pass


class FormInput(AnchorLayout):
    icon = StringProperty('')
    type = StringProperty('')
    input_type = StringProperty('')
    input_filter = ObjectProperty(None)
    rgb = ColorProperty(get_color_from_hex('#c9d0dc'))


class SummaryInput(AnchorLayout):
    icon = StringProperty('')
    type = StringProperty('')
    input_type = StringProperty('')
    input_filter = ObjectProperty(None)
    rgb = ColorProperty(get_color_from_hex('#c9d0dc'))


class FormLabel(ButtonBehavior, AnchorLayout):
    icon = StringProperty('')
    chevron = StringProperty('')
    type = StringProperty('')
    rgb = ColorProperty(get_color_from_hex('#c9d0dc'))


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
            anchor_layout = AnchorLayout(size_hint=(1, 0.1), anchor_x='left', anchor_y='top', padding=(dp(20), dp(20), dp(20), dp(0)))

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
            self._selected_city = None
            self._selected_zip_code = None

            self._name = None
            self._gender = None
            self._age = None
            self._breed = None
            self._color = None
            self._size = None
            self._status = None
            self._date = None
            self._state = None
            self._summary = None
            self._zip = None
            self._city = None
            self._images = []
            self._image_upload = None
            self._images_grid_layout = None
            self._files = None
            self._button_submit = None

            self.raw_images = []

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
                self._files = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path, previous=True, ext=['png', 'jpg', 'jpeg'])
                self._files.show(PythonActivity.storagePath)
            except:
                self._files = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path, previous=True, ext=['png', 'jpg', 'jpeg'])
                self._files.show('/')

        def remove_image(self, instance, path=None):
            self._images_grid_layout.remove_widget(instance.parent.parent)
            self._images.remove(path)

        def select_path(self, path):
            self._image_upload.ids.svg.color = get_color_from_hex('#023b80')
            self._image_upload.ids.icon.color = get_color_from_hex('#023b80')
            self.exit_manager(path)
            self._images.append(path)
            anchor_layout = CustomAnchorLayout(size_hint=(None, None), size=(dp(95), dp(85)))
            layout = CustomStencilView()
            layout.add_widget(CustomImageUpload(size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, keep_ratio=True, allow_stretch=True, source=path))
            anchor_layout.add_widget(layout)
            cancel_layout = AnchorLayout(anchor_x='right', anchor_y='top', padding=(dp(-5), dp(-5)))
            cancel_image = CancelImage()
            cancel_image.ids.cancel.text = ''
            cancel_layout.add_widget(cancel_image)
            anchor_layout.add_widget(cancel_layout)
            holder = AnchorLayout(size_hint=(None, None), size=(dp(95), dp(85)))
            holder.add_widget(anchor_layout)
            copy_cancel_layout = AnchorLayout(anchor_x='right', anchor_y='top', padding=(dp(-5), dp(-5)))
            copy_cancel_image = CancelImage()
            copy_cancel_image.ids.cancel.text = ''
            copy_cancel_image.fbind('on_release', self.remove_image, path=path)
            copy_cancel_layout.add_widget(copy_cancel_image)
            holder.add_widget(copy_cancel_layout)
            self._images_grid_layout.add_widget(holder)

        def exit_manager(self, path):
            self._files.close()

        def on_deselect(self, instance, icon=None, border=None):
            border.rgb = get_color_from_hex('#c9d0dc')

            if border.ids.category.text == border.type:
                icon.color = get_color_from_hex('#c9d0dc')

        def create_drop_down(self, button, list=None, icon=None, border=None):
            border.rgb = get_color_from_hex('#023b80')
            icon.color = get_color_from_hex('#023b80')

            drop_down = DropDown()
            drop_down.fbind('on_dismiss', self.on_deselect, icon=icon, border=border)
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
                        self._cities.sort()

        def on_summary_focus(self, instance, value, icon=None, border=None):
            if value:
                border.rgb = get_color_from_hex('#023b80')
            else:
                border.rgb = get_color_from_hex('#c9d0dc')

            if instance.text == '':
                if value:
                    icon.color = get_color_from_hex('#023b80')
                else:
                    icon.color = get_color_from_hex('#c9d0dc')
            else:
                instance.text = instance.text

        def on_focus(self, instance, value, icon=None, border=None):
            if value:
                border.rgb = get_color_from_hex('#023b80')
            else:
                border.rgb = get_color_from_hex('#c9d0dc')

            if instance.text == '':
                if value:
                    icon.color = get_color_from_hex('#023b80')
                else:
                    icon.color = get_color_from_hex('#c9d0dc')
            else:
                instance.text = instance.text.title()

        def on_focus_city(self, instance, value, icon=None, border=None):
            if self._state.ids.category.text == 'State':
                instance.is_focusable = False
                Snackbar(text='Please select a state first!').show()
                instance.is_focusable = True
            else:
                if value:
                    border.rgb = get_color_from_hex('#023b80')
                else:
                    border.rgb = get_color_from_hex('#c9d0dc')

                if instance.text == '':
                    if value:
                        icon.color = get_color_from_hex('#023b80')
                    else:
                        icon.color = get_color_from_hex('#c9d0dc')
                else:
                    instance.text = self._selected_city

        def on_focus_zip(self, instance, value, icon=None, border=None):
            if self._state.ids.category.text == 'State':
                instance.is_focusable = False
                Snackbar(text='Please select a state first!').show()
                instance.is_focusable = True
            else:
                if value:
                    border.rgb = get_color_from_hex('#023b80')
                else:
                    border.rgb = get_color_from_hex('#c9d0dc')

                if instance.text == '':
                    if value:
                        icon.color = get_color_from_hex('#023b80')
                    else:
                        icon.color = get_color_from_hex('#c9d0dc')
                else:
                    instance.text = self._selected_zip_code

        def on_cities(self, instance, value):
            try:
                for city in self._cities:
                    if city.lower().startswith(value.lower()):
                        diff = re.split(value, city, flags=re.IGNORECASE)[1]
                        if diff != '':
                            self._city.ids.category.suggestion_text = diff
                            self._selected_city = city
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
                            self._selected_zip_code = zip
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
            summary = self._summary.ids.category.text.replace('Summary', '')
            zip = self._zip.ids.category.text.replace('Zip', '')
            city = self._city.ids.category.text.replace('City', '')
            images = self._images

            dict = {
                'name': name.strip(),
                'gender': gender.strip(),
                'age': age.strip(),
                'breed': breed.strip(),
                'color': color.strip(),
                'size': size.strip(),
                'status': status.strip(),
                'date': date.strip(),
                'state': state.strip(),
                'summary': summary,
                'zip': zip.strip(),
                'city': city.strip(),
                'petid': 'N/A'
            }

            for key, value in dict.items():
                if value == '':
                    Snackbar(text=key.title() + ' is missing.').show()
                    return

            if not images:
                Snackbar(text='Image is missing.').show()
                return

            Snackbar(text='Attempting to send requested pet...').show()
            print('All fields satisfied.')

            self._button_submit.disabled = True
            self._button_submit.text = 'SENDING'

            for image in images:
                tuple = (image, open(image, 'rb'))
                self.raw_images.append(tuple)

            #pool = Pool(1)
            #pool.apply_async(requests.post, args=['https://fur-finder.herokuapp.com/api/pets//'], kwds={'data': dict, 'files': self.raw_images}, callback=self.on_success, error_callback=self.on_error)

            Thread(target=self.post, args=(dict, )).start()

        def post(self, data):
            s = requests.Session()
            s.hooks['response'].append(self.callback)
            s.post('https://fur-finder.herokuapp.com/api/pets//', data=data, files=self.raw_images)

        def callback(self, r, **kwargs):
            print(r)

            for raw_image in self.raw_images:
                raw_image[1].close()

            if r.ok:
                Snackbar(text='Successfully reported pet.').show()
                print('POST successful.')
            else:
                Snackbar(text='Could not report pet. Try different pictures.').show()
                print('POST failed.')

            self._button_submit.disabled = False
            self._button_submit.text = 'SUBMIT'

        def create(self):
            with open(os.path.join(os.path.dirname(__file__), '../states.json')) as file:
                self._states = json.load(file)

            main_grid_layout = GridLayout(size_hint=(1, None), cols=1, spacing=dp(20), padding=(dp(20), dp(0), dp(20), dp(0)))
            main_grid_layout.bind(minimum_height=main_grid_layout.setter('height'))

            self._name = FormInput(size_hint=(1, None), height=dp(45), icon='', type='Name', input_type='text', input_filter=None)
            self._name.ids.category.fbind('focus', self.on_focus, icon=self._name.ids.icon, border=self._name)

            self._breed = FormInput(size_hint=(1, None), height=dp(45), icon='', type='Breed', input_type='text', input_filter=None)
            self._breed.ids.category.fbind('focus', self.on_focus, icon=self._breed.ids.icon, border=self._breed)

            self._city = FormInput(size_hint=(1, None), height=dp(45), icon='', type='City', input_type='text', input_filter=None)
            self._city.ids.category.fbind('focus', self.on_focus_city, icon=self._city.ids.icon, border=self._city)
            self._city.ids.category.fbind('text', self.on_cities)

            self._zip = FormInput(size_hint=(1, None), height=dp(45), icon='', type='Zip', input_type='number', input_filter='int')
            self._zip.ids.category.fbind('focus', self.on_focus_zip, icon=self._zip.ids.icon, border=self._zip)
            self._zip.ids.category.fbind('text', self.on_zip_codes)

            self._date = FormLabel(size_hint=(1, None), height=dp(45), icon='', type='Date', chevron='')
            self._date.on_release = lambda: self.date_picker()

            self._gender = FormLabel(size_hint=(1, None), height=dp(45), icon='', type='Gender')
            self._gender.fbind('on_release', self.create_drop_down, list=['Male', 'Female'], icon=self._gender.ids.icon, border=self._gender)

            self._age = FormLabel(size_hint=(1, None), height=dp(45), icon='', type='Age')
            self._age.fbind('on_release', self.create_drop_down, list=['Puppy', 'Adult', 'Senior'], icon=self._age.ids.icon, border=self._age)

            self._color = FormLabel(size_hint=(1, None), height=dp(45), icon='', type='Color')
            self._color.fbind('on_release', self.create_drop_down, list=['Black', 'Blue', 'Brown', 'Cream', 'Fawn', 'Gold', 'Grey', 'Orange', 'Red', 'Tan', 'White'], icon=self._color.ids.icon, border=self._color)

            self._size = FormLabel(size_hint=(1, None), height=dp(45), icon='', type='Size')
            self._size.fbind('on_release', self.create_drop_down, list=['Small', 'Medium', 'Large'], icon=self._size.ids.icon, border=self._size)

            self._status = FormLabel(size_hint=(1, None), height=dp(45), icon='', type='Status')
            self._status.fbind('on_release', self.create_drop_down, list=['Lost', 'Found'], icon=self._status.ids.icon, border=self._status)

            self._state = FormLabel(size_hint=(1, None), height=dp(45), icon='', type='State')
            self._state.fbind('on_release', self.create_drop_down, list=self.get_states(), icon=self._state.ids.icon, border=self._state)
            self._state.ids.category.fbind('text', self.on_change_text)

            self._summary = SummaryInput(size_hint=(1, None), height=dp(135), icon='', type='Summary', input_type='text', input_filter=None)
            self._summary.ids.category.fbind('focus', self.on_summary_focus, icon=self._summary.ids.icon, border=self._summary)

            self._button_submit = Button(text='SUBMIT', background_normal='', background_color=get_color_from_hex('#023b80'), font_size=dp(16), font_name='assets/Inter-Medium.ttf', size_hint=(None, None), size=(dp(100), dp(50)))
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
            main_grid_layout.add_widget(self._summary)
            main_grid_layout.add_widget(self._images_grid_layout)
            main_grid_layout.add_widget(self._button_submit)

            scroll_view = ScrollView(size_hint=(1, 0.9), effect_cls=ScrollEffect, bar_inactive_color=(0, 0, 0, 0), bar_color=(0, 0, 0, 0))
            scroll_view.add_widget(main_grid_layout)

            return scroll_view

    def __init__(self, reported_screen=None, **kwargs):
        super().__init__(**kwargs)
        self._reported_screen = reported_screen
        self.theme_cls.primary_palette = 'BlueGray'

    def create(self):
        box_layout = BoxLayout(orientation='vertical')
        header = self.Header().create()
        scroll_view = self.Form().create()
        box_layout.add_widget(header)
        box_layout.add_widget(scroll_view)

        report_screen = Screen(name='Report')
        report_screen.add_widget(box_layout)

        #submit_button = self.CustomButton(size_hint=(None, None), size=(dp(100), dp(50)))
        #submit_button.fbind('on_release', submit_button.on_submit, reported_screen=self._reported_screen, data=data)

        return report_screen
