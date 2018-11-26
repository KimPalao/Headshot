import time

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from pyglet.sprite import Sprite

from .rectangle import Rectangle
from .projectile import Projectile
from .health_bar import HealthBar
import system


class Player(Projectile):
    damage_modifier: float = 1.0
    health: int = 100
    max_health: int = 100
    health_bar: HealthBar

    def __init__(self, health=100, *args, **kwargs):
        self.max_health = self.health = health
        super().__init__(*args, **kwargs)
        self.health_bar = HealthBar(
            health=self.health,
            x=self.get_window().width / 2,
            y=100,
            width=self.get_window().width * 0.8,
            height=50
        )

    def check_for_rectangle_collision(self, projectile: Projectile):
        px1, py1, px2, py2 = projectile.get_coordinates()
        x1, y1, x2, y2 = self.get_coordinates()
        return (x1 <= px1 <= x2 and y1 <= py1 <= y2) or \
               (x1 <= px2 <= x2 and y1 <= py1 <= y2) or \
               (x1 <= px1 <= x2 and y1 <= py2 <= y2) or \
               (x1 <= px2 <= x2 and y1 <= py2 <= y2)

    def check_for_collision(self, projectile: Projectile):
        if not self.check_for_rectangle_collision(projectile):
            return False
        else:
            print(self.get_coordinates(), projectile.get_coordinates())
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
            print(f'Left vertical: {left_vertical} Top horizontal: {top_horizontal}')
            print('self.get_bounds()', x1, y1, x2, y2)
            img2[y1:y2, x1:x2] = self.gray
            overlap = cv.bitwise_and(img1, img2)
            start = time.time()
            for y, row in enumerate(overlap):
                for x, cell in enumerate(row):
                    if cell >= 1:
                        print(time.time() - start)
                        return True
            print(time.time() - start)
            return False

    def draw(self):
        super().draw()
        self.health_bar.draw()

    def take_damage(self, damage: float) -> float:
        actual_damage = damage * self.damage_modifier
        self.health -= actual_damage
        self.update_health_bar()
        return actual_damage

    def update_health_bar(self):
        self.health_bar.set(self.health)
