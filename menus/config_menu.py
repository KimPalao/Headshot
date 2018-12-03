from typing import List

from pyglet.text import Label

from fonts.fonts import press_start_2p
from menus.menu import Menu
from menus.menu_item import MenuItem
from system.config import config
from widgets.stack_layout import LinearLayout
from widgets.textbox import TextBox


class ConfigMenu(Menu):
    items: List[MenuItem] = []
    labels: List[Label] = []
    config_stack: LinearLayout = LinearLayout()

    def __init__(self, x=0, y=0):
        name_textbox = TextBox(100, caret_color=(255, 255, 255))
        name_textbox.value = config['name']

        @name_textbox.event('on_enter')
        def name_textbox_on_enter():
            config['name'] = name_textbox.value
            self.focused = True
            name_textbox.ignore_enter = True
            name_textbox.focused = False

        self.config_stack.append(name_textbox)

        @self.add_item('Enter Name')
        def enter_name():
            name_textbox.focused = True
            self.focused = False

        @self.add_item('Test')
        def test():
            print('This is a test')


        super().__init__(font_name=press_start_2p, font_size=24, x=x, y=y)
        self.config_stack.x = self.get_window().width - self.x
        self.config_stack.y = self.y
        self.config_stack.render()

    def draw(self):
        super().draw()
        self.config_stack.draw()
