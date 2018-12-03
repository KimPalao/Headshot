from typing import Callable

import pyglet
from pyglet.text.caret import Caret
from pyglet.text.document import FormattedDocument
from pyglet.text.layout import IncrementalTextLayout

from .focusable_widget import Focusable
from .hoverable_widget import Hoverable
from shapes.rectangle import Rectangle


class TextBox(Focusable, Caret, Hoverable):
    underline: Rectangle = None
    _on_enter: Callable = None
    ignore_enter: bool = False

    def __init__(self, width, height=0, multiline=False, dpi=None,
                 batch=None, group=None, wrap_lines=True, x=0, y=0, underlined=True, caret_color=(0, 0, 0)):
        self.document = FormattedDocument()
        self.layout = IncrementalTextLayout(self.document, width, height, multiline, dpi,
                                            batch, group, wrap_lines)
        if not height:
            # If the dev didn't specify a height, make the height equal to the height of the font
            font = pyglet.font.load(self.document.get_style('font'), self.document.get_style('font_size'))
            self.height = font.ascent - font.descent
        self._hover_cursor = self.get_window().CURSOR_TEXT
        super().__init__(self.layout, color=caret_color)
        # TODO: Allow the dev to specify how x and y are treated
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        if underlined:
            self.underline = Rectangle(
                x=self.x,
                y=self.y,
                width=self.width,
                height=1,
            )

    def reset_style(self):
        self.document.set_style(0, len(self.document.text), {'color': (255, 255, 255, 255)})

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
        if self.focused:
            self.on_activate()
        else:
            self.on_deactivate()
        self.layout.draw()
        if self.underline:
            self.underline.draw()

    def on_text(self, text):
        # Only type inside when the user is focused on the textbox
        if not self.focused:
            return
        if ord(text) == 13:
            if self.ignore_enter:  # Enter
                self.ignore_enter = False
            else:
                return self.on_enter()

        res = super().on_text(text)
        self.reset_style()
        return res

    def _on_enter_base(self) -> None:
        """
        The event handler that will be called by default if none are defined
        """
        pass

    @property
    def value(self):
        return self.document.text

    @value.setter
    def value(self, val):
        self.document.text = val

    @property
    def on_enter(self):
        if self._on_enter:
            return self._on_enter
        return self._on_enter_base

    @on_enter.setter
    def on_enter(self, func):
        def new_on_enter():
            if self.focused:
                func()

        self._on_enter = new_on_enter
