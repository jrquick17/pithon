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
    estimate = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def get_estimate(self):
        return self.estimate

    def update(self):
        pass


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


class ScoreBoard(Widget):
    estimate = NumericProperty(0)
    hits = NumericProperty(0)
    misses = NumericProperty(0)

    def add_to_result(self, is_hit):
        if is_hit:
            self.hits += 1
        else:
            self.misses += 1

        self.estimate = (self.hits / (self.hits + self.misses)) * 4


class PiDarts(Game):
    score_board = ObjectProperty(ScoreBoard())

    def update(self, dt):
        dart = Dart()
        self.add_widget(dart)

        is_hit = dart.throw()

        self.score_board.add_to_result(is_hit)

        super().update()


class PiSeries(Game):
    score_board = ObjectProperty(ScoreBoard())

    i = 1
    plus = True
    estimate = NumericProperty(0)

    def update(self, dt):
        self.estimate += 4/self.i * (1, -1)[self.plus]

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

