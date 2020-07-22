from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty
from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.behaviors import FocusBehavior
from kivymd.app import MDApp
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.properties import StringProperty
from kivy.metrics import dp, sp
from screens.pet import Pet
import requests

import os

Builder.load_file(os.path.join(os.path.dirname(__file__), '../KivyFile/reported.kv'))


class CustomCard(AnchorLayout):
    age = StringProperty('N/A')
    breed = StringProperty('N/A')
    city = StringProperty('N/A')
    color = StringProperty('N/A')
    date = StringProperty('N/A')
    gender = StringProperty('N/A')
    images = []
    name = StringProperty('N/A')
    petid = StringProperty('N/A')
    pet_size = StringProperty('N/A')
    state = StringProperty('N/A')
    status = StringProperty('N/A')
    zip = StringProperty('N/A')
    icon = StringProperty('')


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

    def on_touch_down(self, touch):
        if super(SelectableCard, self).on_touch_down(touch):
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
            rv.screen_manager.get_screen('Pet').children[0].location = rv.data[index]['city'] + ', ' + rv.data[index]['state']
            rv.screen_manager.get_screen('Pet').children[0].name = rv.data[index]['name']
            rv.screen_manager.get_screen('Pet').children[0].petid = rv.data[index]['petid']
            rv.screen_manager.get_screen('Pet').children[0].pet_size = rv.data[index]['pet_size']
            rv.screen_manager.get_screen('Pet').children[0].status = rv.data[index]['status']
            rv.screen_manager.get_screen('Pet').children[0].zip = rv.data[index]['zip']
            rv.screen_manager.current = 'Pet'


def getReportedPetsFromBackend():
    data = requests.get(url='https://fur-finder.herokuapp.com/api/pets//').json()

    for i in range(len(data)):
        print(data[i])

    return data


class Reported(MDApp):
    class CustomScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def listen(self, data):
            print(data)

            btn = Button(text=str(data), size_hint=(1, None), height=dp(40))
            self.children[0].children[0].children[0].add_widget(btn)

    class Header:
        def create(self):
            anchor_layout = AnchorLayout(size_hint=(1, 0.1), anchor_x='left', anchor_y='top')

            header = Label(halign='left', valign='top', font_size=sp(20), color=get_color_from_hex('#023b80'), text='[font=assets/Inter-SemiBold.ttf]Reported Pets', markup=True)
            header.bind(size=header.setter('text_size'))

            anchor_layout.add_widget(header)
            return anchor_layout

    class RV(RecycleView):
        def __init__(self, screen_manager=None, **kwargs):
            super().__init__(**kwargs)
            pets=getReportedPetsFromBackend()
            self.data =[]
            for index in range(len(pets)):
                self.data.append({'age' : pets[index]["age"],
                                  'breed': pets[index]["breed"],
                                  'city': pets[index]["city"],
                                  'color': pets[index]["color"],
                                  'date': pets[index]["date"],
                                  'gender': pets[index]["gender"],
                                  'images': pets[index]["images"],
                                  'name': pets[index]["name"],
                                  'petid': pets[index]["petid"],
                                  'pet_size': pets[index]["size"],
                                  'state': pets[index]["state"],
                                  'status': pets[index]["status"].upper(),
                                  'zip': pets[index]["zip"]
                                  })



            self.screen_manager = screen_manager


    def create(self):
        screen_manager = ScreenManager(transition=SlideTransition(), size_hint=(1, 1))

        box_layout = BoxLayout(orientation='vertical', padding=(dp(20), dp(20), dp(20), dp(20)))
        header = self.Header().create()
        rv = self.RV(screen_manager=screen_manager, size_hint=(1, 0.9))
        box_layout.add_widget(header)
        box_layout.add_widget(rv)
        rv_screen = Screen(name='RV')
        rv_screen.add_widget(box_layout)

        pet_screen = Screen(name='Pet')
        pet_screen.add_widget(Pet().create(screen_manager))

        screen_manager.add_widget(rv_screen)
        screen_manager.add_widget(pet_screen)

        reported_screen = self.CustomScreen(name='Reported')
        reported_screen.add_widget(screen_manager)

        return reported_screen
