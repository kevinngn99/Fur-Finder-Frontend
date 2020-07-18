from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.carousel import Carousel
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.utils import get_color_from_hex
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.stencilview import StencilView
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.metrics import dp, sp
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), '../screens/my.kv'))


class CustomLabel(Label):
    type = StringProperty()
    txt = StringProperty()


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
            anchor_layout = AnchorLayout(size_hint=(1, 0.4), anchor_x='center', anchor_y='bottom')

            carousel = Carousel()
            for i in range(10):
                layout = self.CustomStencilView()
                layout.add_widget(self.CustomImage(size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, keep_ratio=True, allow_stretch=True, source='images/aussie.jpg'))
                carousel.add_widget(layout)
            carousel.fbind('index', self.index_callback)

            indicator_layout = AnchorLayout(size_hint=(1, None), height=dp(30), anchor_x='center', anchor_y='center', padding=(dp(0), dp(0), dp(0), dp(20)))
            self._box_layout = BoxLayout(orientation='horizontal', size_hint=(None, 1), spacing=dp(5))
            self._box_layout.bind(minimum_width=self._box_layout.setter('width'))
            for i in range(10):
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

    class Bottom:
        class Background(AnchorLayout):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                with self.canvas.before:
                    Color(rgb=get_color_from_hex('#FFFFFF'))
                    self._rect = RoundedRectangle(radius=(dp(30), dp(30), dp(0), dp(0)))

            def size_callback(self, instance, value):
                self._rect.size = value

        def create(self):
            background = self.Background(size_hint=(1, 0.6), anchor_x='center', anchor_y='center')
            background.bind(size=background.size_callback)

            vertical_scroll_view = ScrollView(do_scroll=(False, True), size_hint=(1, 1), bar_inactive_color=(0, 0, 0, 0))
            vertical_grid_layout = GridLayout(cols=1, size_hint=(1, None), padding=(dp(20), dp(20), dp(20), dp(20)))
            vertical_grid_layout.bind(minimum_height=vertical_grid_layout.setter('height'))
            details_layout = StackLayout(size_hint=(1, None), spacing=dp(20), padding=(dp(0), dp(20), dp(0), dp(0)))
            details_layout.bind(minimum_height=details_layout.setter('height'))
            details_layout.add_widget(CustomLabel(type='Status', txt='Lost'))
            details_layout.add_widget(CustomLabel(type='Breed', txt='Australian Shepard'))
            details_layout.add_widget(CustomLabel(type='Gender', txt='Female'))
            details_layout.add_widget(CustomLabel(type='Color', txt='Brown'))
            details_layout.add_widget(CustomLabel(type='Size', txt='Medium'))
            details_layout.add_widget(CustomLabel(type='Location', txt='Gainesville, FL'))
            details_layout.add_widget(CustomLabel(type='Zip', txt='32601'))
            details_layout.add_widget(CustomLabel(type='Reported', txt='Dec 16, 2020'))

            name_layout = AnchorLayout(size_hint=(1, None), height=dp(30), anchor_x='center', anchor_y='center')
            pet_name = Label(halign='left', valign='center', text='[color=150470][size='+str(int(dp(25)))+'][font=assets/Inter-Bold.ttf]Daisy', markup=True)
            pet_name.bind(size=pet_name.setter('text_size'))
            name_layout.add_widget(pet_name)

            summary_layout = AnchorLayout(size_hint=(1, None), height=dp(42), anchor_x='center', anchor_y='center', padding=(dp(0), dp(0), dp(0), dp(20)))
            summary = Label(halign='left', valign='center', text='[color=150470][size='+str(int(dp(18)))+'][font=assets/Inter-Bold.ttf]Summary', markup=True)
            summary.bind(size=summary.setter('text_size'))
            summary_layout.add_widget(summary)

            vertical_grid_layout.add_widget(name_layout)
            vertical_grid_layout.add_widget(details_layout)
            vertical_grid_layout.add_widget(summary_layout)
            vertical_grid_layout.add_widget(SummaryLabel())

            vertical_scroll_view.add_widget(vertical_grid_layout)
            background.add_widget(vertical_scroll_view)

            return background

    def create(self):
        float_layout = FloatLayout()

        top_layout = AnchorLayout(anchor_x='center', anchor_y='top')
        top_layout.add_widget(self.Top().create())

        bottom_layout = AnchorLayout(anchor_x='center', anchor_y='bottom')
        bottom_layout.add_widget(self.Bottom().create())

        float_layout.add_widget(top_layout)
        float_layout.add_widget(bottom_layout)

        return float_layout
