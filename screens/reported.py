from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty
from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.togglebutton import ToggleButton
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
from kivy.graphics.stencil_instructions import StencilPop, StencilUse, StencilUnUse, StencilPush
from kivy.metrics import dp, sp
from screens.pet import Pet
import requests
import json

import os
from threading import Thread

Builder.load_file(os.path.join(os.path.dirname(__file__), '../KivyFile/reported.kv'))


class WickedAnchorLayout(AnchorLayout, StencilView):
    pass


class CustomCard(AnchorLayout):
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
    author = StringProperty('N/A')
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
        self.custom_image = AsyncImage(size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                       keep_ratio=True, allow_stretch=True, source=None)
        anchor_layout = WickedAnchorLayout(size_hint=(None, None), size=(dp(150), dp(134)))
        anchor_layout.add_widget(self.custom_image)
        self.ids.photo.add_widget(anchor_layout)


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass


class SelectableCard(RecycleDataViewBehavior, CustomCard):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableCard, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_up(self, touch):
        if super(SelectableCard, self).on_touch_up(touch):
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
            rv.screen_manager.get_screen('Pet').children[0].location = rv.data[index]['city'] + ', ' + rv.data[index][
                'state']
            rv.screen_manager.get_screen('Pet').children[0].name = rv.data[index]['name']
            rv.screen_manager.get_screen('Pet').children[0].petid = rv.data[index]['petid']
            rv.screen_manager.get_screen('Pet').children[0].pet_size = rv.data[index]['pet_size']
            rv.screen_manager.get_screen('Pet').children[0].status = rv.data[index]['status']
            rv.screen_manager.get_screen('Pet').children[0].summary = rv.data[index]['summary']
            rv.screen_manager.get_screen('Pet').children[0].zip = rv.data[index]['zip']
            rv.screen_manager.get_screen('Pet').children[0].author = rv.data[index]['author']
            rv.screen_manager.current = 'Pet'
            self.selected = False


def filterBackend(male, female, lost, found):
    headers = {
        'Authorization': 'Token 9a5de7d01e1ce563e4a08a862bf68268128d6f87'
    }
    data = requests.get(url='https://fur-finder.herokuapp.com/api/pets//', headers=headers).json()
    newdata = []
    if male == True:
        gender = "Male"
    else:
        gender = "Female"
    if female == True:
        gender = "Female"
    else:
        gender = "Male"
    if lost == True:
        status = "Lost"
    else:
        status = "Found"
    if found == True:
        status = "Found"
    else:
        status = "Lost"
    for pet in reversed(data):

        if (pet['gender'] == gender and pet["status"] == status):
            newdata.append(
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
    return newdata


class Reported(MDApp):
    stateOfFilter = [True, True, True, False]

    class CustomScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def listen(self, data):
            print(data)

            btn = Button(text=str(data), size_hint=(1, None), height=dp(40))
            self.children[0].children[0].children[0].add_widget(btn)

    class Header:
        def create(self):
            anchor_layout = AnchorLayout(size_hint=(1, 0.1), anchor_x='left', anchor_y='top',
                                         padding=(dp(20), dp(20), dp(20), dp(0)))

            header = Label(halign='left', valign='top', font_size=sp(20), color=get_color_from_hex('#023b80'),
                           text='[font=assets/Inter-SemiBold.ttf]Reported Pets', markup=True)
            header.bind(size=header.setter('text_size'))

            anchor_layout.add_widget(header)
            return anchor_layout

    class RV(RecycleView):
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
                            'zip': pet['zip'],
                            'author': pet['author']
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

        def __init__(self, screen_manager=None, **kwargs):
            super().__init__(**kwargs)
            self.load = False
            self.data = []
            pets = self.getReportedPetsFromBackend()
            self.refresh_callback = self.refresh_callback
            self.root_layout = self.root
            for pet in reversed(pets):
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

    def __init__(self, root_sm=None, **kwargs):
        super().__init__(**kwargs)
        self.root_sm = root_sm

    def stateOfButtons(self, instance, value, rv=None):
        print(instance.text, value)  # male,female,lost,found
        if instance.text == "Found" and value == "down":
            self.stateOfFilter[3] = True
            self.stateOfFilter[2] = False

        if instance.text == "Male" and value == "down":
            self.stateOfFilter[0] = True
            self.stateOfFilter[1] = False

        if instance.text == "Female" and value == "down":
            self.stateOfFilter[0] = False
            self.stateOfFilter[1] = True

        if instance.text == "Lost" and value == "down":
            self.stateOfFilter[2] = True
            self.stateOfFilter[3] = False

        rv.data.clear()
        rv.refresh_from_data()
        data = filterBackend(self.stateOfFilter[0], self.stateOfFilter[1], self.stateOfFilter[2], self.stateOfFilter[3])
        print(data)
        for pet in reversed(data):
            rv.data.append(
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
                    'pet_size': pet['pet_size'],
                    'state': pet['state'],
                    'status': pet['status'].upper(),
                    'summary': pet['summary'],
                    'zip': pet['zip'],
                    'author': pet['author']
                }
            )

    def create(self):
        screen_manager = ScreenManager(transition=SlideTransition(), size_hint=(1, 1))

        box_layout = BoxLayout(orientation='vertical')
        header = self.Header().create()
        anchor_layout = AnchorLayout(size_hint=(1, 0.9), padding=(dp(20), dp(20), dp(20), dp(20)))
        rv = self.RV(smooth_scroll_end=dp(10), root=anchor_layout, screen_manager=screen_manager, size_hint=(1, 1),
                     effect_cls=ScrollEffect, bar_inactive_color=(0, 0, 0, 0), bar_color=(0, 0, 0, 0))
        anchor_layout.add_widget(rv)
        box_layout.add_widget(header)

        filter_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        foundBtn = ToggleButton(text="Found", group="status", background_normal='',
                                background_color=get_color_from_hex('#023b80'), font_name='assets/Inter-Medium.ttf')

        foundBtn.fbind('state', self.stateOfButtons, rv=rv)
        lostBtn = ToggleButton(text="Lost", group="status", background_normal='',
                               background_color=get_color_from_hex('#023b80'), font_name='assets/Inter-Medium.ttf')

        lostBtn.fbind('state', self.stateOfButtons, rv=rv)
        femaleBtn = ToggleButton(text="Female", group="gender", background_normal='',
                                 background_color=get_color_from_hex('#023b80'), font_name='assets/Inter-Medium.ttf')

        femaleBtn.fbind('state', self.stateOfButtons, rv=rv)
        maleBtn = ToggleButton(text="Male", group="gender", background_normal='',
                               background_color=get_color_from_hex('#023b80'), font_name='assets/Inter-Medium.ttf')

        maleBtn.fbind('state', self.stateOfButtons, rv=rv)
        filter_layout.add_widget(foundBtn)
        filter_layout.add_widget(lostBtn)
        filter_layout.add_widget(femaleBtn)
        filter_layout.add_widget(maleBtn)

        box_layout.add_widget(filter_layout)
        box_layout.add_widget(anchor_layout)

        rv_screen = Screen(name='RV')
        rv_screen.add_widget(box_layout)

        pet_screen = Screen(name='Pet')
        pet_screen.add_widget(Pet(root_sm=self.root_sm).create(screen_manager))

        screen_manager.add_widget(rv_screen)
        screen_manager.add_widget(pet_screen)

        reported_screen = self.CustomScreen(name='Reported')
        reported_screen.add_widget(screen_manager)

        return reported_screen
