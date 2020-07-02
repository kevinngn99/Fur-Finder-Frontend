from kivy.uix.image import AsyncImage, Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import stencil_instructions
from kivy.uix.label import Label
from kivy.metrics import dp


class Card:
    class CardView(Widget):
        def prepare(self):
            with self.canvas:
                Color(rgb=get_color_from_hex('#F2F3FB'))
                RoundedRectangle(pos=self.pos, size=(dp(250), dp(200)), radius=(dp(15), dp(15), dp(15), dp(15)))

    class Border(Widget):
        def prepare(self):
            with self.canvas:
                Color(rgb=get_color_from_hex('#150470'))
                RoundedRectangle(pos=self.pos, size=self.size, radius=(dp(55), dp(55), dp(55), dp(55)))

    class Circle(AsyncImage):
        def prepare(self):
            with self.canvas.before:
                stencil_instructions.StencilPush()
                RoundedRectangle(pos=(self.x + dp(5), self.y + dp(5)), size=(dp(100), dp(100)), size_hint=(None, None), radius=(dp(50), dp(50), dp(50), dp(50)))
                stencil_instructions.StencilUse()
            with self.canvas.after:
                stencil_instructions.StencilUnUse()
                stencil_instructions.StencilPop()

    def __init__(self, name='', gender='', image='', breed='', color='', date=''):
        self._name = name,
        self._gender = gender,
        self._image = image,
        self._breed = breed,
        self._color = color,
        self._date = date

    def circular_image(self, pos, size):
        card_x, card_y = pos
        card_width, card_height = size
        padding = dp(15)

        x = card_x + card_width - (dp(110) + padding)
        y = card_y + card_height - (dp(110) + padding)

        border = self.Border(pos=(x, y), size=(dp(110), dp(110)))
        border.prepare()

        circle = self.Circle(source=self._image[0], pos=border.pos)
        if circle.image_ratio < 1:
            circle.size_hint = (circle.image_ratio + 1, circle.image_ratio + 1)
        else:
            circle.size_hint = (circle.image_ratio, circle.image_ratio)
        circle.prepare()

        anchor_layout = AnchorLayout(pos=border.pos, anchor_x='center', anchor_y='center', size=border.size)
        anchor_layout.add_widget(circle)

        border.add_widget(anchor_layout)
        return border

    def details(self, pos, size):
        anchor_layout = AnchorLayout(pos=pos, size=size, anchor_x='center', anchor_y='center')
        pet = Label(padding=(dp(15), dp(15)), size_hint=(1, 1), halign='left', valign='top', markup=True,
                      text='[color=150470][size='+str(int(dp(20)))+'][font=assets/Inter-SemiBold.ttf]'+self._name[0]+'\n[size='+str(int(dp(18)))+'][font=assets/Inter-Medium.ttf]'+self._gender[0]+'\n[size='+str(int(dp(16)))+'][font=assets/Inter-Regular.ttf]'+self._date.split(':')[0])
        pet.bind(size=pet.setter('text_size'))
        time = Label(padding=(dp(15), dp(15)), halign='right', valign='bottom', markup=True,
                     text='[color=150470][size='+str(int(dp(18)))+'][font=assets/Feather.ttf][size='+str(int(dp(18)))+'][font=assets/Inter-Medium.ttf] 5 Hours Ago')
        time.bind(size=time.setter('text_size'))
        anchor_layout.add_widget(pet)
        anchor_layout.add_widget(time)

        return anchor_layout

    def build(self, pos=(0, 0)):
        card_view = self.CardView(pos=pos, size=(dp(250), dp(200)), size_hint=(None, None))
        card_view.prepare()
        card_view.add_widget(self.circular_image(card_view.pos, card_view.size))
        card_view.add_widget(self.details(card_view.pos, card_view.size))
        return card_view
