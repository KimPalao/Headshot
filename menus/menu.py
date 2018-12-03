import time
from typing import List

from pyglet.text import Label
from pyglet.window import key
from pyglet import font

from menus.menu_item import MenuItem
from shapes.triangle import Triangle
from widgets.focusable_widget import Focusable


class Menu(Focusable):
    keys = key.KeyStateHandler()
    pointer: Triangle = None
    index: int = 0
    items: List[MenuItem] = []
    labels: List[Label] = []
    height: int = 0
    width: int = 0

    def __init__(self, menu_items, font_name, font_size=None, x=0, y=0):
        self.x = x
        self.y = y
        self.items = menu_items
        self.labels = [None] * len(self.items)
        for index, item in enumerate(self.items):
            label = Label(item.name, font_name=font_name, font_size=font_size)
            self.labels[index] = label
            # if label not in self.labels:
            #     self.labels.append(label)
        self.set_label_coordinates()
        self.pointer = Triangle(0, 0, 10, 10)
        self.update_pointer()

        # self.pointer.x = self.x - self.pointer.width
        # self.pointer.y = self.y + self.height - self.pointer.height

    def set_label_coordinates(self):
        self.height = 0
        for index, label in enumerate(self.labels):
            label.x = self.x - label.content_width / 2
            label.y = self.y + ((len(self.items) - index) * label.content_height)
            self.height += label.content_height
            self.width = max(self.width, label.content_width)
            # label.anchor_x = label.content_width / 2
            # label.anchor_y = label.content_height / 2

    def draw(self):
        for label in self.labels:
            label.draw()
        if self.focused:
            self.pointer.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.prev()
        elif symbol == key.DOWN:
            self.next()
        elif symbol == key.ENTER:
            self.call_current()
        else:
            return
        self.update_pointer()

    def update_pointer(self):
        current_label: Label = self.labels[self.index]
        # print(current_label, current_label.text)
        font_object = font.load(current_label.get_style('font'), current_label.get_style('font_size'))
        font_height = font_object.ascent - font_object.descent
        self.pointer.x = current_label.x - self.pointer.width
        self.pointer.y = current_label.y + font_height / 2

    def __iter__(self):
        return self.items

    def __next__(self):
        self.index = (self.index + 1) % len(self.items)
        return self.curr()

    def next(self):
        return self.__next__()

    def prev(self):
        self.index = (self.index - 1) % len(self.items)
        return self.curr()

    def curr(self):
        return self.items[self.index]

    def call_current(self):
        return self.items[self.index]()

    def add_item(self, name: str):
        def decorator(func):
            menu_item = MenuItem(name=name, func=func)
            if menu_item not in self:
                self.items.append(menu_item)

        return decorator

    def move(self, x, y):
        self.x, self.y = x, y
        self.set_label_coordinates()
        self.update_pointer()

    def __repr__(self):
        return f'{type(self)} with items: {self.items}'

    def __contains__(self, item: MenuItem) -> bool:
        for menu_item in self.items:
            if item.name == menu_item.name:
                return True
        return False
