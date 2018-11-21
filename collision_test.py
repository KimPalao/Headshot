from math import pi

from widgets.projectile import Projectile
from widgets.event_window import EventWindow
import pyglet
import cv2 as cv
import numpy as np
import time

window = EventWindow(fullscreen=True)
soul_image = pyglet.image.load('soul.png')
soul = pyglet.sprite.Sprite(soul_image, x=window.width / 2, y=window.height / 2)
print('Soul: ', soul.x, soul.y, soul.width, soul.height)

soul.scale = 0.1

print('Soul: ', soul.x, soul.y, soul.width, soul.height)

soul_np = cv.imread('soul.png')
projectile = Projectile(image_src='projectiles/dull_knife.png', speed=20)
# projectile.x = window.width / 4
projectile.y = window.height/2
# projectile.point(soul.x, soul.y)
print(soul_np)
cv.imwrite('big.png', soul_np*255)
dsize = (soul.width//10, soul.height//10)
soul_np = cv.resize(soul_np, dsize=dsize, interpolation=cv.INTER_CUBIC)
cv.imwrite('rotate.png', projectile.np)
print(soul_np)
cv.imwrite('small.png', soul_np*255)


@window.event
def on_draw():
    window.clear()
    projectile.draw()
    soul.draw()


def move_forward(dt):
    projectile.forward()
    if soul.x <= projectile.x+projectile.width <= soul.x + soul.width or soul.y <= projectile.y + projectile.height <= soul.height:
        pyglet.clock.unschedule(move_forward)


start = time.time()
img1 = cv.imread('test_images/dull_knife.png')
# img2 = cv.imread('test_images/heart_overlapping_2.png')
# projectile_arr = np.frombuffer(projectile.image.get_image_data().get_data('BGR', 3), np.uint8)
img2 = projectile.np
# result = img1 | img2
# print(result.all())  # False means there is a collision

# print(f'Time: {time.time() - start}')
# cv.imwrite('a.png', img1 * 255)
# cv.imwrite('b.png', img2 * 255)
# cv.imwrite('d.png', result * 255)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(move_forward, 1/120)
    pyglet.app.run()