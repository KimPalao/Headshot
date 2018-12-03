from pyglet.text import Label
# from pyglet import clock

from fonts.fonts import press_start_2p
from interfaces.interface import Interface
from menus.main_menu import MainMenu
from menus.menu import Menu
from system import system


class MainInterface(Interface):
    title_label: Label = None
    main_menu: Menu = None

    def __init__(self):
        window = system.get_window()
        self.title_label = Label('Headshot', font_name=press_start_2p, font_size=36)
        self.title_label.anchor_x = 'center'
        self.title_label.anchor_y = 'center'
        self.main_menu = MainMenu()
        self.resize()
        window.on_key_press = self.main_menu.on_key_press
        self.main_menu.focused = True

    def on_draw(self):
        self.title_label.draw()
        self.main_menu.draw()

    def resize(self):
        window = system.get_window()
        self.main_menu.move(window.width / 2, 100)
        self.title_label.x = window.width / 2
        self.title_label.y = window.height / 2
