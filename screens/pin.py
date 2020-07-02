from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp, sp
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.clock import Clock
from kivy.uix.recycleview import RecycleView
from kivy.properties import BooleanProperty
import os
import requests
import json

Builder.load_file(os.path.join(os.path.dirname(__file__), '../KivyFile/scroll.kv'))


class TopPageReported(BoxLayout):
    pass


def getRequest():
    resp = requests.get(url='https://fur-finder.herokuapp.com/api/pets//')
    # print(resp.status_code)
    print("updating scroll page")
    data = resp.json()
    return data


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)


class RecyView(RecycleView):
    def __init__(self, **kwargs):
        super(RecyView, self).__init__(**kwargs)
        data = getRequest()

        self.data = [{'name_item': str(x['name']), 'gender_item': str(x['gender']), 'size_item': str(x['size']),
                       'date_item': str(x['date']), 'age_item': str(x['age']), 'state_item': str(x['state']),
                       'zip_item': str(x['zip']), 'location_item': str(x['location']), 'breed_item': str(x['breed'])} for x in
                   data]

    #def update_clock(self):
        #Clock.schedule_once(self.update_data, -1)
        #self.data.refresh_from_data()
        #print("updating clock")

    def update_data(self, *args):
        data = getRequest()
        self.data = [{'name_item': str(x['name']), 'gender_item': str(x['gender']), 'size_item': str(x['size']),
                      'date_item': str(x['date']), 'age_item': str(x['age']), 'state_item': str(x['state']),
                      'zip_item': str(x['zip']), 'location_item': str(x['location']), 'breed_item': str(x['breed'])}
                     for x in
                     data]
        print("updating data")


class Pin:
    class Header:
        def create(self):
            header = Label(size_hint=(1, None), height=dp(50), halign='left', valign='center', font_size=sp(40), color=get_color_from_hex('#150470'), text='[font=assets/Inter-SemiBold.ttf]Pinned', markup=True)
            header.bind(size=header.setter('text_size'))
            return header

    def __init__(self):
        super().__init__

    def create(self):
        pin_screen = Screen(name='Pin')
        pin_screen.add_widget(TopPageReported())

        return pin_screen
