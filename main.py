from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty, NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window

import math
import random


class Dart(RelativeLayout):
    x = NumericProperty(0)
    y = NumericProperty(0)

    r = NumericProperty(0)
    g = NumericProperty(0)

    def is_hit(self):
        return self.g == 1

    def throw(self):
        self.x = random.randint(0, 500)
        self.y = random.randint(0, 500)

        is_hit = math.pow(self.x - 250, 2) + math.pow(self.y - 250, 2) < math.pow(250, 2)
        if is_hit:
            self.g = 1
        else:
            self.r = 1


class Board(Widget):
    target = ObjectProperty(None)

    width = NumericProperty(500)
    height = NumericProperty(500)


class Target(Widget):
    radius = NumericProperty(500)


class PiDarts(Widget):
    board = ObjectProperty(None)

    estimate = NumericProperty(0)
    hits = NumericProperty(0)
    misses = NumericProperty(0)

    def update(self, dt):
        ball = Dart()
        ball.throw()

        if ball.is_hit():
            self.hits += 1
        else:
            self.misses += 1

        self.estimate = (self.hits / (self.hits + self.misses)) * 4

        self.add_widget(ball)


class PiApp(App):
    def build(self):
        if True:
            game = PiDarts()

        Clock.schedule_interval(game.update, 30.0 / 60.0)

        return game


if __name__ == '__main__':
    PiApp().run()
