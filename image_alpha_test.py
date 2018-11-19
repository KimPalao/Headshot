import cv2
import pyglet
from widgets.projectile import Projectile
from widgets.rectangle import Rectangle

# image = cv2.imread('projectiles/minecraft_sword.png')
window = pyglet.window.Window(fullscreen=True)
projectile = Projectile(image_src='projectiles/minecraft_sword.png')
projectile.x = window.width / 2
projectile.y = window.height / 2
rectangle = Rectangle(x=projectile.x, y=projectile.y, width=projectile.width, height=projectile.height,
                      color=(255, 255, 255))
rectangle.x -= rectangle.width/2
rectangle.y -= rectangle.height/2


@window.event
def on_draw():
    window.clear()
    rectangle.draw()
    projectile.draw()


# for row in image:
#     for cell in row:
#         print(cell)


if __name__ == '__main__':
    pyglet.app.run()
