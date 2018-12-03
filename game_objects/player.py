import time
from os.path import join

import cv2 as cv
import numpy as np
# from pyglet.clock import schedule_interval

from game_objects.powerup import Powerup
from game_objects.projectile import Projectile
from game_objects.bar import Bar
# from interfaces.game_over_interface import GameOverInterface
from system import system
from widgets.stack_layout import Orientation
from pyglet import clock

import interfaces.game_over_interface


class Player(Projectile):
    damage_modifier: float = 1.0
    health: int = 100
    max_health: int = 100
    health_bar: Bar
    energy_bar: Bar
    projectile: Projectile = None

    def __init__(self, health=100, *args, **kwargs):
        self.max_health = self.health = health
        super().__init__(*args, **kwargs)
        self.health_bar = Bar(
            value=self.health,
            maximum=self.health,
            x=self.get_window().width / 2,
            y=100,
            width=self.get_window().width * 0.8,
            height=50
        )
        self.energy_bar = Bar(
            value=95,
            maximum=100,
            x=100,
            y=self.get_window().height / 2,
            width=50,
            height=self.get_window().height * 0.8,
            orientation=Orientation.VERTICAL
        )
        clock.schedule_interval(self.increment_energy_bar, 1 / 60)

    def increment_energy_bar(self, dt):
        if self.energy_bar.value >= self.energy_bar.max and system.get_enemy():
            self.energy_bar.set(0)
            self.attack()
        else:
            self.energy_bar += dt * 15

    def check_for_collision(self, projectile: Projectile):
        if not self.check_for_rectangle_collision(projectile):
            return False
        elif projectile == self.projectile:
            return False
        else:
            # Just let the powerup collide if the rectangles collide. Less to worry about
            if isinstance(projectile, Powerup):
                return True
            px1, py1, px2, py2 = projectile.get_coordinates()
            x1, y1, x2, y2 = self.get_coordinates()
            if x1 < px1:
                # The Player is on the left of the projectile
                if x2 < px2:
                    # The projectile overlaps and overflows
                    width = px2 - x1
                    left_vertical, right_vertical = x1, px2
                else:  # x2 >= px2
                    # width = self.get_right_bound() - px1
                    width = self.width
                    left_vertical, right_vertical = x1, x2
            else:  # x1 >= px2
                # The player is on the right of the projectile
                if x2 < px2:
                    width = x2 - px1
                    left_vertical, right_vertical = x1, px2
                else:  # x2 >= px2
                    width = x2 - px1
                    left_vertical, right_vertical = px1, x2
            if y1 < py1:
                if y2 < py2:
                    height = py2 - y1
                    top_horizontal, bottom_horizontal = projectile.get_top_bound(), y1
                else:
                    height = self.height
                    top_horizontal, bottom_horizontal = self.get_top_bound(), py1
            else:
                if y2 < py2:
                    height = projectile.height
                    top_horizontal, bottom_horizontal = projectile.get_top_bound(), y1
                else:
                    height = y2 - py1
                    top_horizontal, bottom_horizontal = self.get_top_bound(), py1
            width, height = int(round(width)), int(round(height))
            empty = np.zeros((height, width))
            # print(f'shape: {empty.shape}')
            img1 = empty.copy()
            img2 = empty.copy()
            x1, y1, x2, y2 = projectile.get_bounds(left_vertical, top_horizontal)
            img1[y1:y2, x1:x2] = projectile.threshold

            x1, y1, x2, y2 = self.get_bounds(left_vertical, top_horizontal)
            # print(f'Left vertical: {left_vertical} Top horizontal: {top_horizontal}')
            # print('self.get_bounds()', x1, y1, x2, y2)
            img2[y1:y2, x1:x2] = self.gray
            overlap = cv.bitwise_and(img1, img2)
            start = time.time()
            for y, row in enumerate(overlap):
                for x, cell in enumerate(row):
                    if cell >= 1:
                        # print(time.time() - start)
                        return True
            # print(time.time() - start)
            return False

    def draw(self):
        super().draw()
        if self.projectile:
            self.projectile.forward()
            self.projectile.draw()
            if system.get_enemy().check_for_rectangle_collision(self.projectile):
                # if self.projectile.check_for_rectangle_collision(system.get_enemy()):
                print('Enemy took damage')
                system.get_enemy().take_damage(self.projectile.damage)
                self.projectile.delete()
        self.health_bar.draw()
        self.energy_bar.draw()

    def take_damage(self, damage: float) -> float:
        actual_damage = damage * self.damage_modifier
        self.health -= actual_damage
        self.update_health_bar()
        if self.health <= 0:
            system.get_window().current_interface.enemy.attack_pattern.stop()
            system.get_window().load_interface(interfaces.game_over_interface.GameOverInterface())
        return actual_damage

    def update_health_bar(self):
        self.health_bar.set(self.health)

    def attack(self):
        print(system.get_enemy())
        if system.get_enemy():
            self.projectile = Projectile(src=join('images', 'laser-04.png'), x=self.x, y=self.y, damage=10, speed=5,
                                         acceleration=50)
            self.projectile.point(system.get_enemy().x, system.get_enemy().y)
