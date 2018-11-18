from typing import Callable

import pyglet
from pyglet.event import EventDispatcher
from pyglet.text.caret import Caret
from pyglet.text.document import FormattedDocument
from pyglet.text.layout import IncrementalTextLayout

from .focusable_widget import Focusable
from .hoverable_widget import Hoverable
from .rectangle import Rectangle


class TextBox(Focusable, Caret, Hoverable):
    underline: Rectangle = None

    def __init__(self, width, height=0, multiline=False, dpi=None,
                 batch=None, group=None, wrap_lines=True, x=0, y=0, underlined=True):
        self.document = FormattedDocument()
        self.layout = IncrementalTextLayout(self.document, width, height, multiline, dpi,
                                                             batch, group, wrap_lines)
        if not height:
            # If the dev didn't specify a height, make the height equal to the height of the font
            font = pyglet.font.load(self.document.get_style('font'), self.document.get_style('font_size'))
            self.height = font.ascent - font.descent
        self._hover_cursor = self.get_window().CURSOR_TEXT
        super().__init__(self.layout)
        # TODO: Allow the dev to specify how x and y are treated
        self.x = x - self.width//2
        self.y = y - self.height//2
        print(self.height)
        if underlined:
            self.underline = Rectangle(
                x=self.x,
                y=self.y,
                width=self.width,
                height=1,
            )
            print(self.underline)

    @property
    def x(self):
        return self.layout.x
    
    @x.setter
    def x(self, value):
        if self.underline:
            self.underline.x = value
        self.layout.x = value

    @property
    def y(self):
        return self.layout.y

    @y.setter
    def y(self, value):
        print(value)
        if self.underline:
            self.underline.y = value
        self.layout.y = value

    @property
    def width(self):
        return self.layout.width

    @width.setter
    def width(self, value):
        if self.underline:
            self.underline.width = value
        self.layout.width = value

    @property
    def height(self):
        return self.layout.height

    @height.setter
    def height(self, value):
        print(value)
        self.layout.height = value

    def draw(self):
        self.layout.draw()
        if self.underline:
            self.underline.draw()

    def on_text(self, text):
        # Only type inside when the user is focused on the textbox
        if not self.focused:
            return
        return super().on_text(text)
