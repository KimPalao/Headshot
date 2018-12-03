import inspect
from past.builtins import basestring
from pyglet.event import EventDispatcher
from pyglet.canvas import get_display
from abc import ABC


class EventWidget(EventDispatcher, ABC):
    x: int
    y: int
    width: int
    height: int

    @staticmethod
    def get_window():
        """
        Returns the current window
        :return: Window
        """
        return get_display().get_windows()[0]

    def check_if_in_bounds(self, x: int, y: int) -> bool:
        """
        Checks if the user clicked inside the bounds of the widget
        :param x: X-coordinate with respect to the origin (bottom left)
        :param y: Y-coordinate with respect to the origin (bottom left)
        :return: bool
        """
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def event(self, *args):
        """
        Override the event function of EventDispatcher
        """
        if len(args) == 0:  # @window.event()
            def decorator(func):
                setattr(self, func.__name__, func)

            return decorator
        elif inspect.isroutine(args[0]):  # @window.event
            func = args[0]
            name = func.__name__
            setattr(self, name, func)
            return args[0]
        elif isinstance(args[0], basestring):  # @window.event('on_resize')
            name = args[0]

            def decorator(func):
                setattr(self, name, func)

            return decorator
