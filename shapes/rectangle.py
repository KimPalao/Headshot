from pyglet.graphics import draw
from pyglet.gl import GL_QUADS, GL_LINE_LOOP

from shapes.shape import Shape


class Rectangle(Shape):
    sides = 4
    gl_shape = GL_QUADS

    def __init__(self, x=0, y=0, width=None, height=None, color=(255, 255, 255, 255), outline=False):
        super().__init__(x=x, y=y, width=width, height=height, color=color, outline=outline)

    def refresh_polygon(self):
        self.polygon = ('v2f', (self.x,  # left
                                self.y,  # bottom
                                self.x + self.width,  # right
                                self.y,  # bottom
                                self.x + self.width,  # right
                                self.y + self.height,  # top
                                self.x,  # left
                                self.y + self.height))  # top

    def __repr__(self):
        return f'A rectangle at ({self.width}, {self.y}) width dimensions {self.width} width {self.height}'
