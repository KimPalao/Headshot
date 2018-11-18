"""
Demo for the face tracking
"""

import time
from widgets.rectangle import Rectangle
import cv2
import pyglet
pyglet.options['debug_gl'] = False
from pyglet import gl
from pyglet.window import FPSDisplay
from webcam import Facecam
from pygarrayimage.arrayimage import ArrayInterfaceImage

gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

face_cascade = cv2.CascadeClassifier('venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
facecam = Facecam(face_cascade).start()
img = facecam.read()
aii = ArrayInterfaceImage(img, 'BGR')
soul = pyglet.image.load('chihiro.png')
soul_sprite = pyglet.sprite.Sprite(soul, x=0, y=0)
image = aii.texture
window = pyglet.window.Window(vsync=False)
window.height = image.height
window.width = image.width
fps_display = FPSDisplay(window)
box = Rectangle(x=0, y=0, width=100, height=100)


@window.event
def on_draw():
    window.clear()
    image.blit(0, 0, 0)
    img = facecam.read()
    aii.view_new_array(img)
    fps_display.draw()
    soul_sprite.draw()


def follow_face(x, y, width, height):
    print('HI!')
    soul_sprite.x = x + (width//2) - soul_sprite.width//2
    soul_sprite.y = y + (height//2) - soul_sprite.height//2


facecam.on_face_move = follow_face

if __name__ == '__main__':
    count = 0
    timer = time.time()
    while 1:
        pyglet.clock.tick()
        for window in pyglet.app.windows:
            window.switch_to()
            window.dispatch_events()
            window.dispatch_event('on_draw')
            window.flip()
            count += 1
        time.sleep(1 / 60)
