import pyglet
from widgets.projectile import Projectile
from math import pi, sqrt, cos, sin, acos, asin

window = pyglet.window.Window(fullscreen=True)
soul_image = pyglet.image.load('soul.png')
soul = pyglet.sprite.Sprite(soul_image, x=window.width / 2, y=window.height / 2)
soul.scale = 0.1


projectile_one = Projectile(image_src='projectiles/minecraft_sword.png', speed=10)
projectile_two = Projectile(image_src='projectiles/minecraft_sword.png', x=window.width, y=window.height, speed=10)
projectile_three = Projectile(image_src='projectiles/minecraft_sword.png', x=window.width, speed=10)
projectile_four = Projectile(image_src='projectiles/minecraft_sword.png', y=window.height, speed=10)

projectile_one.scale = .5
projectile_two.scale = .5
projectile_three.scale = .5
projectile_four.scale = .5
# projectile.rotate(45)

distance1 = sqrt((soul.x - projectile_one.x) ** 2 + (soul.y - projectile_one.y) ** 2)
x1 = soul.x / distance1
y1 = soul.y / distance1
# print(acos(x), asin(y))
radians1 = acos(x1)


projectile_one.rotate(radians1)
projectile_two.point(soul.x, soul.y)
projectile_three.point(soul.x, soul.y)
projectile_four.point(soul.x, soul.y)

# print(x, y)


def rotate_projectile(dt):
    projectile_one.rotate(pi / 180)


def move(dt):
    projectile_one.forward()
    projectile_two.forward()
    projectile_three.forward()
    projectile_four.forward()


@window.event
def on_draw():
    window.clear()
    soul.draw()
    projectile_one.draw()
    projectile_two.draw()
    projectile_three.draw()
    projectile_four.draw()


if __name__ == '__main__':
    pyglet.clock.schedule_interval(move, .02)
    pyglet.app.run()
