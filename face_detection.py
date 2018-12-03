import time
from shapes.rectangle import Rectangle
import cv2
import pyglet
from pyglet import gl
from pyglet.window import FPSDisplay
from pygarrayimage.arrayimage import ArrayInterfaceImage

gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

face_cascade = cv2.CascadeClassifier('venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
# facecam = Facecam(face_cascade, src='ACM App.mp4').start()
img = cv2.imread('faces/four.jpeg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
aii = ArrayInterfaceImage(img, 'BGR')
soul = pyglet.image.load('chihiro.png')
soul_sprite = pyglet.sprite.Sprite(soul, x=0, y=0)
image = aii.texture
window = pyglet.window.Window(vsync=False)
window.maximize()
# window.height = image.height
# window.width = image.width
fps_display = FPSDisplay(window)
box = Rectangle(x=0, y=0, width=100, height=100)


@window.event
def on_draw():
    window.clear()
    image.blit(0, 0, 0)
    # img = facecam.read()
    aii.view_new_array(img)
    fps_display.draw()
    soul_sprite.draw()


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
