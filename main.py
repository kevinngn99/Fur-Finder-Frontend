import kivy
kivy.require('1.11.1')

from kivy.config import Config
Config.set('graphics', 'width', '375')
Config.set('graphics', 'height', '812')
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'multisamples', '5')

from kivy.core.window import Window
Window.clearcolor = (1, 1, 1, 1)

<<<<<<< HEAD
from kivymd.app import MDApp

Builder.load_string("""
#:include KivyFile/login.kv
#:include KivyFile/report.kv
#:include KivyFile/scroll.kv
""")

<<<<<<< Updated upstream
from kivy.uix.label import Label
=======
from kivy.app import App
>>>>>>> e631afbba8826dae696c418f8027cfbf7d24c340
from kivy.uix.boxlayout import BoxLayout
from navigation import Navigation
from screen_manager import Screens
from jnius import cast
from jnius import autoclass

import requests
import json


<<<<<<< HEAD
class TopPageReported(BoxLayout):
    pass


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
        #self.data = [{'text': str(x)} for x in range(50)]
        Clock.schedule_interval(self.update_data, 0.1)

        data = getRequest()
        self.data = [{'name_item': str(x['name']), 'gender_item': str(x['gender']), 'size_item': str(x['size']),
                       'date_item': str(x['date']), 'age_item': str(x['age']), 'state_item': str(x['state']),
                       'zip_item': str(x['zip']), 'location_item': str(x['location']), 'breed_item': str(x['breed'])} for x in
                    data]
    def update_data(self, *args):
        data = getRequest()
        self.data = [{'name_item': str(x['name']), 'gender_item': str(x['gender']), 'size_item': str(x['size']),
                      'date_item': str(x['date']), 'age_item': str(x['age']), 'state_item': str(x['state']),
                      'zip_item': str(x['zip']), 'location_item': str(x['location']), 'breed_item': str(x['breed'])}
                     for x in
                     data]
        #self.data = [{'text': val} for row in items for val in row.values()]


class ImageButton(ButtonBehavior, Image):
    pass


class BackgroundBox(BoxLayout):
    pass


class TopPage(BoxLayout):
    pass


class LoginView(Screen):
    pass


class ReportView(Screen):
    name_button = ObjectProperty(None)
    gender_button = ObjectProperty(None)
    size_button = ObjectProperty(None)
    age_button = ObjectProperty(None)
    state_button = ObjectProperty(None)
    zip_button = ObjectProperty(None)
    breed_button = ObjectProperty(None)
    calendar_button = ObjectProperty(None)
    postlist = []
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_button = None
        gender_items = [{'viewclass': 'MDMenuItem', 'text': 'Female'},
                        {'viewclass': 'MDMenuItem', 'text': 'Male'}]
        self.gender_menu = MDDropdownMenu(caller=self.gender_button, items=gender_items, width_mult=3,
                                          use_icon_item=False)

        age_items = [{'viewclass': 'MDMenuItem', 'text': f"{i+1}"} for i in range(20)]

        self.age_menu = MDDropdownMenu(caller=self.age_button, items=age_items, width_mult=2,
                                        use_icon_item=False)

        size_items = [{'viewclass': 'MDMenuItem', 'text': 'Small'},
                      {'viewclass': 'MDMenuItem', 'text': 'Medium'},
                      {'viewclass': 'MDMenuItem', 'text': 'Large'}]

        self.size_menu = MDDropdownMenu(caller=self.size_button, items=size_items, width_mult=2,
                                        use_icon_item=False)

        state_items = [
            {'viewclass': 'MDMenuItem', 'text': 'AL'},
            {'viewclass': 'MDMenuItem', 'text': 'AK'},
            {'viewclass': 'MDMenuItem', 'text': 'AS'},
            {'viewclass': 'MDMenuItem', 'text': 'AZ'},
            {'viewclass': 'MDMenuItem', 'text': 'AR'},
            {'viewclass': 'MDMenuItem', 'text': 'CA'},
            {'viewclass': 'MDMenuItem', 'text': 'CO'},
            {'viewclass': 'MDMenuItem', 'text': 'CT'},
            {'viewclass': 'MDMenuItem', 'text': 'DE'},
            {'viewclass': 'MDMenuItem', 'text': 'DC'},
            {'viewclass': 'MDMenuItem', 'text': 'FL'},
            {'viewclass': 'MDMenuItem', 'text': 'GA'},
            {'viewclass': 'MDMenuItem', 'text': 'GU'},
            {'viewclass': 'MDMenuItem', 'text': 'HI'},
            {'viewclass': 'MDMenuItem', 'text': 'ID'},
            {'viewclass': 'MDMenuItem', 'text': 'IL'},
            {'viewclass': 'MDMenuItem', 'text': 'IN'},
            {'viewclass': 'MDMenuItem', 'text': 'IA'},
            {'viewclass': 'MDMenuItem', 'text': 'KS'},
            {'viewclass': 'MDMenuItem', 'text': 'KY'},
            {'viewclass': 'MDMenuItem', 'text': 'LA'},
            {'viewclass': 'MDMenuItem', 'text': 'ME'},
            {'viewclass': 'MDMenuItem', 'text': 'MD'},
            {'viewclass': 'MDMenuItem', 'text': 'MA'},
            {'viewclass': 'MDMenuItem', 'text': 'MI'},
            {'viewclass': 'MDMenuItem', 'text': 'MN'},
            {'viewclass': 'MDMenuItem', 'text': 'MS'},
            {'viewclass': 'MDMenuItem', 'text': 'MO'},
            {'viewclass': 'MDMenuItem', 'text': 'MT'},
            {'viewclass': 'MDMenuItem', 'text': 'NE'},
            {'viewclass': 'MDMenuItem', 'text': 'NV'},
            {'viewclass': 'MDMenuItem', 'text': 'NH'},
            {'viewclass': 'MDMenuItem', 'text': 'NJ'},
            {'viewclass': 'MDMenuItem', 'text': 'NM'},
            {'viewclass': 'MDMenuItem', 'text': 'NY'},
            {'viewclass': 'MDMenuItem', 'text': 'NC'},
            {'viewclass': 'MDMenuItem', 'text': 'ND'},
            {'viewclass': 'MDMenuItem', 'text': 'MP'},
            {'viewclass': 'MDMenuItem', 'text': 'OH'},
            {'viewclass': 'MDMenuItem', 'text': 'OK'},
            {'viewclass': 'MDMenuItem', 'text': 'OR'},
            {'viewclass': 'MDMenuItem', 'text': 'PA'},
            {'viewclass': 'MDMenuItem', 'text': 'PR'},
            {'viewclass': 'MDMenuItem', 'text': 'RI'},
            {'viewclass': 'MDMenuItem', 'text': 'SC'},
            {'viewclass': 'MDMenuItem', 'text': 'SD'},
            {'viewclass': 'MDMenuItem', 'text': 'TN'},
            {'viewclass': 'MDMenuItem', 'text': 'TX'},
            {'viewclass': 'MDMenuItem', 'text': 'UT'},
            {'viewclass': 'MDMenuItem', 'text': 'VT'},
            {'viewclass': 'MDMenuItem', 'text': 'VI'},
            {'viewclass': 'MDMenuItem', 'text': 'VA'},
            {'viewclass': 'MDMenuItem', 'text': 'WA'},
            {'viewclass': 'MDMenuItem', 'text': 'WV'},
            {'viewclass': 'MDMenuItem', 'text': 'WI'},
            {'viewclass': 'MDMenuItem', 'text': 'WY'}
        ]
=======
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from navigation import Navigation
from screen_manager import Screens, ScreenManager
>>>>>>> Stashed changes

        self.state_menu = MDDropdownMenu(caller=self.state_button, items=state_items, width_mult=2,
                                        use_icon_item=False)

<<<<<<< Updated upstream
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
=======
class MyClass(MDApp):
    class CustomBoxLayout(BoxLayout):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            with self.canvas:
                Color(rgb=get_color_from_hex('#f6f7fb'))
                self._rect = Rectangle(size_hint=(None, None))
>>>>>>> Stashed changes

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        self.exit_manager(path)
        toast(path)

    def exit_manager(self, path):
        '''Called when the user reaches the root of the directory tree.'''
        print(path)
        #self.imgPath=path
        self.manager_open = False
        self.file_manager.close()
        return Image(source=path)

    datestr = "date"
    def get_date(self, date):
        self.datestr = str(date)
        toast("Date Missing: " + self.datestr, duration=3)
        #print(date)

    def date_picker(self):
        date_dialog = MDDatePicker(callback=self.get_date)
        date_dialog.open()

    def set_item(self):
        print("set_item")

    def post_report(self):
        print("post report")
        print(self.name_button.text)
        print(self.gender_button.text)
        print(self.size_button.text)
        print(self.datestr)
        print(self.age_button.text)
        print(self.state_button.text)
        print(self.zip_button.text)
        print(self.location_button.text)
        print(self.breed_button.text)
        self.postlist.append(self.name_button.text)
        self.postlist.append(self.gender_button.text)
        self.postlist.append(self.size_button.text)
        self.postlist.append(self.datestr)
        self.postlist.append(self.age_button.text)
        self.postlist.append(self.state_button.text)
        self.postlist.append(self.zip_button.text)
        self.postlist.append(self.location_button.text)
        self.postlist.append(self.breed_button.text)
        #TO DO
        #number authentication
        #blank authentication
        #default authentication



        #with open(self.imgPath, mode='rb') as file:
        #    img = file.read()
        post_data = {

            'name': self.postlist[0],
            'gender': self.postlist[1],
            'size': self.postlist[2],
            'date': self.postlist[3],
            'age': self.postlist[4],
            'state': self.postlist[5],
            'zip': self.postlist[6],
            'location': self.postlist[7],
            'breed': self.postlist[8],

        }

        requests.post(url='http://10.253.253.111:8000/api/pets/', data=post_data)


class MyApp(MDApp):
    def home_callback(self, screen_manager):
        print('The home button is being pressed')
        screen_manager.current = 'Home'

    def report_callback(self, screen_manager):
        print('The report button is being pressed')
        screen_manager.current = 'Report'

    def message_callback(self, screen_manager):
        print('The message button is being pressed')
        screen_manager.current = 'Message'

    def scroll_callback(self, screen_manager):
        print('The scroll page button is being pressed')
        if getRequest():
            print("there is data when pressed")
        screen_manager.current = 'Scroll'


    def set_item(self, instance):
        print("set item")
=======
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
>>>>>>> e631afbba8826dae696c418f8027cfbf7d24c340

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
