from typing import Callable
from .event_widget import EventWidget


class Focusable(EventWidget):
    _on_focus: Callable = None
    focused: bool = False

    def _on_focus_base(self) -> None:
        """
        The event handler that will be called by default if none are defined
        """
        pass

    @property
    def on_focus(self):
        if self._on_focus:
            return self._on_focus
        return self._on_focus_base

    @on_focus.setter
    def on_focus(self, func):
        def new_on_focus(x, y, button, modifiers):
            if not self.check_if_in_bounds(x, y):
                return
            func(x, y, button, modifiers)

        self._on_focus = new_on_focus

    def on_mouse_press(self, x, y, button, modifiers):
        # TODO: Test out behavior when implementing both Focusable and Clickable
        if self.check_if_in_bounds(x, y):
            self.focused = True
        else:
            self.focused = False
        self.dispatch_event('on_focus')


Focusable.register_event_type('on_focus')
Focusable.register_event_type('on_mouse_press')
