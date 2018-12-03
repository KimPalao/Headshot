from math import cos, sin, pi, sqrt

from pyglet.graphics import draw
from pyglet.gl import GL_TRIANGLES

from shapes.shape import Shape


class Triangle(Shape):
    sides = 3
    gl_shape = GL_TRIANGLES

    def __init__(self, x=0, y=0, width=0, height=0, rotation=0):
        self.rotation = rotation
        super().__init__(x, y, width, height)

    def refresh_polygon(self):
        coordinates = []
        for i in range(self.sides):
            radians = self.rotation + ((2 * pi) / 3) * i
            radius = sqrt(self.width ** 2 + self.height ** 2) / 2
            x, y = self.x + cos(radians) * radius, self.y + sin(radians) * radius
            coordinates.append(x)
            coordinates.append(y)
        self.polygon = ('v2f', tuple(coordinates))


if __name__ == '__main__':
    import pyglet.app
    from pyglet.window import Window

    window = Window()
    triangle = Triangle(x=window.width / 2, y=window.height / 2, width=100, height=100, rotation=pi)

    @window.event
    def on_draw():
        window.clear()
        triangle.draw()

    pyglet.app.run()
