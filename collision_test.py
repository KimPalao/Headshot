from game_objects.projectile import Projectile
from game_objects.player import Player
from pyglet import clock
from widgets.event_window import EventWindow
import pyglet
import cv2 as cv
import time

window = EventWindow(fullscreen=True)
# soul_image = pyglet.image.load('soul.png')
# soul = pyglet.sprite.Sprite(soul_image)
soul = Player(src='soul.png')
print(soul.width, soul.height)
print(window.width / 2, window.height / 2)
soul.move(window.width / 2 - soul.width, window.height / 2 - soul.height)
soul.scale = 1.3
print('Soul: ', soul.x, soul.y, soul.width, soul.height)
soul_np = cv.imread('soul.png')
projectile = Projectile(src='projectiles/dull_knife.png', speed=10, x=window.width * 0.7, y=window.height)
# projectile.x = window.width / 3
# projectile.rectangle.x = projectile.x
# projectile.y = window.height / 2
# projectile.rectangle.y = projectile.y
projectile.point(soul.x, soul.y)


@window.event
def on_draw():
    window.clear()
    projectile.draw()
    soul.draw()


def move_forward(dt):
    # projectile.forward()
    # projectile.rotate(pi/180)
    if soul.check_for_collision(projectile):
        print('hit!',
              projectile.get_left_bound(),
              projectile.get_right_bound(),
              soul.get_left_bound(),
              )
        clock.unschedule(move_forward)


start = time.time()
img1 = cv.imread('test_images/dull_knife.png')
img1 = projectile.np
# img2 = cv.imread('test_images/heart_not_overlapping_3.png')
img2 = cv.imread('test_images/heart_overlapping_2.png')
img1gray = cv.threshold(img1, 1, 255, cv.THRESH_BINARY)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(move_forward, 1 / 120)
    pyglet.app.run()
