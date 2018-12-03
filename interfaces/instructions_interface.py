from fonts.fonts import press_start_2p

from interfaces.interface import Interface

from os.path import join
from os import getcwd

from pyglet.text import Label
from pyglet import image

from game_objects.projectile import Projectile

from widgets.stack_layout import LinearLayout


class InstructionsInterface(Interface):
    title_label: Label = None
    main_container: LinearLayout = LinearLayout()

    def __init__(self):
        self.title_label = Label('HOW TO PLAY', font_name=press_start_2p, font_size=48)
        self.title_label.anchor_x = 'center'
        self.title_label.anchor_y = 'center'

        projectiles = [
            ('Candy Cane', image.load(join(getcwd(), 'images', 'candy_cane.png')))
        ]
        powerups = [
            ('Cookie (Heal)', image.load(join(getcwd(), 'images', 'cookie.png')))
        ]

    def on_draw(self):
        self.title_label.draw()
        self.main_container.draw()

    def on_bind(self):
        self.resize()

    def resize(self):
        self.title_label.x = self.window.width / 2
        self.title_label.y = self.window.height - self.title_label.content_height / 2
        self.main_container.width = self.window.width
        self.main_container.height = self.window.height - self.title_label.height
