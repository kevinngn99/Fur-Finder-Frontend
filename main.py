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
from navigation import Navigation
from screen_manager import Screens
from jnius import cast
from jnius import autoclass

import requests
import json


class MyApp(App):

    def fidoFinder(self, zipCode):
        ArrayListHorizontalData = autoclass('org.recyclerview.ArrayListHorizontalData')
        HorizontalData = autoclass('org.recyclerview.HorizontalData')
        String = autoclass('java.lang.String')
        array_list_horizontal_data = ArrayListHorizontalData()
        url = 'https://fur-finder.herokuapp.com/api/fidofinder/' + str(zipCode) + '/'

        data = json.loads(requests.get(url).text)
        for dict in data:
            # print('------------------------------------------')
            # print('Name: ', dict['name'])
            # print('City: ', dict['city'])
            # print('Date: ', dict['date'])
            # print('Breed: ', dict['breed'])
            # print('Status: ', dict['status'])
            # print('Image: ', dict['image'])
            # print('PetID: ', dict['petid'])

            name = cast('java.lang.String', String(dict['name']))
            gender = cast('java.lang.String', String('Unknown'))
            status = cast('java.lang.String', String(dict['status']))
            image = cast('java.lang.String', String(dict['image']))

            horizontal_data = HorizontalData(name, gender, status, image)
            array_list_horizontal_data.addHorizontalData(horizontal_data)

        return array_list_horizontal_data

    def helpingLostPets(self, zipCode):
        ArrayListHorizontalData = autoclass('org.recyclerview.ArrayListHorizontalData')
        HorizontalData = autoclass('org.recyclerview.HorizontalData')
        String = autoclass('java.lang.String')
        array_list_horizontal_data = ArrayListHorizontalData()
        url = 'https://fur-finder.herokuapp.com/api/helpinglostpets/' + str(zipCode) + '/'

        data = json.loads(requests.get(url).text)
        for dict in data:
            # print('------------------------------------------')
            # print('Status: ', dict['status'])
            # print('Date: ', dict['date'])
            # print('Location: ', dict['location'])
            # print('Image: ', dict['image'])
            # print('Name: ', dict['name'])
            # print('Breed: ', dict['breed'])
            # print('Gender: ', dict['gender'])
            # print('Age: ', dict['age'])
            # print('Size: ', dict['size'])
            # print('Color: ', dict['color'])

            name = cast('java.lang.String', String(dict['name']))
            gender = cast('java.lang.String', String(dict['gender']))
            status = cast('java.lang.String', String(dict['status']))
            image = cast('java.lang.String', String(dict['image']))

            horizontal_data = HorizontalData(name, gender, status, image)
            array_list_horizontal_data.addHorizontalData(horizontal_data)

        return array_list_horizontal_data

    def lostMyDoggie(self, zipCode):
        ArrayListHorizontalData = autoclass('org.recyclerview.ArrayListHorizontalData')
        HorizontalData = autoclass('org.recyclerview.HorizontalData')
        String = autoclass('java.lang.String')
        array_list_horizontal_data = ArrayListHorizontalData()
        url = 'https://fur-finder.herokuapp.com/api/lostmydoggie/' + str(zipCode) + '/'

        data = json.loads(requests.get(url).text)
        for dict in data:
            # print('------------------------------------------')
            # print('Image: ', dict['image'])
            # print('Name: ', dict['name'])
            # print('Status: ', dict['status'])
            # print('Gender: ', dict['gender'])
            # print('Location: ', dict['location'])
            # print('Zip: ', dict['zip'])
            # print('Breed: ', dict['breed'])
            # print('Color: ', dict['color'])
            # print('Date: ', dict['date'])

            name = cast('java.lang.String', String(dict['name']))
            gender = cast('java.lang.String', String(dict['gender']))
            status = cast('java.lang.String', String(dict['status']))
            image = cast('java.lang.String', String(dict['image']))

            horizontal_data = HorizontalData(name, gender, status, image)
            array_list_horizontal_data.addHorizontalData(horizontal_data)

        return array_list_horizontal_data

    def pawBoost(self, zipCode):
        ArrayListHorizontalData = autoclass('org.recyclerview.ArrayListHorizontalData')
        HorizontalData = autoclass('org.recyclerview.HorizontalData')
        String = autoclass('java.lang.String')
        array_list_horizontal_data = ArrayListHorizontalData()
        url = 'https://fur-finder.herokuapp.com/api/pawboost/' + str(zipCode) + '/'

        data = json.loads(requests.get(url).text)
        for dict in data:
            # print('------------------------------------------')
            # print('Name: ', dict['name'])
            # print('Breed: ', dict['breed'])
            # print('Location: ', dict['location'])
            # print('Date: ', dict['date'])
            # print('PetID: ', dict['petid'])
            # print('Image: ', dict['image'])

            name = cast('java.lang.String', String(dict['name']))
            gender = cast('java.lang.String', String('Unknown'))
            status = cast('java.lang.String', String('Lost'))
            image = cast('java.lang.String', String(dict['image']))

            horizontal_data = HorizontalData(name, gender, status, image)
            array_list_horizontal_data.addHorizontalData(horizontal_data)

        return array_list_horizontal_data

    def petKey(self, zipCode):
        ArrayListHorizontalData = autoclass('org.recyclerview.ArrayListHorizontalData')
        HorizontalData = autoclass('org.recyclerview.HorizontalData')
        String = autoclass('java.lang.String')
        array_list_horizontal_data = ArrayListHorizontalData()
        url = 'https://fur-finder.herokuapp.com/api/petkey/' + str(zipCode) + '/'

        data = json.loads(requests.get(url).text)
        for dict in data:
            # print('------------------------------------------')
            # print('Name: ', dict['name'])
            # print('Breed: ', dict['breed'])
            # print('Age: ', dict['age'])
            # print('Gender: ', dict['gender'])
            # print('Color: ', dict['color'])
            # print('Image: ', dict['image'])

            name = cast('java.lang.String', String(dict['name']))
            gender = cast('java.lang.String', String(dict['gender']))
            status = cast('java.lang.String', String('Lost'))
            image = cast('java.lang.String', String(dict['image']))

            horizontal_data = HorizontalData(name, gender, status, image)
            array_list_horizontal_data.addHorizontalData(horizontal_data)

        return array_list_horizontal_data

    def tabbyTracker(self, zipCode):
        ArrayListHorizontalData = autoclass('org.recyclerview.ArrayListHorizontalData')
        HorizontalData = autoclass('org.recyclerview.HorizontalData')
        String = autoclass('java.lang.String')
        array_list_horizontal_data = ArrayListHorizontalData()
        url = 'https://fur-finder.herokuapp.com/api/tabbytracker/' + str(zipCode) + '/'

        data = json.loads(requests.get(url).text)
        for dict in data:
            # print('------------------------------------------')
            # print('Name: ', dict['name'])
            # print('Location: ', dict['location'])
            # print('Date: ', dict['date'])
            # print('Breed: ', dict['breed'])
            # print('Status: ', dict['status'])
            # print('Image: ', dict['image'])
            # print('PetID: ', dict['petid'])

            name = cast('java.lang.String', String(dict['name']))
            gender = cast('java.lang.String', String('Unknown'))
            status = cast('java.lang.String', String(dict['status']))
            image = cast('java.lang.String', String(dict['image']))

            horizontal_data = HorizontalData(name, gender, status, image)
            array_list_horizontal_data.addHorizontalData(horizontal_data)

        return array_list_horizontal_data

    def build(self):
        try:
            # REQUEST ANDROID LOCATION PERMISSIONS AND PERFORM DATA SCRAP BASED ON ZIP CODE #
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            SDLActivity = autoclass('org.libsdl.app.SDLActivity')
            Scrapers = autoclass('org.recyclerview.Scrapers')

            scrapers_list = Scrapers()
            scrapers_list.addScraper(self.fidoFinder(PythonActivity.zipCode))
            scrapers_list.addScraper(self.helpingLostPets(PythonActivity.zipCode))
            scrapers_list.addScraper(self.lostMyDoggie(PythonActivity.zipCode))
            scrapers_list.addScraper(self.pawBoost(PythonActivity.zipCode))
            scrapers_list.addScraper(self.petKey(PythonActivity.zipCode))
            scrapers_list.addScraper(self.tabbyTracker(PythonActivity.zipCode))

            SDLActivity.scrapersVariable.setScrapers(scrapers_list.getScrapers())
            # REQUEST ANDROID LOCATION PERMISSIONS AND PERFORM DATA SCRAP BASED ON ZIP CODE #
        except:
            print('Not an Android')

        box_layout = BoxLayout(orientation='vertical')
        screens = Screens().create()
        navigation = Navigation(screens).create()

        box_layout.add_widget(screens)
        box_layout.add_widget(navigation)

        return box_layout


if __name__ == '__main__':
    MyApp().run()
