import os
import time
import traceback

import pyglet
from pyglet import clock, app
from pyglet.window import get_platform

platform = get_platform()
display = platform.get_default_display()
screen = display.get_default_screen()
window = pyglet.window.Window(width=screen.width, height=screen.height, resizable=True)
window.maximize()

base_path = os.path.join('..', 'images', 'space_background_pack', 'layers')

background = pyglet.image.load(os.path.join(base_path, 'parallax-space-background.png'))
background_sprite = pyglet.sprite.Sprite(background)
scale = window.width / background.width
background_sprite.scale = scale

big_planet = pyglet.image.load(os.path.join(base_path, 'parallax-space-big-planet.png'))
big_planet_sprite = pyglet.sprite.Sprite(big_planet)
big_planet_sprite.scale = scale / 2
big_planet_sprite.x = window.width / 2
big_planet_sprite.y = window.height / 2

far_planet = pyglet.image.load(os.path.join(base_path, 'parallax-space-far-planets.png'))
far_planet_sprite = pyglet.sprite.Sprite(far_planet)
far_planet_sprite.scale = scale / 2
far_planet_sprite.x = window.width - far_planet_sprite.width
far_planet_sprite.y = window.height - far_planet_sprite.height

ring_planet = pyglet.image.load(os.path.join(base_path, 'parallax-space-ring-planet.png'))
ring_planet_sprite = pyglet.sprite.Sprite(ring_planet)
ring_planet_sprite.scale = scale / 2
ring_planet_sprite.x = 100
ring_planet_sprite.y = 100

stars = pyglet.image.load(os.path.join(base_path, 'parallax-space-stars.png'))
stars_sprite = pyglet.sprite.Sprite(stars)
stars_sprite.scale = scale


@window.event
def on_draw():
    window.clear()
    background_sprite.draw()
    big_planet_sprite.draw()
    far_planet_sprite.draw()
    ring_planet_sprite.draw()
    stars_sprite.draw()

    big_planet_sprite_depth = 3
    far_planet_sprite_depth = 10
    ring_planet_sprite_depth = 5
    stars_sprite_depth = 8

    big_planet_sprite.x = big_planet_sprite.x - 1 * (1 / big_planet_sprite_depth)
    if big_planet_sprite.x + big_planet_sprite.width <= 0:
        big_planet_sprite.x = window.width
    far_planet_sprite.x = far_planet_sprite.x - 1 * (1 / far_planet_sprite_depth)
    if far_planet_sprite.x + far_planet_sprite.width <= 0:
        far_planet_sprite.x = window.width
    ring_planet_sprite.x = ring_planet_sprite.x - 1 * (1 / ring_planet_sprite_depth)
    if ring_planet_sprite.x + ring_planet_sprite.width <= 0:
        ring_planet_sprite.x = window.width
    stars_sprite.x = stars_sprite.x - 1 * (1 / stars_sprite_depth)
    if stars_sprite.x + stars_sprite.width <= 0:
        stars_sprite.x = window.width


if __name__ == '__main__':
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
            time.sleep(1 / 60)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        input()
