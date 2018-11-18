import os
from datetime import datetime

import cv2
import json
import pyglet
from pyglet.window import FPSDisplay
from widgets.event_window import EventWindow
from widgets.button import Button
from widgets.textbox import TextBox


with open('config.json') as config_file:
    config = json.loads(config_file.read())
print(config)

if config['font']['names']:
    print(tuple(config['font']['names']))
    sans_serif = pyglet.font.load(tuple(config['font']['names']), 16)
    # sans_serif = pyglet.font.load('Microsoft YaHei UI Light', 16)

# window = pyglet.window.Window()
window = EventWindow()
pyglet.gl.glClearColor(1, 1, 1, 1)

label = pyglet.text.Label(f'Hello {config["name"]["first"]}!',
                          font_size=36,
                          x=window.width // 2,
                          anchor_x='center',
                          anchor_y='center',
                          color=(0, 0, 0, 255))
button_press_label = pyglet.text.Label('You haven\'t pressed anything yet', color=(0, 0, 0, 255))
button = Button('Take a picture', color=(0, 0, 0, 255), padding=(5,))

fps_display = FPSDisplay(window)


text_box = TextBox(100, x=window.width//2, y=window.height//2)
# text_box.x = (window.width - text_box.width) // 2
# text_box.y = (window.height - text_box.height) // 2
print(text_box.x, text_box.y, text_box.underline)


def reposition_button_press_label():
    button_press_label.x = window.width // 2 - button_press_label.content_width // 2
    button_press_label.y = button_press_label.content_height


@button.event('on_mouse_press')
def test(x, y, btn, mod):
    date: datetime = datetime.now()
    filename: str = os.path.join('capture', f'{date:%Y_%m_%d__%H%I%S}.jpg')
    print(filename)


@window.event
def on_draw():
    window.clear()
    # label.draw()
    button.draw()
    reposition_button_press_label()
    button_press_label.draw()
    fps_display.draw()
    text_box.draw()


@window.event
def on_key_press(symbol: int, modifiers: int):
    button_press_label.text = f'You pressed {chr(symbol)}'
    reposition_button_press_label()


# window.push_handlers(text_box, button)
window.push_handlers(button, text_box)

if __name__ == '__main__':
    pyglet.app.run()
