from typing import Callable

import pyglet
from pyglet.graphics import Batch, Group
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
    style: dict = {}

    def __init__(self, width: int, height: int = 0, multiline: bool = False, dpi: object = None,
                 batch: Batch = None, group: Group = None, wrap_lines: bool = True, x: int = 0, y: int = 0,
                 underlined: bool = True, caret_color: tuple = (0, 0, 0),
                 numbers_only: bool = False, font_name=None, font_size=None, font_color=(255, 255, 255, 2555), max_chars=0) -> None:
        self.document = FormattedDocument()
        self.layout = IncrementalTextLayout(self.document, width, height, multiline, dpi,
                                            batch, group, wrap_lines)
        self.numbers_only = numbers_only
        self.style['color'] = font_color
        self.max_chars = max_chars
        if font_name:
            self.style['font_name'] = font_name
        if font_size:
            self.style['font_size'] = font_size
        self.reset_style()
        if not height:
            # If the dev didn't specify a height, make the height equal to the height of the font
            font = pyglet.font.load(
                font_name or self.document.get_style('font'),
                font_size or self.document.get_style('font_size')
            )
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
        self.document.set_style(0, len(self.document.text), self.style)

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

    def on_text(self, text: str):
        # Only type inside when the user is focused on the textbox
        # print(text)
        if not self.focused:
            return
        if ord(text) == 13:
            if self.ignore_enter:  # Enter
                self.ignore_enter = False
                return
            else:
                return self.on_enter()
        # if self.max_chars and len(self.value) >= self.max_chars:
        #         return
        # if self.numbers_only and not text.isnumeric():
        #     return
        res = super().on_text(text)
        print('res', res, 'text', text)
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
        self.reset_style()

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
