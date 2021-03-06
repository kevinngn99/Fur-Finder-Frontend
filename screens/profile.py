from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty
from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import FocusBehavior
from kivymd.app import MDApp
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from custom_recycle_view import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.stencilview import StencilView
from kivy.effects.scroll import ScrollEffect
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp, sp
import requests
import json
import os

from threading import Thread

Builder.load_file(os.path.join(os.path.dirname(__file__), '../KivyFile/profile.kv'))


class MainProfileHeader(BoxLayout):
    pass


class ProfileAnchorLayout(AnchorLayout, StencilView):
    pass


class ProfileCustomCard(AnchorLayout):
    age = StringProperty('N/A')
    breed = StringProperty('N/A')
    city = StringProperty('N/A')
    color = StringProperty('N/A')
    date = StringProperty('N/A')
    gender = StringProperty('N/A')
    images = ObjectProperty([])
    name = StringProperty('N/A')
    petid = StringProperty('N/A')
    pet_size = StringProperty('N/A')
    state = StringProperty('N/A')
    status = StringProperty('N/A')
    summary = StringProperty('N/A')
    zip = StringProperty('N/A')
    icon = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.custom_image = None
        self.add_image()
        self.fbind('images', self.images_loaded)

    def images_loaded(self, instance, value):
        image = self.images[0]['image']
        self.custom_image.source = image
        self.custom_image.fbind('texture_size', self.update_size)

    def update_size(self, instance, value):
        instance.size = value

        if value[0] < dp(150) or value[1] < dp(134):
            if value[0] < value[1]:
                scale = 150 / value[0]
                instance.size = (dp(value[0] * scale), dp(value[1] * scale))
            elif value[1] < value[0]:
                scale = 134 / value[1]
                instance.size = (dp(value[0] * scale), dp(value[1] * scale))

    def add_image(self):
        self.custom_image = AsyncImage(size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, keep_ratio=True, allow_stretch=True, source=None)
        anchor_layout = ProfileAnchorLayout(size_hint=(None, None), size=(dp(150), dp(134)))
        anchor_layout.add_widget(self.custom_image)
        self.ids.photo.add_widget(anchor_layout)

    def delete_pet(self):
        print(self.petid)
        headers = {
            'Authorization': 'Token 9a5de7d01e1ce563e4a08a862bf68268128d6f87'
        }
        print(self.petid)
        r = requests.delete(url='https://fur-finder.herokuapp.com/api/pets//'+self.petid, headers=headers)
        self.parent.remove_widget(self)

class ProfileSelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass


class ProfileSelectableCard(RecycleDataViewBehavior, ProfileCustomCard):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(ProfileSelectableCard, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_up(self, touch):
        if super(ProfileSelectableCard, self).on_touch_up(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            self.selected = True
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        if self.selected:
            self.selected = False


class Profile(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    class CustomScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def listen(self, data):
            print(data)
            btn = Button(text=str(data), size_hint=(1, None), height=dp(40))
            self.children[0].children[0].children[0].add_widget(btn)

    class Header:
        def create(self):
            anchor_layout = AnchorLayout(size_hint=(1, 0.1), anchor_x='left', anchor_y='top', padding=(dp(20), dp(20), dp(0), dp(0)))
            header = Label(halign='left', valign='top', font_size=sp(20), color=get_color_from_hex('#023b80'), text='[font=assets/Inter-SemiBold.ttf]Profile Page', markup=True)
            header.bind(size=header.setter('text_size'))
            anchor_layout.add_widget(header)
            return anchor_layout

    class MidHead:
        def create(self):
            anchor_layout = AnchorLayout(size_hint=(1, 0.1), anchor_x='left', anchor_y='top', padding=(dp(20), dp(20), dp(0), dp(0)))
            header = Label(halign='left', valign='top', font_size=sp(20), color=get_color_from_hex('#023b80'), text='[font=assets/Inter-SemiBold.ttf]My Reported Pets', markup=True)
            header.bind(size=header.setter('text_size'))
            anchor_layout.add_widget(header)
            return anchor_layout


    class ProfileRV(RecycleView):
        root = ObjectProperty()

        def getReportedPetsFromBackend(self):
            s = requests.Session()
            s.hooks['response'].append(self.callback)
            headers = {
                'Authorization': 'Token 9a5de7d01e1ce563e4a08a862bf68268128d6f87'
            }

            pets = s.get(url='https://fur-finder.herokuapp.com/api/pets//', headers=headers).json()
            return pets

        def callback(self, r, **kwargs):
            if self.load:
                self.data.clear()
                self.refresh_from_data()
                pets_list = []
                #print(r.json())
                for pet in r.json():
                    if pet['author'] == self.author:
                        pets_list.append(pet)
                print(pets_list)
                print(self.author)
                for pet in reversed(pets_list):
                    self.data.append(
                        {
                            'age': pet['age'],
                            'breed': pet['breed'],
                            'city': pet['city'],
                            'color': pet['color'],
                            'date': pet['date'],
                            'gender': pet['gender'],
                            'images': pet['images'],
                            'name': pet['name'],
                            'petid': pet['petid'],
                            'pet_size': pet['size'],
                            'state': pet['state'],
                            'status': pet['status'].upper(),
                            'summary': pet['summary'],
                            'zip': pet['zip']
                        }
                    )
                self.refresh_done()

        def refresh_callback(self, *args):
            print('refreshed')

            def refresh_callback(interval):
                th = Thread(target=self.getReportedPetsFromBackend)
                th.setDaemon(True)
                th.start()

            Clock.schedule_once(refresh_callback, 1)

        def __init__(self, screen_manager=None, pets_list=None, author=None, **kwargs):
            super().__init__(**kwargs)
            self.load = False
            self.refresh_callback = self.refresh_callback
            self.root_layout = self.root
            self.author = author
            for pet in reversed(pets_list):
                self.data.append(
                    {
                        'age': pet['age'],
                        'breed': pet['breed'],
                        'city': pet['city'],
                        'color': pet['color'],
                        'date': pet['date'],
                        'gender': pet['gender'],
                        'images': pet['images'],
                        'name': pet['name'],
                        'petid': pet['petid'],
                        'pet_size': pet['size'],
                        'state': pet['state'],
                        'status': pet['status'].upper(),
                        'summary': pet['summary'],
                        'zip': pet['zip'],
                        'author': pet['author']
                    }
                )
            self.screen_manager = screen_manager
            self.load = True

    def create(self, data, author):
        screen_manager = ScreenManager(transition=SlideTransition(), size_hint=(1, 1))
        grid_layout = GridLayout(cols=1)
        anchor_layout = AnchorLayout(size_hint=(1, 0.9), padding=(dp(20), dp(0), dp(20), dp(0)))
        rv2 = self.ProfileRV(pets_list=data, author=author, smooth_scroll_end=dp(10), root=anchor_layout, screen_manager=screen_manager, size_hint=(1, 1), effect_cls=ScrollEffect, bar_inactive_color=(0, 0, 0, 0), bar_color=(0, 0, 0, 0))

        anchor_layout.add_widget(rv2)
        grid_layout.add_widget(MainProfileHeader())
        grid_layout.add_widget(anchor_layout)
        rv_screen = Screen(name='RV2')
        rv_screen.add_widget(grid_layout)
        screen_manager.add_widget(rv_screen)

        reported_screen = self.CustomScreen(name='Profile')
        reported_screen.add_widget(screen_manager)

        return reported_screen
