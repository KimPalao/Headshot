from abc import ABC, abstractmethod
from math import radians, cos, sin, pi, acos
from os.path import join
from random import randint
from time import time
from typing import List

from pyglet.graphics import Batch
from pyglet.window import Window

from audio import projectile_generate_one, sword_slice, sword_sharpen
from game_objects.projectile import Projectile
from system import system


class AttackPattern(ABC):
    projectile_per_attack: int = 1
    base_damage: int = 1
    base_speed: int = 1
    base_acceleration: int = 1
    self_acceleration = 0
    init_time = float
    projectiles: List[Projectile] = []
    batch: Batch = None
    running: bool = True

    def __init__(self, batch: Batch):
        self.batch = batch
        self.init_time = time()

    @abstractmethod
    def generate(self):
        pass

    def draw(self):
        for projectile in self.projectiles:
            if projectile.active:
                projectile.forward()
                projectile.draw()
                if system.get_player().check_for_collision(projectile):
                    print(system.get_player().take_damage(projectile.damage))
                    projectile.delete()

    def stop(self):
        self.running = False
        for projectile in self.projectiles:
            projectile.delete()
        del self


class BasicAttack(AttackPattern):
    projectile_per_attack = 1
    base_damage = 10
    base_speed = 5
    base_acceleration = 5
    projectiles: List[Projectile] = []

    def generate(self):
        window: Window = system.get_window()
        for i in range(self.projectile_per_attack):
            # Generate a projectile anywhere on the right side of the window
            x = randint(window.width // 2, window.width)
            y = randint(window.height // 2, window.height)
            projectile = Projectile(src=join('images', 'bonus-11.png'), x=x, y=y, damage=self.base_damage,
                                    speed=self.base_speed, acceleration=self.base_acceleration, batch=self.batch)
            player = system.get_player()
            projectile_generate_one.play()
            if player:
                projectile.point(player.x, player.y)
                self.projectiles.append(projectile)


class PinwheelAttack(AttackPattern):
    projectile_per_attack = 4
    base_damage = 5
    base_speed = 1
    base_acceleration = 2
    projectiles: List[Projectile] = []

    def generate(self):
        window: Window = system.get_window()
        player = system.get_player()
        max_range = min(window.width // 2, window.height // 2)
        diameter = randint(300, max_range)
        degrees = randint(0, 359)
        for i in range(self.projectile_per_attack):
            theta = radians(degrees) + ((2 * pi) / self.projectile_per_attack) * i
            x = player.x + cos(theta) * diameter
            y = player.y + sin(theta) * diameter
            projectile = Projectile(src=join('images', 'staryu.png'), x=x, y=y,
                                    damage=self.base_damage,
                                    speed=self.base_speed, acceleration=self.base_acceleration, batch=self.batch, )
            projectile.point(player.x, player.y)
            self.set_movement(projectile, diameter)

            self.projectiles.append(projectile)
        sword_sharpen.play()

    @staticmethod
    def set_movement(projectile: Projectile, diameter: int):
        player = system.get_player()
        center_x = (projectile.x + player.x) / 2
        center_y = (projectile.y + player.y) / 2

        @projectile.movement
        def movement():
            # pass
            if projectile.active:
                radius = diameter / 2
                cos_x = round((projectile.x - center_x) / radius, 4)
                sin_y = round((projectile.y - center_y) / radius, 4)
                try:
                    alpha = acos(cos_x)
                except ValueError:
                    projectile.delete()
                    return
                if sin_y < 0:
                    alpha = 2 * pi - alpha
                speed = projectile.calculate_speed()
                new_alpha = alpha + radians(speed)
                new_x = center_x + cos(new_alpha) * radius
                new_y = center_y + sin(new_alpha) * radius
                projectile.move(x=new_x, y=new_y)
                projectile.counter += speed
                projectile.rotation -= speed
                if projectile.counter >= 185:
                    projectile.delete()


class RainAttack(AttackPattern):
    projectile_per_attack = 5
    base_damage = 10
    base_speed = 5
    base_acceleration = 5
    projectiles = []

    def generate(self):
        if not self.running:
            return
        window = system.get_window()
        interface = window.current_interface
        projectiles = randint(0, self.projectile_per_attack)
        for i in range(projectiles):
            # Generate projectiles right above the player
            x = randint(int(interface.border.x), int(interface.border.x + interface.border.width))
            y = window.height - 100
            projectile = Projectile(src=join('images', 'meteor_sequence.png'), x=x, y=y, damage=self.base_damage,
                                    speed=self.base_speed, acceleration=self.base_acceleration, batch=self.batch,
                                    animated=True, animation_rows=1, animation_columns=4, animation_item_width=202,
                                    animation_item_height=103, animation_main_frame=0, animation_period=.25)
            # Rotate it so it points right below
            projectile.rotate(3 * pi / 2)
            self.projectiles.append(projectile)
