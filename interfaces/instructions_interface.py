from fonts.fonts import press_start_2p

from interfaces.interface import Interface

from os.path import join
from os import getcwd

from pyglet.text import Label
from pyglet import image

from game_objects.projectile import Projectile
from system import system

from widgets.stack_layout import LinearLayout


class InstructionsInterface(Interface):
    title_label: Label = None
    main_container: LinearLayout = LinearLayout()

    def __init__(self):
        self.title_label = Label('HOW TO PLAY', font_name=press_start_2p, font_size=48)
        # self.title_label.anchor_x = 'center'
        # self.title_label.anchor_y = 'center'

        self.step1_label = Label('Dodge Projectiles', font_name=press_start_2p, font_size=48)
        # self.step1_label.anchor_x = 'center'
        # self.step1_label.anchor_y = 'center'

        self.step2_label = Label('Charge Your Energy', font_name=press_start_2p, font_size=48)
        # self.step2_label.anchor_x = 'center'
        # self.step2_label.anchor_y = 'center'

        self.step3_label = Label('Defeat Enemies', font_name=press_start_2p, font_size=48)
        # self.step3_label.anchor_x = 'center'
        # self.step3_label.anchor_y = 'center'

        projectiles = [
            ('Homing Projectiles', image.load(join(getcwd(), 'images', 'candy_cane.png'))),
            ('Staryu', image.load(join(getcwd(), 'images', 'staryu.png'))),
            ('Meteor', image.load(join(getcwd(), 'images', 'meteor_1.png'))),
        ]
        powerups = [
            # ('Cookie (Heal)', image.load(join(getcwd(), 'images', 'cookie.png')))
        ]

        self.main_container.append(self.step1_label)
        self.main_container.append(self.step2_label)
        self.main_container.append(self.step3_label)

    def on_draw(self):
        self.title_label.draw()
        self.main_container.draw()

    def on_bind(self):
        self.resize()

    def resize(self):
        window = system.get_window()
        self.title_label.x = window.width / 2
        self.title_label.y = window.height - self.title_label.content_height / 2
        self.main_container.width = window.width
        self.main_container.height = window.height - self.title_label.height
        self.main_container.x = window.width / 2
        self.main_container.y = window.height - self.title_label.content_height
        self.main_container.render()
