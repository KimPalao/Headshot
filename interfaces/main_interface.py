from pyglet.text import Label

from .interface import Interface


class MainInterface(Interface):
    title_label: Label = None

    def __init__(self):
        self.title_label = Label('Headshot')

    def on_bind(self):
        self.title_label.x = self.window.width
        pass

    def on_draw(self):
        pass
