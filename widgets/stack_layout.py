from enum import Enum
from typing import List


class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Alignment(Enum):
    CENTER = 0

    LEFT = 1
    RIGHT = 2

    BOTTOM = 3
    TOP = 4


class LinearLayout:  # Implementation of Android's linear layout
    widgets: List = []
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    orientation: Orientation
    alignment_x: Alignment
    alignment_y: Alignment

    def __init__(self, x=0, y=0, orientation: Orientation = Orientation.VERTICAL, alignment_x=Alignment.LEFT,
                 alignment_y=Alignment.BOTTOM, *args):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.alignment_x = alignment_x
        self.alignment_y = alignment_y
        for widget in args:
            self.widgets.append(widget)
            if orientation == Orientation.VERTICAL:
                self.height += widget.height  # Let the stack layout grow as the stack increases
                self.width = max(self.width, widget.width)
            elif orientation == Orientation.HORIZONTAL:
                self.width += widget.width  # Let the stack layout expand as the stack increases
                self.height = max(self.height, widget.height)
            else:
                raise ValueError('Invalid Orientation')

    def render(self):
        current_x = self.x
        current_y = self.y
        for widget in self.widgets:
            if self.orientation == Orientation.VERTICAL:
                if self.alignment_x == Alignment.LEFT:  # Allow it to be 
                    widget.x = self.x
                elif self.alignment_x == Alignment.RIGHT:
                    widget.x = self.x + self.width - widget.width
                else:
                    widget.x = self.x + self.width / 2 - widget.width / 2
                current_y -= widget.height
                widget.y = current_y
            else:
                if self.alignment_y == Alignment.BOTTOM:
                    widget.y = self.y
                elif self.alignment_y == Alignment.TOP:
                    widget.y = self.y + self.height - widget.height
                else:
                    widget.y = self.y + self.height / 2 - widget.height / 2
                widget.x = current_x
                current_x += widget.width

    def draw(self):
        for widget in self.widgets:
            widget.draw()

    def __getitem__(self, item):
        return self.widgets[item]

    def __setitem__(self, key, value):
        self.widgets[key] = value

    def append(self, value):
        self.widgets.append(value)

    def insert(self, index, value):
        self.widgets.insert(index, value)
