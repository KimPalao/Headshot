from pyglet.clock import schedule_interval

from shapes.rectangle import Rectangle


class HealthBar:
    max_health: int

    def __init__(self, health, width, height, x, y):
        self.max_health = health
        self.health = self.max_health
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.max_health_rectangle = Rectangle(
            x=(self.x - self.width / 2),
            y=(self.y - self.height / 2),
            width=self.width,
            height=self.height,
            color=(255, 0, 18, 255)
        )
        self.health_rectangle = Rectangle(
            x=(self.x - self.width / 2),
            y=(self.y - self.height / 2),
            width=self.width,
            height=self.height,
            color=(0, 179, 44, 255)
        )
        schedule_interval(self.update_health_bar, 1/30)

    def update_health_bar(self, dt):
        difference = self.health_rectangle.width - (self.width * (self.health / self.max_health))
        while self.health_rectangle.width >= self.width * (self.health / self.max_health):
        # for i in range(100):
            self.health_rectangle.width -= self.max_health_rectangle.width / 10000

    def set(self, health):
        self.health = health
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
        self.max_health_rectangle.draw()
        self.health_rectangle.draw()
