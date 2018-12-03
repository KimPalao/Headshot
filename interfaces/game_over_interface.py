from pyglet.text import Label

from fonts.fonts import press_start_2p
from interfaces.interface import Interface
from system import system

import menus.menu
import menus.game_over_menu


class GameOverInterface(Interface):
    game_over_label: Label = None
    game_over_menu: menus.menu.Menu = None

    def __init__(self):
        self.game_over_label = Label('GAME OVER', font_name=press_start_2p, font_size=48)
        self.game_over_label.anchor_x = 'center'
        self.game_over_label.anchor_y = 'center'
        self.game_over_menu = menus.game_over_menu.GameOverMenu()
        self.resize()
        window = system.get_window()
        window.on_key_press = self.game_over_menu.on_key_press
        self.game_over_menu.focused = True

    def on_draw(self):
        self.game_over_label.draw()
        self.game_over_menu.draw()

    def resize(self):
        window = system.get_window()
        self.game_over_menu.move(window.width / 2, 100)
        self.game_over_label.x = window.width / 2
        self.game_over_label.y = window.height / 2
