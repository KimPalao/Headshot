from pyglet.graphics import draw
from pyglet.gl import GL_QUADS


class Rectangle:
    def __init__(self, *args, **kwargs):
        self._x = kwargs.get('x', None)
        self._y = kwargs.get('y', None)
        self._width = kwargs.get('width', None)
        self._height = kwargs.get('height', None)
        self.rgb = kwargs.get('color', (0, 0, 0))
        self.color = ('c3B', self.rgb * 4)
        self.polygon = tuple()
        self.refresh_polygon()

    def draw(self):
        draw(4, GL_QUADS, self.polygon, self.color)

    def refresh_polygon(self):
        self.polygon = ('v2f', (self.x,  # left
                                self.y,  # bottom
                                self.x + self.width,  # right
                                self.y,  # bottom
                                self.x + self.width,  # right
                                self.y + self.height,  # top
                                self.x,  # left
                                self.y + self.height))  # top

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

    def __repr__(self):
        return f'A rectangle at ({self.width}, {self.y}) width dimensions {self.width} width {self.height}'
