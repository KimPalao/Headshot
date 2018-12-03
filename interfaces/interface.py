from abc import ABC, abstractmethod
from typing import Callable

from pyglet.window import Window

from widgets.event_widget import EventWidget
# from .event_window import EventWindow


class Interface(EventWidget, ABC):
    _on_init: Callable = None
    window: Window = None
    scheduled_functions = tuple()

    def _on_init_base(self):
        pass

    @property
    def on_init(self):
        """
        Returns the event handler for mouse presses
        :return: Callable
        """
        if self._on_init:
            return self.on_init
        return self._on_init_base

    @on_init.setter
    def on_init(self, func):
        self._on_init = func

    def bind(self, window):
        self.window = window
        self.on_bind()

    @abstractmethod
    def on_draw(self):
        pass

    @abstractmethod
    def on_bind(self):
        pass
