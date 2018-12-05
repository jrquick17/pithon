from kivy.app import App
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty, NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window

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


class Target(Widget):
    radius = NumericProperty(500)


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

        animation = Animation(size=(1,1))
        animation.start(self)

        return is_hit


class DartBoard(Widget):
    width = NumericProperty(500)
    height = NumericProperty(500)

    target = ObjectProperty(Target)


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
    dart_board = ObjectProperty(DartBoard)
    score_board = ObjectProperty(ScoreBoard())

    def update(self, dt):
        dart = Dart()

        is_hit = dart.throw()

        self.score_board.add_to_result(is_hit)

        self.add_widget(dart)

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
        if False:
            game = PiDarts()
        else:
            game = PiSeries()

        return game


if __name__ == '__main__':
    PiApp().run()

