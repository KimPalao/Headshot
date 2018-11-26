from math import pi

from widgets.projectile import Projectile
from widgets.player import Player
from widgets.event_window import EventWindow
import pyglet
import cv2 as cv
import numpy as np
import time
from matplotlib import pyplot as plt
from config import config

window = EventWindow(fullscreen=True)
# soul_image = pyglet.image.load('soul.png')
# soul = pyglet.sprite.Sprite(soul_image)
soul = Player(image_src='soul.png')
print(soul.width, soul.height)
print(window.width / 2, window.height / 2)
soul.move(window.width / 2 - soul.width, window.height / 2 - soul.height)
soul.scale = 1.3
print('Soul: ', soul.x, soul.y, soul.width, soul.height)
soul_np = cv.imread('soul.png')
projectile = Projectile(image_src='projectiles/dull_knife.png', speed=10, x=window.width * 0.7, y=window.height)
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
        pyglet.clock.unschedule(move_forward)


start = time.time()
img1 = cv.imread('test_images/dull_knife.png')
img1 = projectile.np
# img2 = cv.imread('test_images/heart_not_overlapping_3.png')
img2 = cv.imread('test_images/heart_overlapping_2.png')
img1gray = cv.threshold(img1, 1, 255, cv.THRESH_BINARY)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(move_forward, 1 / 120)
    pyglet.app.run()
