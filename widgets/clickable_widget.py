from typing import Callable
from .event_widget import EventWidget


class Clickable(EventWidget):
    _on_mouse_press: Callable = None

    def _on_mouse_press_base(self, x: int, y: int, button: int, modifiers: int) -> None:
        """
        A placeholder function that will be called when the button is clicked.
        :param x:
        :param y:
        :param button:
        :param modifiers:
        """
        pass

    @property
    def on_mouse_press(self):
        """
        Returns the event handler for mouse presses
        :return: Callable
        """
        if self._on_mouse_press:
            return self._on_mouse_press
        return self._on_mouse_press_base

    @on_mouse_press.setter
    def on_mouse_press(self, func):
        def new_on_mouse_press(x, y, button, modifiers):
            # Check first if the user actually clicked inside the button
            if not self.check_if_in_bounds(x, y):
                return
            # Call the function if the user did
            func(x, y, button, modifiers)
        # Change the event handler
        self._on_mouse_press = new_on_mouse_press


Clickable.register_event_type('on_mouse_press')
