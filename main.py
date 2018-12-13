from decimal import *
getcontext().prec = 51
from kivy.app import App
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import BooleanProperty, NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.time_picker import MDTimePicker
from kivymd.slider import *
from kivymd.theming import ThemeManager
import math
import random


class Game(Widget):
    PI = ObjectProperty(
        Decimal('3.14159265358979323846264338327950288419716939937510')
    )

    estimate = ObjectProperty(Decimal(0))
    iterations = NumericProperty(0)
    speed = NumericProperty(50)
    # speed_slider = ObjectProperty(None)

    schedule = False

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)

        self.set_speed(False, 100)

        # self.speed_slider.bind(value=self.set_speed)
        # self.speed_slider.value = 50

    def get_estimate(self):
        pass

    def get_iterations(self):
        pass

    def set_speed(self, slider, value):
        if value == 0:
            self.speed = 0
        else:
            self.speed = abs(1 * ((99 - value) / 100))

        if self.schedule:
            self.schedule.cancel()

            self.schedule = False

        if self.speed != 0:
            self.schedule = Clock.schedule_interval(self.update, self.speed)

    def check_accuracy(self):
        # TODO
        pass

    def update(self, dt):
        self.estimate = self.get_estimate()
        self.iterations = self.get_iterations()

        self.check_accuracy()

    def get_accuracy(self):
        return # correct digits and # number of iterations per


class Dart(RelativeLayout):
    parent_width = NumericProperty(1)

    x = NumericProperty(0)
    y = NumericProperty(0)

    r = NumericProperty(0)
    g = NumericProperty(0)

    def is_hit(self):
        return self.g == 1

    def throw(self):
        is_hit = None

        self.parent_width = self.parent.ids.dartboard.canvas.get_group('target')[0].size[0]
        height = self.parent.ids.dartboard.canvas.get_group('target')[0].size[1]

        if height > self.parent_width:
            self.parent_width = height

        if self.parent_width != 1:
            self.x = random.randint(0, self.parent_width)
            self.y = random.randint(0, self.parent_width)

            radius = self.parent_width / 2

            is_hit = math.pow(self.x - radius, 2) + math.pow(self.y - radius, 2) < math.pow(radius, 2)
            if is_hit:
                self.g = 1
            else:
                self.r = 1

            self.y += self.parent.ids.dartboard.canvas.get_group('target')[0].pos[1]
            self.x += self.parent.ids.dartboard.canvas.get_group('target')[0].pos[0]

            animation = Animation(size=(2, 2))
            animation.start(self)

        return is_hit


class PiDarts(Game):
    hits = NumericProperty(0)
    misses = NumericProperty(0)

    def __init__(self, **kwargs):
        super(PiDarts, self).__init__(**kwargs)

    def add_to_result(self, is_hit):
        if is_hit:
            self.hits = self.hits + 1
        else:
            self.misses = self.misses + 1

    def get_iterations(self):
        return self.iterations

    def get_estimate(self):
        return Decimal(
            Decimal(self.hits) / Decimal(self.hits + self.misses) * Decimal(4)
        ).quantize(
            Decimal('1.00000000000000000000000000000000000000000000000000')
        )

    def update(self, dt):
        dart = Dart()

        self.add_widget(dart)

        is_hit = dart.throw()

        if is_hit is not None:
            self.add_to_result(is_hit)

        self.iterations += 1

        super().update(dt)


class PiSeries(Game):
    i = 1
    equation = StringProperty('pi = 4 * 1 / (')
    estimate = ObjectProperty(Decimal(1))
    plus = True

    def __init__(self, **kwargs):
        super(PiSeries, self).__init__(**kwargs)

    def get_estimate(self):
        return self.estimate

    def get_iterations(self):
        return self.iterations

    def update(self, dt):
        self.i += 2
        self.plus = self.plus == False

        self.estimate = self.estimate + Decimal(1) / Decimal(self.i * (-1, 1)[self.plus])

        self.iterations += 1

        self.equation = self.equation + (' + ', ' - ')[self.plus] + '1/' + str(self.i)

        super().update(dt)


class PiApp(App):
    theme_cls = ThemeManager()
    title = "PiThon"

    def build(self):
        main_widget = Builder.load_file('pi.kv')

        # self.theme_cls.theme_style = 'Dark'
        self.bottom_navigation_remove_mobile(main_widget)

        return main_widget

    def bottom_navigation_remove_mobile(self, widget):
        # Removes some items from bottom-navigation demo when on mobile
        if DEVICE_TYPE == 'mobile':
            widget.ids.bottom_navigation_demo.remove_widget(widget.ids.bottom_navigation_desktop_2)
        if DEVICE_TYPE == 'mobile' or DEVICE_TYPE == 'tablet':
            widget.ids.bottom_navigation_demo.remove_widget(widget.ids.bottom_navigation_desktop_1)

if __name__ == '__main__':
    PiApp().run()

