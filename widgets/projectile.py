from .event_widget import EventWidget
from pyglet.sprite import Sprite
from pyglet.image import load
from math import degrees, sin, cos, sqrt, acos, pi, asin
import cv2 as cv
from scipy.ndimage import rotate
from numpy import ndarray


class Projectile(EventWidget, Sprite):
    def __init__(self, *args, **kwargs):
        """
        """
        print(args, kwargs)
        self.image_src = kwargs.pop('image_src')
        img = load(self.image_src)
        self.np = cv.imread(self.image_src)
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
        self.rotation += -degrees(self.radians)
        self.np = rotate(self.np, degrees(self.radians))

    def point(self, x: int, y: int) -> None:
        distance = sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        cos_x = x / distance
        sin_y = y / distance
        if -pi*2 <= sin_y <= pi*2:
            radians = abs(asin(sin_y))
        elif 0 <= cos_x <= pi:
            radians = abs(acos(cos_x))
        else:
            raise ValueError
        if x <= self.x and y >= self.y:  # Q2
            radians = pi - radians
        elif x <= self.x and y <= self.y:
            radians += pi
        elif x >= self.x and y <= self.y:
            radians = 2 * pi - radians
        self.rotate(radians)

    def forward(self):
        x = cos(self.radians) * self.speed
        y = sin(self.radians) * self.speed
        self.x += x
        self.y += y
        window = self.get_window()
        if self.x > window.width or self.y > window.height:
            self.delete()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        print(self.x, self.y, self.width, self.height)
        self._scale = value
        self._update_position()
        print(self.x, self.y, self.width, self.height)


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
