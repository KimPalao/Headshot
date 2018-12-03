import pyglet
import time

from math import sqrt, sin, cos, acos, pi, radians

from pyglet.window import get_platform

from widgets.event_window import EventWindow
from game_objects.projectile import Projectile

platform = get_platform()
display = platform.get_default_display()
screen = display.get_default_screen()
window = pyglet.window.Window(width=screen.width, height=screen.height)
window.maximize()
projectile = Projectile(src='images/candy_cane.png')
projectile.move(window.width / 2, window.height / 2 + 100)
print(projectile.x, projectile.y)
center_x, center_y = window.width / 2, window.height / 2
radius = sqrt((projectile.x - center_x) ** 2 + (projectile.y - center_y) ** 2)
initial_x, initial_y = center_x + radius, center_y
start = time.time()
acceleration = 1


@window.event
def on_draw():
    window.clear()
    projectile.draw()


def move_clockwise(dt):
    x = (projectile.x - center_x) / radius
    y = (projectile.y - center_y) / radius
    print(f'x {x}')
    theta = acos(x)
    delta_time = time.time() - start
    velocity = acceleration * delta_time
    print('delta', delta_time)
    if y < 0:
        theta = 2 * pi - theta
    new_theta = theta + radians(1 * velocity)
    print(f'new_theta {new_theta}, cos {cos(new_theta)}, sin {sin(new_theta)}')
    projectile.move(center_x + cos(new_theta) * radius, center_y + sin(new_theta) * radius)


if __name__ == '__main__':
    pyglet.clock.schedule_interval(move_clockwise, 1 / 60)
    pyglet.app.run()
