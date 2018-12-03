from abc import ABC, abstractmethod

from pyglet.gl import GL_LINE_LOOP
from pyglet.graphics import draw


class Shape(ABC):
    color: tuple = tuple()
    gl_shape: int = 0
    sides: int = 0
    polygon: tuple = tuple()

    def __init__(self, x: float = 0, y: float = 0, width=1, height=1, color=(255, 255, 255, 255), rotation: float = 0.0,
                 outline=False):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self.outline = outline
        self.rgba = color
        self.color = ('c4B', self.rgba * self.sides)

        self.refresh_polygon()

    @abstractmethod
    def refresh_polygon(self):
        pass

    def draw(self):
        gl = GL_LINE_LOOP if self.outline else self.gl_shape
        draw(self.sides, gl, self.polygon, self.color)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.refresh_polygon()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.refresh_polygon()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self.refresh_polygon()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self.refresh_polygon()
