import json
import traceback
import time

import cv2 as cv

from random import randint

from typing import List

from pyglet.graphics import Batch
from pyglet.window import get_platform
from pyglet import options, gl, clock, app
from pygarrayimage.arrayimage import ArrayInterfaceImage
from pyglet.window import FPSDisplay
from widgets.event_window import EventWindow
from widgets.facecam import Facecam
from widgets.player import Player
from widgets.projectile import Projectile

options['debug_gl'] = False
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

with open('config.json') as config_file:
    config = json.loads(config_file.read())

# Window Settings
platform = get_platform()
display = platform.get_default_display()
screen = display.get_default_screen()
window = EventWindow(width=screen.width, height=screen.height)
window.maximize()

face_cascade = cv.CascadeClassifier('venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

facecam = Facecam(face_cascade).start()
img = facecam.read()
aii = ArrayInterfaceImage(img, 'BGR')
image = aii.texture
image.x = (window.width - image.width) / 2
image.y = (window.height - image.height) / 2
fps_display = FPSDisplay(window)

soul = Player(image_src='chihiro.png', x=window.width / 2, y=window.height / 2)
soul.scale = 1.2

batch = Batch()
projectiles: List[Projectile] = []


@window.event
def on_draw():
    window.clear()
    image.blit(
        image.x,
        image.y,
        0)
    aii.view_new_array(facecam.read())
    fps_display.draw()
    soul.draw()
    batch.draw()
    for projectile in projectiles:
        if projectile.active:
            projectile.forward()
            if soul.check_for_collision(projectile):
                projectile.delete()
                print(soul.take_damage(projectile.damage))


@facecam.event('on_face_move')
def follow_face(x, y, width, height):
    print('Face moving')
    new_x = image.x + x + width // 2
    new_y = image.y + y + height // 2
    print(new_x, new_y)
    soul.move(new_x, new_y)


window.push_handlers(facecam)


def randomize_projectiles(dt):
    x = randint(0, window.width)
    y = randint(0, window.height)
    projectile = Projectile(image_src='images/candy_cane.png', x=x, y=y, damage=10.0, batch=batch, speed=5,
                            bg=(255, 255, 255))
    projectile.scale = 2
    projectile.point(soul.x, soul.y)
    projectiles.append(projectile)


if __name__ == '__main__':
    count = 0
    timer = time.time()
    clock.schedule_interval(randomize_projectiles, 2)
    try:
        while 1:
            clock.tick()
            if window.has_exit:
                window.close()
                break
            for window in app.windows:
                window.switch_to()
                window.dispatch_events()
                window.dispatch_event('on_draw')
                window.flip()
                count += 1
            time.sleep(1 / 120)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        input()
