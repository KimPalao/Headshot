from pyglet.clock import schedule_interval

from shapes.rectangle import Rectangle
from widgets.stack_layout import Orientation


class Bar:
    max: int

    def __init__(
            self,
            value: int,
            maximum: int,
            width: int,
            height: int,
            x: int,
            y: int,
            orientation: Orientation = Orientation.HORIZONTAL,
            value_color: tuple = (1, 68, 33, 255),  # UP Maroon
            max_color: tuple = (123, 17, 19, 255)  # UP Forest Green
    ) -> None:
        self.value = value
        self.max = maximum
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.orientation = orientation
        self.max_rectangle = Rectangle(
            x=(self.x - self.width / 2),
            y=(self.y - self.height / 2),
            width=self.width,
            height=self.height,
            color=max_color  # UP Maroon
            # color=(255, 0, 18, 255)
        )
        self.rectangle = Rectangle(
            x=(self.x - self.width / 2),
            y=(self.y - self.height / 2),
            width=self.width,
            height=self.height,
            color=value_color  # UP Forest Green
            # color=(0, 179, 44, 255)
        )
        schedule_interval(self.update_bar, 1 / 30)

    def update_bar(self, dt):
        if self.orientation == Orientation.HORIZONTAL:
            if self.value == 0:
                self.rectangle.width = 0
            else:
                self.rectangle.width = self.width * (self.value / self.max)
        elif self.orientation == Orientation.VERTICAL:
            if self.value == 0:
                self.rectangle.height = 0
            else:
                self.rectangle.height = self.height * (self.value / self.max)
        # difference = self.rectangle.width - (self.width * (self.value / self.max))
        # while self.rectangle.width >= self.width * (self.value / self.max):
        #     for i in range(100):
        # self.rectangle.width -= self.max_rectangle.width / 10000

    def set(self, value):
        self.value = value
        # self.health_rectangle.width = self.width * (self.health / self.max_health)
        # schedule_once(self.update_health_bar, 0)
        # schedule_interval(self.update_health_bar, 1/60)
        # TODO: Somehow make this run asynchronously.

        # difference = self.health_rectangle.width - (self.width * (self.health / self.max_health))
        # while self.health_rectangle.width >= self.width * (self.health / self.max_health):
        # for i in range(100):
        #     self.health_rectangle.width -= difference / 100
        #     sleep(1/1000)

    def draw(self):
        self.max_rectangle.draw()
        self.rectangle.draw()

    def __iadd__(self, other: int):
        self.set(min(self.value + other, self.max))
        return self

    def __isub__(self, other: int):
        self.set(self.value - other)
        return self

    def move(self, x, y):
        self.rectangle.x = x
        self.max_rectangle.x = x
        self.rectangle.y = y
        self.max_rectangle.y = y
