from os.path import join

from pyglet import media
from pyglet.text import Label

import menus
import audio
from fonts.fonts import press_start_2p
from interfaces.interface import Interface
from system import system


class WinInterface(Interface):
    win_label: Label = None
    game_over_menu: menus.menu.Menu = None
    drawn = False

    def __init__(self):
        self.game_over_label = Label('YOU WIN', font_name=press_start_2p, font_size=48)
        self.game_over_label.anchor_x = 'center'
        self.game_over_label.anchor_y = 'center'
        self.game_over_menu = menus.game_over_menu.GameOverMenu()
        self.game_over_menu.items.pop(0)
        self.game_over_menu.labels.pop(0)
        self.resize()
        window = system.get_window()
        window.on_key_press = self.game_over_menu.on_key_press
        self.game_over_menu.focused = True
        # media.load(
        #     join(
        #         'sound_FX',
        #         'freesound.org',
        #         'win.wav'
        #     ),
        #     streaming=False
        # ).play()
        # win.play()

    def on_draw(self):
        self.game_over_label.draw()
        self.game_over_menu.draw()

    def resize(self):
        window = system.get_window()
        self.game_over_menu.move(window.width / 2, 100)
        self.game_over_label.x = window.width / 2
        self.game_over_label.y = window.height / 2
