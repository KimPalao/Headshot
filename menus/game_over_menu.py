from typing import List

from pyglet.text import Label

from fonts.fonts import press_start_2p
from menus.menu import Menu
from menus.menu_item import MenuItem

import interfaces.game_interface
import interfaces.main_interface


class GameOverMenu(Menu):
    items: List[MenuItem] = []
    labels: List[Label] = []

    def __init__(self, x=0, y=0):
        def play_again():
            self.get_window().load_interface(interfaces.game_interface.GameInterface())

        def return_to_main_menu():
            self.get_window().load_interface(interfaces.main_interface.MainInterface())

        def exit_game():
            self.get_window().has_exit = True

        menu_items = [
            MenuItem('Play Again?', play_again),
            MenuItem('Return to Main Menu', return_to_main_menu),
            MenuItem('Exit', exit_game),
        ]

        super().__init__(menu_items, font_name=press_start_2p, font_size=24, x=x, y=y)
