from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.uix.button import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.carousel import Carousel
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.stencilview import StencilView
from kivy.properties import ColorProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.metrics import dp, sp
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), '../KivyFile/pet.kv'))


class PinButton(AnchorLayout):
    text = StringProperty('')
    icon = StringProperty('')
    color = ColorProperty()


class MessageButton(AnchorLayout):
    text = StringProperty('')
    icon = StringProperty('')
    color = ColorProperty()


class BackButton(ButtonBehavior, AnchorLayout):
    icon = StringProperty('')


class CustomFloatLayout(BoxLayout):
    age = StringProperty('N/A')
    breed = StringProperty('N/A')
    color = StringProperty('N/A')
    date = StringProperty('N/A')
    gender = StringProperty('N/A')
    images = []
    location = StringProperty('N/A')
    name = StringProperty('N/A')
    petid = StringProperty('N/A')
    pet_size = StringProperty('N/A')
    status = StringProperty('N/A')
    zip = StringProperty('N/A')


class CustomLabel(Label):
    type = StringProperty()
    txt = StringProperty()


class CustomName(Label):
    name = StringProperty()


class SummaryLabel(Label):
    pass


class Pet:
    class Top:
        def __init__(self):
            self._box_layout = None

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

        class Indicator(Widget):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                with self.canvas.before:
                    Color(rgb=get_color_from_hex('#FFFFFF'))
                    self._rect = RoundedRectangle(size_hint=self.size_hint, size=self.size, radius=(dp(5), dp(5), dp(5), dp(5)))

            def pos_callback(self, instance, value):
                self._rect.pos = value

        def index_callback(self, instance, value):
            length = len(self._box_layout.children)

            previous = length - value - 1 + 1
            current = length - value - 1 + 0
            next = length - value - 1 - 1

            if previous < length:
                self._box_layout.children[previous].opacity = 0.5
            self._box_layout.children[current].opacity = 1
            if next >= 0:
                self._box_layout.children[next].opacity = 0.5

        def create(self):
            anchor_layout = AnchorLayout(size_hint=(1, 1), anchor_x='center', anchor_y='bottom')

            carousel = Carousel()
            for i in range(4):
                image = None
                if i == 0:
                    image = 'images/pup.jpg'
                elif i == 1:
                    image = 'images/more.jpg'
                elif i == 2:
                    image = 'images/doge.jpg'
                elif i == 3:
                    image = 'images/other.jpg'

                layout = self.CustomStencilView()
                layout.add_widget(self.CustomImage(size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, keep_ratio=True, allow_stretch=True, source=image))
                carousel.add_widget(layout)
            carousel.fbind('index', self.index_callback)

            indicator_layout = AnchorLayout(size_hint=(1, None), height=dp(30), anchor_x='center', anchor_y='center', padding=(dp(0), dp(0), dp(0), dp(20)))
            self._box_layout = BoxLayout(orientation='horizontal', size_hint=(None, 1), spacing=dp(5))
            self._box_layout.bind(minimum_width=self._box_layout.setter('width'))
            for i in range(4):
                if i == 0:
                    indicator = self.Indicator(opacity=1, size_hint=(None, None), size=(dp(10), dp(10)))
                    indicator.bind(pos=indicator.pos_callback)
                    self._box_layout.add_widget(indicator)
                else:
                    indicator = self.Indicator(opacity=0.5, size_hint=(None, None), size=(dp(10), dp(10)))
                    indicator.bind(pos=indicator.pos_callback)
                    self._box_layout.add_widget(indicator)
            indicator_layout.add_widget(self._box_layout)

            anchor_layout.add_widget(carousel)
            anchor_layout.add_widget(indicator_layout)

            return anchor_layout

    def create(self, screen_manager):
        float_layout = CustomFloatLayout(orientation='vertical')

        top_layout = AnchorLayout(size_hint=(1, 0.4), anchor_x='center', anchor_y='top')
        top = self.Top().create()
        button_layout = AnchorLayout(size_hint=(1, 1), padding=(dp(20), dp(20), dp(20), dp(20)), anchor_x='left', anchor_y='top', opacity=0.5)
        back_button = BackButton()
        back_button.bind(on_release=lambda instance: setattr(screen_manager, 'current', 'RV'))
        button_layout.add_widget(back_button)
        top.add_widget(button_layout)
        top_layout.add_widget(top)

        background = AnchorLayout(size_hint=(1, 1), anchor_x='center', anchor_y='center')
        vertical_scroll_view = ScrollView(do_scroll=(False, True), size_hint=(1, 1), bar_inactive_color=(0, 0, 0, 0))
        vertical_grid_layout = GridLayout(cols=1, size_hint=(1, None), padding=(dp(20), dp(20), dp(20), dp(20)))
        vertical_grid_layout.bind(minimum_height=vertical_grid_layout.setter('height'))
        details_layout = StackLayout(size_hint=(1, None), spacing=dp(20), padding=(dp(0), dp(20), dp(0), dp(0)))
        details_layout.bind(minimum_height=details_layout.setter('height'))

        age = CustomLabel(type='Age', txt=str(float_layout.age))
        float_layout.bind(age=lambda instance, value: setattr(age, 'txt', value))

        breed = CustomLabel(type='Breed', txt=str(float_layout.breed))
        float_layout.bind(breed=lambda instance, value: setattr(breed, 'txt', value))

        location = CustomLabel(type='Location', txt=str(float_layout.location))
        float_layout.bind(location=lambda instance, value: setattr(location, 'txt', value))

        color = CustomLabel(type='Color', txt=str(float_layout.color))
        float_layout.bind(color=lambda instance, value: setattr(color, 'txt', value))

        date = CustomLabel(type='Date', txt=str(float_layout.date))
        float_layout.bind(date=lambda instance, value: setattr(date, 'txt', value))

        gender = CustomLabel(type='Gender', txt=str(float_layout.gender))
        float_layout.bind(gender=lambda instance, value: setattr(gender, 'txt', value))

        petid = CustomLabel(type='Pet ID', txt=str(float_layout.petid))
        float_layout.bind(petid=lambda instance, value: setattr(petid, 'txt', value))

        size = CustomLabel(type='Size', txt=str(float_layout.pet_size))
        float_layout.bind(pet_size=lambda instance, value: setattr(size, 'txt', value))

        status = CustomLabel(type='Status', txt=str(float_layout.status))
        float_layout.bind(status=lambda instance, value: setattr(status, 'txt', value.title()))

        zip = CustomLabel(type='Zip', txt=str(float_layout.zip))
        float_layout.bind(zip=lambda instance, value: setattr(zip, 'txt', value))

        details_layout.add_widget(age)
        details_layout.add_widget(breed)
        details_layout.add_widget(location)
        details_layout.add_widget(color)
        details_layout.add_widget(date)
        details_layout.add_widget(gender)
        details_layout.add_widget(petid)
        details_layout.add_widget(size)
        details_layout.add_widget(status)
        details_layout.add_widget(zip)

        name_layout = AnchorLayout(size_hint=(1, None), height=dp(30), anchor_x='center', anchor_y='center')
        pet_name = CustomName(name=str(float_layout.name))
        float_layout.bind(name=lambda instance, value: setattr(pet_name, 'name', value))
        pet_name.bind(size=pet_name.setter('text_size'))
        name_layout.add_widget(pet_name)

        summary_layout = AnchorLayout(size_hint=(1, None), height=dp(42), anchor_x='center', anchor_y='center', padding=(dp(0), dp(0), dp(0), dp(20)))
        summary = Label(halign='left', valign='center', text='[color=6e7c97][size=' + str(int(dp(16))) + '][font=assets/Inter-SemiBold.ttf]Summary',markup=True)
        summary.bind(size=summary.setter('text_size'))
        summary_layout.add_widget(summary)

        vertical_grid_layout.add_widget(name_layout)
        vertical_grid_layout.add_widget(details_layout)
        vertical_grid_layout.add_widget(summary_layout)
        vertical_grid_layout.add_widget(SummaryLabel())

        vertical_scroll_view.add_widget(vertical_grid_layout)
        background.add_widget(vertical_scroll_view)

        bottom_layout = AnchorLayout(size_hint=(1, 0.5), anchor_x='center', anchor_y='bottom')
        bottom_layout.add_widget(background)

        pin_and_message_layout = BoxLayout(size_hint=(1, None), height=dp(45), orientation='horizontal')
        pin_and_message_layout.add_widget(PinButton(icon='', text='Pin', color=get_color_from_hex('#e01646'), padding=(dp(20), dp(0), dp(7), dp(0))))
        pin_and_message_layout.add_widget(MessageButton(icon='', text='Message', color=get_color_from_hex('#023b80'), padding=(dp(0), dp(0), dp(20), dp(0))))

        float_layout.add_widget(top_layout)
        float_layout.add_widget(bottom_layout)
        float_layout.add_widget(pin_and_message_layout)

        return float_layout
