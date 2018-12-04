import os
from os.path import join

import random

import cv2 as cv

from typing import List

from pyglet import options, gl, clock
from pyglet.graphics import Batch
from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.window import FPSDisplay, key

from pygarrayimage.arrayimage import ArrayInterfaceImage

from game_objects.attack_pattern import AttackPattern
from game_objects.enemy import AlienEnemy, AlienDog, Enemy, enemies
from game_objects.powerup import Powerup, HealPowerup, powerups
from interfaces.win_interface import WinInterface
from system import system, config
from widgets.facecam import Facecam
from interfaces.interface import Interface
from game_objects.player import Player
from game_objects.projectile import Projectile
from shapes.rectangle import Rectangle

options['debug_gl'] = False
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)


class GameInterface(Interface):
    attack: AttackPattern = None
    aii: ArrayInterfaceImage = None
    background_sprite: Sprite = None
    batch: Batch = None
    border: Rectangle = None
    enemy: Enemy = None
    image = None
    facecam: Facecam = None
    face_cascade = None
    foreground_sprite: Sprite = None
    fps_display: FPSDisplay = None
    keys = key.KeyStateHandler()
    player: Player = None
    projectiles: List[Projectile] = []
    powerup: Powerup = None
    scheduled_functions = tuple()

    def __init__(self):
        super().__init__()
        window = system.get_window()
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        base_path = os.path.join('images', 'space_background_pack', 'layers')

        self.background = load(os.path.join(base_path, 'parallax-space-background.png'))
        self.background_sprite = Sprite(self.background)
        big_planet = load(os.path.join(base_path, 'parallax-space-big-planet.png'))
        self.big_planet_sprite = Sprite(big_planet)
        far_planet = load(os.path.join(base_path, 'parallax-space-far-planets.png'))
        self.far_planet_sprite = Sprite(far_planet)
        ring_planet = load(os.path.join(base_path, 'parallax-space-ring-planet.png'))
        self.ring_planet_sprite = Sprite(ring_planet)
        self.ring_planet_sprite.x = 100
        self.ring_planet_sprite.y = 100
        stars = load(os.path.join(base_path, 'parallax-space-stars.png'))
        self.stars_sprite = Sprite(stars)
        self.scheduled_functions = (
            (self.randomize_projectiles, 2),
            (self.check_direction, 1 / 120),
            (self.generate_powerup, 20)
        )

        if config.get_config('control') == 1:
            self.face_cascade = cv.CascadeClassifier(
                'venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
            self.facecam = Facecam(face_cascade=self.face_cascade).start()
            self.aii = ArrayInterfaceImage(self.facecam.read(), 'BGR')
            self.image = self.aii.texture

            @self.facecam.event('on_face_move')
            def follow_face(x, y, width, height):
                # Need to flip things first to work
                x = self.image.width - x
                y = self.image.height - y
                new_x = self.border.x + x - width // 2
                new_y = self.border.y + y - height // 2
                self.player.move(new_x, new_y)

            self.scheduled_functions = (
                (self.randomize_projectiles, 2),
                (self.generate_powerup, 20),
            )

            window.push_handlers(self.facecam)

        self.player = Player(src='images/ufo.png', background=(255, 255, 255, 255))
        self.border = Rectangle(
            width=(500 if not self.image else self.image.width) + 10,
            height=(500 if not self.image else self.image.height) + 10,
            color=(0, 0, 0, 127)
        )
        self.player.scale = 1.2
        self.batch = Batch()
        self.projectiles: List[Projectile] = []
        window.push_handlers(self.keys)

        def pause_game(symbol, modifiers):
            if symbol == key.ESCAPE:
                self.enemy.running = not self.enemy.running
                self.enemy.attack_pattern.running = not self.enemy.attack_pattern.running
                self.player.running = not self.player.running

        window.on_key_press = pause_game

        for func, interval in self.scheduled_functions:
            clock.schedule_interval(func, interval)
        self.fps_display = FPSDisplay(window)
        # self.enemy = AlienEnemy(self.batch, speed=100)
        self.generate_enemy(0)

        self.resize()
        # self.attack = PinwheelAttack(self.player, batch=self.batch)
        # self.attack = RainAttack(self.player, batch=self.batch)

    def generate_enemy(self, dt):
        enemy_index = config.get_config('enemy')
        if enemy_index > len(enemies) - 1:
            return system.get_window().load_interface(WinInterface())

        window = system.get_window()
        self.enemy = enemies[enemy_index](self.batch, speed=100)
        self.enemy.move(window.width * 0.8, window.height / 2)
        self.enemy.next_x, self.enemy.next_y = self.enemy.x, self.enemy.y

        def on_die():
            config.set_config('enemy', config.get_config('enemy') + 1)
            clock.schedule_once(self.generate_enemy, 2)

        self.enemy.on_die = on_die

    def resize(self):
        window = system.get_window()
        scale = window.width / self.background.width
        self.background_sprite.scale = scale
        self.big_planet_sprite.scale = scale / 2
        self.far_planet_sprite.scale = scale / 2
        self.ring_planet_sprite.scale = scale / 2
        self.stars_sprite.scale = scale

        self.big_planet_sprite.x = window.width / 2
        self.big_planet_sprite.y = window.height / 2
        self.far_planet_sprite.x = window.width - self.far_planet_sprite.width
        self.far_planet_sprite.y = window.height - self.far_planet_sprite.height

        if self.image:
            self.image.x = (window.width - self.image.width) / 2
            self.image.y = (window.height - self.image.height) / 2
        # self.border.x = (window.width - self.border.width) / 2
        self.border.x = window.width / 2 * 0.3
        self.border.y = (window.height - self.border.height) / 2

        self.generate_powerup(0)
        self.player.move(x=window.width / 2 * 0.3, y=window.height / 2)

    def on_draw(self):
        self.animate_background()
        self.background_sprite.draw()
        self.big_planet_sprite.draw()
        self.far_planet_sprite.draw()
        self.ring_planet_sprite.draw()
        self.stars_sprite.draw()
        self.border.draw()
        if self.facecam:
            img = self.facecam.read()
            img = cv.flip(img, -1)
            self.image.blit(self.border.x, self.border.y, 0)
            self.aii.view_new_array(img)
        # self.fps_display.draw()
        self.player.draw()
        self.batch.draw()
        # self.attack.draw()
        if self.enemy:
            self.enemy.draw()
        if self.powerup:
            self.powerup.forward()
            self.powerup.draw()
            if self.player.check_for_collision(self.powerup):
                self.powerup.on_collide(self.player)
                self.powerup.delete()
                self.powerup = None

    def animate_background(self):
        big_planet_sprite_depth = 3
        far_planet_sprite_depth = 10
        ring_planet_sprite_depth = 5
        stars_sprite_depth = 8

        window = system.get_window()
        self.big_planet_sprite.x = self.big_planet_sprite.x - 1 * (1 / big_planet_sprite_depth)
        if self.big_planet_sprite.x + self.big_planet_sprite.width <= 0:
            self.big_planet_sprite.x = window.width
        self.far_planet_sprite.x = self.far_planet_sprite.x - 1 * (1 / far_planet_sprite_depth)
        if self.far_planet_sprite.x + self.far_planet_sprite.width <= 0:
            self.far_planet_sprite.x = window.width
        self.ring_planet_sprite.x = self.ring_planet_sprite.x - 1 * (1 / ring_planet_sprite_depth)
        if self.ring_planet_sprite.x + self.ring_planet_sprite.width <= 0:
            self.ring_planet_sprite.x = window.width
        self.stars_sprite.x = self.stars_sprite.x - 1 * (1 / stars_sprite_depth)
        if self.stars_sprite.x + self.stars_sprite.width <= 0:
            self.stars_sprite.x = window.width

    def generate_powerup(self, dt):
        window = system.get_window()
        roll = random.randint(1, 10)
        if roll <= 3:  # 30% chance of getting a powerup
            powerup = random.choice(powerups)(batch=self.batch)
            x = random.randint(self.border.x, self.border.x + self.border.width)
            powerup.move(x=x, y=window.height)

            @powerup.movement
            def movement():
                powerup.move(powerup.x, powerup.y - powerup.calculate_speed())

            self.powerup = powerup

    def randomize_projectiles(self, dt):
        if self.enemy:
            self.enemy.attack_pattern.generate()

    def check_direction(self, dt):
        unit = 500 * dt
        if self.keys[key.DOWN]:
            if self.player.get_bot_bound() - unit >= self.border.y:
                self.player.move(self.player.x, self.player.y - unit)
        elif self.keys[key.UP]:
            if self.player.get_bot_bound() + self.player.height + unit <= self.border.y + self.border.height:
                self.player.move(self.player.x, self.player.y + unit)
                # self.player.y += unit
        if self.keys[key.LEFT]:
            if self.player.get_left_bound() - unit >= self.border.x:
                self.player.move(self.player.x - unit, self.player.y)
        elif self.keys[key.RIGHT]:
            if self.player.get_left_bound() + self.player.width + unit <= self.border.x + self.border.width:
                self.player.move(self.player.x + unit, self.player.y)
        # if self.keys[key.ESCAPE]:
        # fg_ratio = 0.4
        # bg_ratio = 0.1
        # self.foreground_sprite.x = (window.width * (1 + fg_ratio)) / 2 - self.player.x * fg_ratio
        # self.foreground_sprite.y = (window.height * (1 + fg_ratio)) / 2 - self.player.y * fg_ratio
        # self.background_sprite.x = (window.width * (1 + bg_ratio)) / 2 - self.player.x * bg_ratio
        # self.background_sprite.y = (window.height * (1 + bg_ratio)) / 2 - self.player.y * bg_ratio

    def clean(self):
        self.enemy.clean()
        if self.facecam:
            self.facecam.clean()
        print(f'Deleting {self}')
        super().clean()
