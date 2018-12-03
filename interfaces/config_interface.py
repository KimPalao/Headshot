from pyglet.text import Label

from interfaces.interface import Interface
from menus.config_menu import ConfigMenu
from menus.menu import Menu
from system import system
from widgets.event_widget import EventWidget
from widgets.textbox import TextBox


class ConfigInterface(Interface):
    name_label: Label = None
    name_textbox: TextBox = None
    config_menu: ConfigMenu = None

    def __init__(self):
        # print('Menu items:', Menu.items)
        self.config_menu = ConfigMenu(x=self.get_window().width / 4,
                                      y=self.get_window().height / 2)
        self.config_menu.focused = True
        window = system.get_window()
        for widget in self.config_menu.config_stack:
            if isinstance(widget, EventWidget):
                window.push_handlers(widget)
        window.on_key_press = self.config_menu.on_key_press

    def on_draw(self):
        self.config_menu.draw()

    def resize(self):
        self.config_menu.move(x=self.get_window().width / 4,
                              y=self.get_window().height / 2)
