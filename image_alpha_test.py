import pyglet
from game_objects.projectile import Projectile
from shapes.rectangle import Rectangle

# image = cv2.imread('projectiles/minecraft_sword.png')
window = pyglet.window.Window(fullscreen=True)
projectile = Projectile(src='projectiles/minecraft_sword.png')
projectile.x = window.width / 2
projectile.y = window.height / 2
rectangle = Rectangle(x=projectile.x, y=projectile.y, width=projectile.width, height=projectile.height,
                      color=(255, 255, 255, 255))
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
