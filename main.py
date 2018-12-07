from decimal import *
getcontext().prec = 50
from kivy.app import App
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import BooleanProperty, NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.vector import Vector
import math
import random


class Game(Widget):
    PI = ObjectProperty(
        Decimal('3.14159265358979323846264338327950288419716939937510')
    )

    estimate = ObjectProperty(Decimal(0))
    iterations = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def get_estimate(self):
        pass

    def check_accuracy(self):
        # TODO
        pass

    def update(self):
        self.estimate = self.get_estimate()
        self.iterations += 1

        self.check_accuracy()

    def get_accuracy(self):
        return # correct digits and # number of iterations per


class Dart(RelativeLayout):
    x = NumericProperty(0)
    y = NumericProperty(0)

    r = NumericProperty(0)
    g = NumericProperty(0)

    def is_hit(self):
        return self.g == 1

    def throw(self):
        if self.parent.width > self.parent.height:
            width = self.parent.height
        else:
            width = self.parent.width

        self.x = random.randint(0, width)
        self.y = random.randint(0, width)

        radius = width / 2

        is_hit = math.pow(self.x - radius, 2) + math.pow(self.y - radius, 2) < math.pow(radius, 2)
        if is_hit:
            self.g = 1
        else:
            self.r = 1

        animation = Animation(size=(1, 1))
        animation.start(self)

        return is_hit


class PiDarts(Game):
    hits = NumericProperty(0)
    misses = NumericProperty(0)

    def add_to_result(self, is_hit):
        if is_hit:
            self.hits = self.hits + 1
        else:
            self.misses = self.misses + 1

    def get_estimate(self):
        return Decimal(self.hits) / Decimal(self.hits + self.misses) * Decimal(4)

    def update(self, dt):
        dart = Dart()

        self.add_widget(dart)

        is_hit = dart.throw()

        self.add_to_result(is_hit)

        super().update()


class PiSeries(Game):
    i = 1
    plus = True

    def get_estimate(self):
        return Decimal(-4) / Decimal(self.i * (1, -1)[self.plus])

    def update(self, dt):
        self.i += 2
        self.plus = self.plus == False

        super().update()


class PiApp(App):
    def build(self):
        if True:
            game = PiDarts()
        else:
            game = PiSeries()

        return game


if __name__ == '__main__':
    PiApp().run()

