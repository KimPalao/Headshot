import datetime
import time
from typing import Tuple, Callable, Union

from system import system
from widgets.event_widget import EventWidget
from shapes.rectangle import Rectangle
from pyglet.sprite import Sprite
from pyglet.image import load, ImageGrid, TextureGrid, Animation
from math import degrees, sin, cos, sqrt, acos, pi
import cv2 as cv
from scipy.ndimage import rotate


class Projectile(EventWidget, Sprite):
    _forward: Callable = None
    active: bool = True
    counter: int = 0
    damage: int = 1
    gray = None
    next_x: int
    next_y: int
    rectangle: Rectangle = None
    running: bool = True
    threshold = None

    def __init__(self, src: str, background: tuple = None, speed: Union[int, float] = 1, damage: Union[int, float] = 1,
                 acceleration: Union[int, float] = 0, animated: bool = False, animation_rows: int = None, animation_columns: int = None,
                 animation_item_width: int = None, animation_item_height: int = None, animation_period: float = 0.1,
                 animation_main_frame: int = 0, *args, **kwargs) -> None:
        """
        :param src:                     File of the image to load
        :param background:              A tuple representing RGBA values for the background
        :param speed:                   Speed at which the projectile will move
        :param damage:                  Damage the projectile will deal
        :param acceleration:            Acceleration in m/s^2
        :param animated:                Flag saying if the projectile uses an animation
        :param animation_rows:          The number of rows in the animation sequence source
        :param animation_columns:       The number of columns in the animation sequence source
        :param animation_item_width:    The width of each frame of the animation in the source
        :param animation_item_height:   The height of each frame in the source
        :param animation_period:        Time to show each frame
        :param animation_main_frame:    The frame in which the hitbox bounds will be calculated
        :param args:
        :param kwargs:
        """
        if animated:
            image = load(src)
            image_seq = ImageGrid(image, rows=animation_rows, columns=animation_columns,
                                  item_width=animation_item_width, item_height=animation_item_height)
            image_texture = TextureGrid(image_seq)
            img = Animation.from_image_sequence(image_texture[0:], period=animation_period, loop=True)
            # self.src =
            image_array = cv.imread(src)
            x1 = animation_item_width * animation_main_frame
            x2 = x1 + animation_item_width
            self.np = image_array[:, x1:x2]  # The numpy array used for the collision test will be the slice
        else:
            img = load(src)
            self.np = cv.imread(src)  # The whole image will be read
        self.src = img
        self.background = background
        self.speed = speed
        self.acceleration = acceleration
        self.damage = damage
        super().__init__(img, *args, **kwargs)
        self.radians = 0
        # self.anchor
        if animated:
            for frame in self.image.frames:
                frame.image.anchor_x = image.width / animation_columns / 2
                frame.image.anchor_y = image.height / animation_rows / 2
        else:
            self.image.anchor_x = self.image.width / 2
            self.image.anchor_y = self.image.height / 2
        self.init_time = time.time()
        self.update(x=self.x, y=self.y)
        self.refresh_threshold()
        if self.background:
            self.rectangle = Rectangle(x=self.get_left_bound(), y=self.get_bot_bound(), width=self.width,
                                       height=self.height, color=self.background)

    def move(self, x, y):
        if not self.running:
            return
        self.x = x
        self.y = y
        if self.rectangle:
            self.rectangle.x = x - self.width / 2
            self.rectangle.y = y - self.height / 2

    def draw(self):
        if self:
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
        # cv.imwrite(f'test_laser_{datetime.datetime.now():%H_%M_%S}.png', self.np)
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

    def check_for_rectangle_collision(self, p):
        px1, py1, px2, py2 = p.get_coordinates()
        x1, y1, x2, y2 = self.get_coordinates()
        return (x1 <= px1 <= x2 and y1 <= py1 <= y2) or \
               (x1 <= px2 <= x2 and y1 <= py1 <= y2) or \
               (x1 <= px1 <= x2 and y1 <= py2 <= y2) or \
               (x1 <= px2 <= x2 and y1 <= py2 <= y2)

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

    def calculate_speed(self):
        # Speed derived from the acceleration formula
        time_delta = time.time() - self.init_time
        return time_delta * self.acceleration + self.speed or self.speed

    def forward(self):
        if not self.running:
            return
        if self._forward:
            return self._forward()
        else:
            # This allows for boomerang movement, don't remove yet
            # multiplier = (time_delta * self.acceleration - self.speed or self.speed)

            multiplier = self.calculate_speed()
            x = cos(self.radians) * multiplier
            y = sin(self.radians) * multiplier
            self.move(self.x + x, self.y + y)
        self.counter += 1
        window = system.get_window()
        if not (0 < self.x < window.width and 0 < self.y < window.height):
            self.delete()
        # window = self.get_window()
        # if self.x > window.width or self.y > window.height:
        #     self.delete()

    def movement(self, func):
        self._forward = func
        return func

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
        if self:
            super().delete()
        self.active = False
