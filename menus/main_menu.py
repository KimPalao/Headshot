from typing import List

from pyglet.text import Label

from fonts.fonts import press_start_2p
from game_objects.enemy import enemies
from interfaces.config_interface import ConfigInterface
from interfaces.game_interface import GameInterface
from interfaces.instructions_interface import InstructionsInterface
from interfaces.level_select_interface import LevelSelectInterface
from menus.menu import Menu
from menus.menu_item import MenuItem
from system import config


class MainMenu(Menu):
    items: List[MenuItem] = []
    labels: List[Label] = []

    def __init__(self, x=0, y=0):
        def play_game():
            self.get_window().load_interface(GameInterface())

        def new_game():
            config.set_config('enemy', 0)
            play_game()

        def select_level():
            self.get_window().load_interface(LevelSelectInterface())

        def options():
            self.get_window().load_interface(ConfigInterface())

        def how_to_play():
            self.get_window().load_interface(InstructionsInterface())

        menu_items = [
            MenuItem('New Game', new_game),
            MenuItem('Options', options),
            MenuItem('How To Play', how_to_play),
        ]

        if config.get_config('enemy') >= len(enemies):
            menu_items.insert(0, MenuItem('Select Level', select_level))
        elif config.get_config('enemy') > 0:
            menu_items.insert(0, MenuItem('Continue', play_game))

        super().__init__(menu_items=menu_items, font_name=press_start_2p, font_size=24, x=x, y=y)
