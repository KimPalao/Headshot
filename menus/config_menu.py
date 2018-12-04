from typing import List

from pyglet.text import Label

from fonts.fonts import press_start_2p
from menus.menu import Menu
from menus.menu_item import MenuItem
from system import config
from widgets.stack_layout import LinearLayout
from widgets.textbox import TextBox


class ConfigMenu(Menu):
    items: List[MenuItem] = []
    labels: List[Label] = []
    config_stack: LinearLayout = LinearLayout()

    def __init__(self, x=0, y=0):
        health_textbox = TextBox(200, caret_color=(255, 255, 255), font_name=press_start_2p, font_size=24, max_chars=4)
        health_textbox.value = str(config.get_config('health'))

        @health_textbox.event('on_enter')
        def health_textbox_on_enter():
            # config['health'] = health_textbox.value
            config.set_config('health', int(health_textbox.value))
            self.focused = True
            health_textbox.ignore_enter = True
            health_textbox.focused = False

        damage_textbox = TextBox(200, caret_color=(255, 255, 255), font_name=press_start_2p, font_size=24, max_chars=3)
        damage_textbox.value = str(config.get_config('damage'))

        @damage_textbox.event('on_enter')
        def damage_textbox_on_enter():
            config.set_config('damage', int(damage_textbox.value))
            self.focused = True
            damage_textbox.ignore_enter = True
            damage_textbox.focused = False

        self.config_stack.append(health_textbox)
        self.config_stack.append(damage_textbox)

        # @self.add_item('Enter Name')
        def enter_health():
            health_textbox.focused = True
            self.focused = False
            self.move(self.x, self.y)

        # @self.add_item('Test')
        def enter_damage():
            damage_textbox.focused = True
            self.focused = False

        menu_items = [
            MenuItem('Health: ', enter_health),
            MenuItem('Damage: ', enter_damage)
        ]

        super().__init__(menu_items=menu_items, font_name=press_start_2p, font_size=24, x=x, y=y)
        self.move(self.x, self.y)

    def draw(self):
        super().draw()
        self.config_stack.draw()

    def move(self, x, y):
        super().move(x, y)
        self.config_stack.x = self.get_window().width - self.x
        self.config_stack.y = self.y + self.height
        self.config_stack.render()
