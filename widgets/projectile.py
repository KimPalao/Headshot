import datetime
from typing import Tuple

from .event_widget import EventWidget
from .rectangle import Rectangle
from pyglet.sprite import Sprite
from pyglet.image import load
from math import degrees, sin, cos, sqrt, acos, pi, asin
import cv2 as cv
from scipy.ndimage import rotate
from numpy import ndarray
from matplotlib import pyplot


class Projectile(EventWidget, Sprite):
    threshold = None
    rectangle: Rectangle = None
    gray = None
    active: bool = True
    damage: int = 1

    def __init__(self, *args, **kwargs):
        """
        """
        self.image_src = kwargs.pop('image_src')
        self.background = kwargs.pop('bg', False)
        img = load(self.image_src)
        self.np = cv.imread(self.image_src)
        self.speed = kwargs.pop('speed', 1)
        self.damage = kwargs.pop('damage', self.damage)
        super().__init__(img, *args, **kwargs)
        self.radians = 0
        self.image.anchor_x = self.image.width / 2
        self.image.anchor_y = self.image.height / 2
        self.update(x=self.x, y=self.y)
        self.refresh_threshold()
        if self.background:
            self.rectangle = Rectangle(x=self.get_left_bound(), y=self.get_bot_bound(), width=self.width,
                                       height=self.height, color=self.background)

    def move(self, x, y):
        self.x = x
        self.y = y
        if self.rectangle:
            self.rectangle.x = x - self.width / 2
            self.rectangle.y = y - self.height / 2

    def draw(self):
        if self.rectangle:
            self.rectangle.draw()
        super().draw()

    def get_left_bound(self):
        return self.x - self.width / 2

    def get_right_bound(self):
        return self.x + self.width / 2

    def get_top_bound(self):
        return self.y + self.height / 2

    def get_bot_bound(self):
        return self.y - self.height / 2

    def get_coordinates(self) -> Tuple[int, int, int, int]:
        return self.get_left_bound(), self.get_bot_bound(), self.get_right_bound(), self.get_top_bound()

    def crop(self):
        left = top = 0
        height, width, _ = self.np.shape
        right, bot = min_right, min_bot = width - 1, height - 1

        while top < bot:
            for x in range(width):
                if any(self.np[top, x]):
                    min_right = x
                    min_bot = top
                    break
            else:
                top += 1
                continue
            break

        while left < min_right:
            for y in range(height - 1, top, -1):
                # if self.np[y, left] != [0, 0, 0]:
                if any(self.np[y, left]):
                    min_bot = y
                    break
            else:
                left += 1
                continue
            break

        while bot > min_bot:
            for x in range(width - 1, left - 1, -1):
                if any(self.np[bot, x]):
                    min_right = x
                    break
            else:
                bot -= 1
                continue
            break

        while right > min_right:
            for y in range(bot, top, -1):
                if any(self.np[y, right]):
                    # min_right = y
                    break
            else:
                right -= 1
                continue
            break

        self.np = self.np[top:bot, left:right]
        gray = cv.cvtColor(self.np, cv.COLOR_BGR2GRAY)
        retval, self.threshold = cv.threshold(gray, 1, 255, cv.THRESH_BINARY)

    def refresh_threshold(self):
        _, self.threshold = cv.threshold(self.np, 1, 255, cv.THRESH_BINARY)
        self.gray = cv.cvtColor(self.threshold, cv.COLOR_BGR2GRAY)

    def rotate(self, radians):
        self.radians = radians
        self.rotation += -degrees(self.radians)
        self.np = rotate(self.np, degrees(self.radians))
        self.refresh_threshold()
        self.crop()
        height, width, a = self.np.shape
        if self.rectangle:
            self.rectangle.width = width
            self.rectangle.height = height

    @property
    def width(self) -> int:
        return self.np.shape[1]

    @property
    def height(self) -> int:
        return self.np.shape[0]

    def point(self, x: int, y: int) -> None:
        distance = sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        if distance == 0:
            return
        cos_x = (x - self.x) / distance
        radians = abs(acos(cos_x))
        if x <= self.x and y <= self.y:  # Q3
            print('Q3')
            radians = 2 * pi - radians
        elif x >= self.x and y <= self.y:  # Q 4
            print('Q4')
            radians = 2 * pi - radians
        print(f'Radians: {radians}')
        self.rotate(radians)

    def forward(self):
        x = cos(self.radians) * self.speed
        y = sin(self.radians) * self.speed
        self.x += x
        self.y += y
        if self.rectangle:
            self.rectangle.x = self.get_left_bound()
            self.rectangle.y = self.get_bot_bound()
        # window = self.get_window()
        # if self.x > window.width or self.y > window.height:
        #     self.delete()

    def get_bounds(self, left_vertical, top_horizontal) -> Tuple[int, int, int, int]:
        x1: int = int(self.get_left_bound() - left_vertical)
        x2: int = int(x1 + self.width)
        y1: int = int(top_horizontal - (self.get_bot_bound() + self.height))
        y2: int = int(y1 + self.height)
        return x1, y1, x2, y2

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, value) -> None:
        self._scale = value
        self._update_position()

    def __repr__(self):
        return f'Projectile: x={self.x} y={self.y} width={self.width} height={self.height}'

    def __bool__(self):
        return self.active

    def delete(self):
        super().delete()
        self.active = False
