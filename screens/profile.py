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


class CustomAnchorLayout(AnchorLayout, StencilView):
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
    icon = StringProperty('')

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
        anchor_layout = CustomAnchorLayout(size_hint=(None, None), size=(dp(150), dp(134)))
        anchor_layout.add_widget(self.custom_image)
        self.ids.photo.add_widget(anchor_layout)


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
        if rv.screen_manager.current == 'RV' and self.selected:
            rv.screen_manager.get_screen('Pet').children[0].age = rv.data[index]['age']
            rv.screen_manager.get_screen('Pet').children[0].breed = rv.data[index]['breed']
            rv.screen_manager.get_screen('Pet').children[0].color = rv.data[index]['color']
            rv.screen_manager.get_screen('Pet').children[0].date = rv.data[index]['date']
            rv.screen_manager.get_screen('Pet').children[0].gender = rv.data[index]['gender']
            rv.screen_manager.get_screen('Pet').children[0].images = rv.data[index]['images']
            rv.screen_manager.get_screen('Pet').children[0].location = rv.data[index]['city'] + ', ' + rv.data[index]['state']
            rv.screen_manager.get_screen('Pet').children[0].name = rv.data[index]['name']
            rv.screen_manager.get_screen('Pet').children[0].petid = rv.data[index]['petid']
            rv.screen_manager.get_screen('Pet').children[0].pet_size = rv.data[index]['pet_size']
            rv.screen_manager.get_screen('Pet').children[0].status = rv.data[index]['status']
            rv.screen_manager.get_screen('Pet').children[0].summary = rv.data[index]['summary']
            rv.screen_manager.get_screen('Pet').children[0].zip = rv.data[index]['zip']
            rv.screen_manager.current = 'Pet'
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
            anchor_layout = AnchorLayout(size_hint=(1, 0.2), anchor_x='left', anchor_y='top', padding=(dp(20), dp(20), dp(20), dp(0)))
            header = Label(halign='left', valign='top', font_size=sp(20), color=get_color_from_hex('#023b80'), text='[font=assets/Inter-SemiBold.ttf]Profile Page', markup=True)
            header.bind(size=header.setter('text_size'))
            anchor_layout.add_widget(header)
            return anchor_layout

    class MidHead:
        def create(self):
            anchor_layout = AnchorLayout(size_hint=(1, 0.3), anchor_x='left', anchor_y='top', padding=(dp(20), dp(20), dp(20), dp(0)))
            header = Label(halign='left', valign='top', font_size=sp(20), color=get_color_from_hex('#023b80'), text='[font=assets/Inter-SemiBold.ttf]My Reported Pets', markup=True)
            header.bind(size=header.setter('text_size'))
            anchor_layout.add_widget(header)
            return anchor_layout

    class LastHead:
        def create(self):
            anchor_layout = AnchorLayout(size_hint=(1, 0.3), anchor_x='left', anchor_y='top', padding=(dp(20), dp(20), dp(20), dp(0)))
            header = Label(halign='left', valign='top', font_size=sp(20), color=get_color_from_hex('#023b80'), text='[font=assets/Inter-SemiBold.ttf]My Pinned Pets', markup=True)
            header.bind(size=header.setter('text_size'))
            anchor_layout.add_widget(header)
            return anchor_layout

    class ProfileRV2(RecycleView):
        root = ObjectProperty()

        def getReportedPetsFromBackend(self):
            s = requests.Session()
            s.hooks['response'].append(self.callback)
            headers = {
                'Authorization': 'Token 9a5de7d01e1ce563e4a08a862bf68268128d6f87'
            }

            data = s.get(url='https://fur-finder.herokuapp.com/api/pets//', headers=headers).json()

            return data

        def callback(self, r, **kwargs):
            if self.load:
                self.data.clear()
                self.refresh_from_data()
                for pet in reversed(r.json()):
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

        def __init__(self, screen_manager=None, pets_list=None, **kwargs):
            super().__init__(**kwargs)
            self.load = False
            self.refresh_callback = self.refresh_callback
            self.root_layout = self.root
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

    def create(self, data):
        print("hey")
        print(data)
        screen_manager = ScreenManager(transition=SlideTransition(), size_hint=(1, 1))
        box_layout = BoxLayout(orientation='vertical')
        grid_layout = GridLayout(cols=1)
        header = self.Header().create()
        midhead = self.MidHead().create()
        lasthead = self.LastHead().create()
        anchor_layout = AnchorLayout(size_hint=(1, 0.9), padding=(dp(20), dp(0), dp(20), dp(0)))
        anchor_layout2 = AnchorLayout(size_hint=(1, 0.9), padding=(dp(20), dp(0), dp(20), dp(0)))
        rv2 = self.ProfileRV2(pets_list=data, smooth_scroll_end=dp(10), root=anchor_layout, screen_manager=screen_manager, size_hint=(1, 1), effect_cls=ScrollEffect, bar_inactive_color=(0, 0, 0, 0), bar_color=(0, 0, 0, 0))
        rv3 = self.ProfileRV2(pets_list=data, smooth_scroll_end=dp(10), root=anchor_layout, screen_manager=screen_manager, size_hint=(1, 1), effect_cls=ScrollEffect, bar_inactive_color=(0, 0, 0, 0), bar_color=(0, 0, 0, 0))

        anchor_layout.add_widget(rv2)
        anchor_layout2.add_widget(rv3)

        grid_layout.add_widget(header)
        grid_layout.add_widget(midhead)
        grid_layout.add_widget(anchor_layout)
        grid_layout.add_widget(lasthead)
        grid_layout.add_widget(anchor_layout2)
        rv_screen = Screen(name='RV')
        rv_screen.add_widget(grid_layout)

        #pet_screen = Screen(name='Pet')
        #pet_screen.add_widget(Pet().create(screen_manager))

        screen_manager.add_widget(rv_screen)
        #screen_manager.add_widget(pet_screen)

        reported_screen = self.CustomScreen(name='Profile')
        reported_screen.add_widget(screen_manager)

        return reported_screen