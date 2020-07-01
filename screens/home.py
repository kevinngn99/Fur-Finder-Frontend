from kivy.lang.builder import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.metrics import sp, dp
import os
from jnius import cast
from jnius import autoclass

Builder.load_file(os.path.join(os.path.dirname(__file__), '../screens/home.kv'))


class HomeScreen(Screen):
    pass


class VerticalScrollView(ScrollView):
    def on_scroll_start(self, touch, check_children=True):
        return super(VerticalScrollView, self).on_scroll_start(touch)

    def on_scroll_move(self, touch):
        x, y = self.ids.vertical_grid_layout.to_widget(*self.to_window(*touch.pos))

        for i in range(6):
            if self.ids.vertical_grid_layout.children[i].collide_point(x, y):
                if abs(touch.dy) >= abs(touch.dx):
                    self.ids.vertical_grid_layout.children[i].disabled = True

        return super(VerticalScrollView, self).on_scroll_move(touch)

    def on_scroll_stop(self, touch, check_children=True):
        for i in range(6):
            self.ids.vertical_grid_layout.children[i].disabled = False

        return super(VerticalScrollView, self).on_scroll_stop(touch)


class HorizontalScrollView(ScrollView):
    def on_scroll_start(self, touch, check_children=True):
        return super(HorizontalScrollView, self).on_scroll_start(touch)

    def on_scroll_move(self, touch):
        if abs(touch.dx) > abs(touch.dy):
            self.parent.parent.disabled = True

        return super(HorizontalScrollView, self).on_scroll_move(touch)

    def on_scroll_stop(self, touch, check_children=True):
        self.parent.parent.disabled = False

        return super(HorizontalScrollView, self).on_scroll_stop(touch)


class Home:
    def create(self):
        home_screen = HomeScreen()

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
            print('Not an Android')


        '''
        vertical_home_screen = VerticalScrollView()
        home_screen.add_widget(vertical_home_screen)
        for i in range(5):
            vertical_home_screen.ids.vertical_grid_layout.add_widget(Label(text='[color=150470]Bruh', size_hint=(1, None), height=dp(50), markup=True))

        for i in range(6):
            horizontal_scroll_view = HorizontalScrollView()
            vertical_home_screen.ids.vertical_grid_layout.add_widget(horizontal_scroll_view)

            for j in range(25):
                horizontal_scroll_view.ids.horizontal_grid_layout.add_widget(Label(text='[color=150470]Bruh', size_hint=(None, None), size=(dp(50), dp(50)), markup=True))
        '''

        return home_screen
