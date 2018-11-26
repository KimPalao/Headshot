import pyglet

window = pyglet.window.Window()
label = pyglet.text.Label()
button = pyglet.input.Button('button')
# text_box = pyglet.text.layout.IncrementalTextLayout(label, height=100, width=100)
# caret = pyglet.text.caret.Caret(text_box)

# TODO: Implement the configuration screen


@button.event
def on_press():
    print('The button was pressed.')


@window.event
def on_draw():
    window.clear()
    label.draw()


if __name__ == '__main__':
    pyglet.app.run()
