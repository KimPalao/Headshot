import pyglet
from game_objects.projectile import Projectile
from game_objects.player import Player
from math import pi

window = pyglet.window.Window(fullscreen=True)
# soul_image = pyglet.image.load('soul.png')
# soul = pyglet.sprite.Sprite(soul_image, x=window.width / 2, y=window.height / 2)
# soul = Player
# soul.scale = 0.1
soul = Player(src='images/santa.gif')
print(soul.width, soul.height)
print(window.width / 2, window.height / 2)
soul.move(window.width / 2 - soul.width, window.height / 2 - soul.height)
soul.scale = 1.3
print('Soul: ', soul.x, soul.y, soul.width, soul.height)
# projectile = Projectile(src='projectiles/dull_knife.png', speed=10, x=window.width * 0.7, y=window.height)


projectile_one = Projectile(src='images/candy_cane.png', speed=10)
projectile_two = Projectile(src='images/candy_cane.png', x=window.width, y=window.height, speed=10)
projectile_three = Projectile(src='images/candy_cane.png', x=window.width, speed=10)
projectile_four = Projectile(src='images/candy_cane.png', y=window.height, speed=10)

# projectile_one.scale = .5
# projectile_two.scale = .5
# projectile_three.scale = .5
# projectile_four.scale = .5
# projectile.rotate(45)
projectiles = [projectile_one, projectile_two, projectile_three, projectile_four]
for projectile in projectiles:
    projectile.point(soul.x, soul.y)
    projectile.scale = 2
# print(x, y)


def rotate_projectile(dt):
    projectile_one.rotate(pi / 180)


def move(dt):
    for projectile in projectiles:
        if projectile:
            projectile.forward()
            if soul.check_for_collision(projectile):
                projectile.delete()


@window.event
def on_draw():
    window.clear()
    soul.draw()
    for projectile in projectiles:
        if projectile:
            projectile.draw()


if __name__ == '__main__':
    pyglet.clock.schedule_interval(move, .02)
    pyglet.app.run()
