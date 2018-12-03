from os.path import join
from random import randint
from typing import Callable

from pyglet.text import Label
# from pyglet import clock

from game_objects.attack_pattern import AttackPattern
from game_objects.bar import Bar
from game_objects.attack_pattern import BasicAttack, PinwheelAttack, RainAttack
from game_objects.projectile import Projectile
from pyglet import clock

from system import system


class Enemy(Projectile):
    attack_pattern: AttackPattern = None
    name_tag: Label = None
    health: int = 100
    speed: int = 10
    on_die: Callable = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.health_bar = Bar(
            value=self.health,
            maximum=self.health,
            width=self.width,
            height=25,
            x=self.x,
            y=self.y - 25
        )
        self.name_tag = Label(type(self).__name__)
        self.name_tag.anchor_x = 'center'
        self.name_tag.anchor_y = 'center'
        self.scheduled_functions = (
            (self.change_position, 1),
            (self.move_around, 1 / 60)
        )
        self.next_x, self.next_y = self.x, self.y
        for func, interval in self.scheduled_functions:
            clock.schedule_interval(func, interval)

    def change_position(self, dt):
        if not self.running:
            return
        x = randint(-1, 1) * self.calculate_speed()
        y = randint(-1, 1) * self.calculate_speed()
        window = system.get_window()
        # If the enemy would move too far left or right, make it move the other way
        if self.x + x > window.width or self.x + x < window.width / 2:
            x = -x
        if self.y + y > window.height or self.y + y < window.height / 3:
            y = -y
        self.next_x = self.x + x
        self.next_y = self.y + y

    def move_around(self, dt):
        # Make it move incrementally instead of all at once for a smooth moving animation
        if not self.running:
            return
        print(f'dt: {dt}')
        next_x = self.x + ((self.next_x - self.x) * dt)
        next_y = self.y + ((self.next_y - self.y) * dt)
        print(next_x, next_y)
        self.move(next_x, next_y)
        # self.move(self.x + x, self.y + y)

    def draw(self):
        if not self.running:
            return
        super().draw()
        self.attack_pattern.draw()
        self.name_tag.draw()
        self.health_bar.draw()

    def move(self, x, y):
        if not self.running:
            return
        super().move(x, y)
        self.health_bar.move(self.x - self.width / 2, self.y - self.height / 2 - 25)
        self.name_tag.x = self.x - self.width / 2
        self.name_tag.y = self.y + self.height / 2
        print(self.health_bar, self.health_bar.x, self.health_bar.y)

    def clean(self):
        for func, interval in self.scheduled_functions:
            clock.unschedule(func)
        print('Unscheduling, hopefully')
        self.name_tag.delete()
        self.delete()
        self.attack_pattern.stop()

    def take_damage(self, damage: float) -> float:
        actual_damage = damage
        self.health -= actual_damage
        self.update_health_bar()
        if self.health <= 0:
            self.die()
        return actual_damage

    def update_health_bar(self):
        self.health_bar.set(self.health)

    def die(self):
        self.running = False
        print(f'Opacity: {self.opacity}')

        def fade(dt):
            self.opacity -= dt * 255
            if self.opacity <= 0:
                clock.unschedule(fade)

        print(f'Opacity: {self.opacity}')

        self.attack_pattern.stop()
        clock.schedule_interval(fade, 1 / 20)
        clock.schedule_once(lambda dt: self.clean(), 2)

        self.on_die()


class AlienShip(Enemy):
    health = 20

    def __init__(self, batch, *args, **kwargs):
        super().__init__(src=join('images', 'alien_ship.png'), *args, **kwargs)
        # self.attack_pattern = BasicAttack(batch=batch)
        # self.attack_pattern = RainAttack(batch=batch)
        self.attack_pattern = BasicAttack(batch=batch)


class AlienDog(Enemy):
    health = 40

    def __init__(self, batch, *args, **kwargs):
        super().__init__(src=join('images', 'alien_dog.png'), *args, **kwargs)
        # self.attack_pattern = BasicAttack(batch=batch)
        # self.attack_pattern = RainAttack(batch=batch)
        self.attack_pattern = PinwheelAttack(batch=batch)


class AlienBlob(Enemy):
    health = 60

    def __init__(self, batch, *args, **kwargs):
        super().__init__(src=join('images', 'alien_blob.png'), *args, **kwargs)
        # self.attack_pattern = BasicAttack(batch=batch)
        # self.attack_pattern = RainAttack(batch=batch)
        self.attack_pattern = RainAttack(batch=batch)


class AlienEnemy(Enemy):
    health = 100

    def __init__(self, batch, *args, **kwargs):
        super().__init__(src=join('images', 'alien.png'), *args, **kwargs)
        # self.attack_pattern = BasicAttack(batch=batch)
        # self.attack_pattern = RainAttack(batch=batch)
        self.attack_pattern = RainAttack(batch=batch)

    # def draw(self):
    #     super().draw()


enemies = [AlienShip, AlienDog, AlienBlob, AlienEnemy]
