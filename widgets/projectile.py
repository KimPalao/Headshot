from .event_widget import EventWidget
from pyglet.sprite import Sprite
from pyglet.image import load
from math import degrees, sin, cos, sqrt, acos, pi, asin


class Projectile(EventWidget, Sprite):
    def __init__(self, *args, **kwargs):
        """
        """
        print(args, kwargs)
        img = load(kwargs.pop('image_src'))
        # self.sprite = Sprite(img, x=kwargs.get('x', 0), y=kwargs.get('y', 0))
        # self._x = self.sprite.x
        # self._y = self.sprite.y
        # self.rotation = kwargs.get('rotation', 0)
        self.speed = kwargs.pop('speed', 1)
        super().__init__(img, *args, **kwargs)
        self.radians = 0
        self.image.anchor_x = self.image.width / 2
        self.image.anchor_y = self.image.height / 2

    def rotate(self, radians):
        self.radians = radians
        self.rotation += -degrees(radians)

    def point(self, x, y):
        distance = sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        cos_x = x / distance
        radians = abs(acos(cos_x))
        if x <= self.x and y >= self.y:  # Q2
            radians = pi - radians
        elif x <= self.x and y <= self.y:
            radians += pi
        elif x >= self.x and y <= self.y:
            radians = 2*pi - radians

        # if y <= self.y:
        #     radians += pi
        #     if x >= self.x:
        #         radians += pi/2
        # elif x <= self.x:
        #     radians += pi/2
        #     if y >= self.y:
        #         radians += pi/2
        self.rotate(radians)

    def forward(self):
        x = cos(self.radians) * self.speed
        y = sin(self.radians) * self.speed
        self.x += x
        self.y += y

    # def draw(self):
    #     self.sprite.draw()
    #
    # @property
    # def x(self):
    #     return self._x
    #
    # @x.setter
    # def x(self, value):
    #     self._x = value
    #     self.sprite.x = value
    #
    # @property
    # def y(self):
    #     return self._y
    #
    # @y.setter
    # def y(self, value):
    #     self._y = value
    #     self.sprite.y = value
    #
    # @property
    # def width(self):
    #     return self._width
    #
    # @width.setter
    # def width(self, value):
    #     self._width = value
    #
    # @property
    # def height(self):
    #     return self._height
    #
    # @height.setter
    # def height(self, value):
    #     self._height = value
    #
    # @property
    # def rotation(self):
    #     return self._rotation
    #
    # @rotation.setter
    # def rotation(self, value):
    #     self._rotation = value
    #     self.sprite.rotation = value
