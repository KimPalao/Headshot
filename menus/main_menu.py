from typing import List

from pyglet.text import Label

from fonts.fonts import press_start_2p
from interfaces.config_interface import ConfigInterface
from interfaces.game_interface import GameInterface
from interfaces.instructions_interface import InstructionsInterface
from menus.menu import Menu
from menus.menu_item import MenuItem


class MainMenu(Menu):
    items: List[MenuItem] = []
    labels: List[Label] = []

    def __init__(self, x=0, y=0):
        # @self.add_item('Play Game')
        def play_game():
            self.get_window().load_interface(GameInterface())

        # @self.add_item('Options')
        def options():
            self.get_window().load_interface(ConfigInterface())

        # @self.add_item('How To Play')
        def how_to_play():
            self.get_window().load_interface(InstructionsInterface())

        menu_items = [
            MenuItem('Play Game', play_game),
            MenuItem('Options', options),
            MenuItem('How To Play', how_to_play),
        ]
        # @self.add_item('four')
        # def four():
        #     print('Hello four!')
        #
        # @self.add_item('five')
        # def five():
        #     print('Hello five!')

        super().__init__(menu_items=menu_items, font_name=press_start_2p, font_size=24, x=x, y=y)
