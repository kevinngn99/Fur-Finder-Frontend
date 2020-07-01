import kivy
kivy.require('1.11.1')

from kivy.config import Config

Config.set('graphics', 'width', '375')
Config.set('graphics', 'height', '812')
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'multisamples', '5')

from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from jnius import cast
from jnius import autoclass
from navigation import Navigation
from screen_manager import Screens
import requests
import json


class MyApp(App):
    def callback_pos(self, instance, value):
        instance.rect.pos = value

    def scale(self):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            DisplayMetrics = autoclass('android.util.DisplayMetrics')
            displayMetrics = DisplayMetrics()
            currentActivity.getWindowManager().getDefaultDisplay().getMetrics(displayMetrics)

            width = displayMetrics.widthPixels
            height = displayMetrics.heightPixels - dp(24)

            print('The width of this android device is:', width)
            print('The height of this android device is:', height)

            ratio_width = width / 375
            ratio_height = height / 812

            return width, height, ratio_height, ratio_width
        except:
            print('Not an android device')
            return 375, 812, 1, 1

    def fidoFinder(self):
        data = json.loads(requests.get('https://fur-finder.herokuapp.com/api/fidofinder/33990/').text)
        for dict in data:
            print('------------------------------------------')
            print('Name: ', dict['name'])
            print('City: ', dict['city'])
            print('Date: ', dict['date'])
            print('Breed: ', dict['breed'])
            print('Status: ', dict['status'])
            print('Image: ', dict['image'])
            print('PetID: ', dict['petid'])

    def helpingLostPets(self):
        data = json.loads(requests.get('https://fur-finder.herokuapp.com/api/helpinglostpets/33990/').text)
        for dict in data:
            print('------------------------------------------')
            print('Status: ', dict['status'])
            print('Date: ', dict['date'])
            print('Location: ', dict['location'])
            print('Image: ', dict['image'])
            print('Name: ', dict['name'])
            print('Breed: ', dict['breed'])
            print('Gender: ', dict['gender'])
            print('Age: ', dict['age'])
            print('Size: ', dict['size'])
            print('Color: ', dict['color'])

    def lostMyDoggie(self):
        data = json.loads(requests.get('https://fur-finder.herokuapp.com/api/lostmydoggie/33990/').text)
        for dict in data:
            print('------------------------------------------')
            print('Image: ', dict['image'])
            print('Name: ', dict['name'])
            print('Status: ', dict['status'])
            print('Gender: ', dict['gender'])
            print('Location: ', dict['location'])
            print('Zip: ', dict['zip'])
            print('Breed: ', dict['breed'])
            print('Color: ', dict['color'])
            print('Date: ', dict['date'])

    def pawBoost(self):
        data = json.loads(requests.get('https://fur-finder.herokuapp.com/api/pawboost/33990/').text)
        for dict in data:
            print('------------------------------------------')
            print('Name: ', dict['name'])
            print('Breed: ', dict['breed'])
            print('Location: ', dict['location'])
            print('Date: ', dict['date'])
            print('PetID: ', dict['petid'])
            print('Image: ', dict['image'])

    def petKey(self):
        data = json.loads(requests.get('https://fur-finder.herokuapp.com/api/petkey/33990/').text)
        for dict in data:
            print('------------------------------------------')
            print('Name: ', dict['name'])
            print('Breed: ', dict['breed'])
            print('Age: ', dict['age'])
            print('Gender: ', dict['gender'])
            print('Color: ', dict['color'])
            print('Image: ', dict['image'])

    def tabbyTracker(self):
        data = json.loads(requests.get('https://fur-finder.herokuapp.com/api/tabbytracker/33990/').text)
        for dict in data:
            print('------------------------------------------')
            print('Name: ', dict['name'])
            print('Location: ', dict['location'])
            print('Date: ', dict['date'])
            print('Breed: ', dict['breed'])
            print('Status: ', dict['status'])
            print('Image: ', dict['image'])
            print('PetID: ', dict['petid'])

    def build(self):
        self.tabbyTracker()

        box_layout = BoxLayout(orientation='vertical')
        screens = Screens().create()
        navigation = Navigation(screens).create()

        box_layout.add_widget(screens)
        box_layout.add_widget(navigation)

        return box_layout

if __name__ == '__main__':
    MyApp().run()

#return Label(text='[color=150470]Fur Finder', font_name='DM-Serif-Display-Regular.ttf', font_size='50', markup=True)
