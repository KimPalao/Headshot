from typing import Callable
from .event_widget import EventWidget
from pyglet.window import Window


class Hoverable(EventWidget):
    _mouse_enter: Callable = None
    _mouse_leave: Callable = None
    _hover_cursor: str = ''
    hovered: bool = False

    def _mouse_enter_base(self) -> bool:
        """
        The base event handler for when a mouse pointer hovers into an element
        Returning False means the user has hovered inside but hasn't left yet
        :return: bool
        """
        if self.hovered:
            return False
        self.hovered = True
        window: Window = self.get_window()
        # Set the cursor as defined by the developer
        # By default, window.CURSOR_HAND will be used
        cursor = window.get_system_mouse_cursor(self._hover_cursor or window.CURSOR_HAND)
        window.set_mouse_cursor(cursor)
        return True

    def _mouse_leave_base(self):
        """
        The base event handler for when a mouse pointer hovers out of an element
        Returning False means the user has hovered outside but hasn't returned yet
        :return: bool
        """
        if not self.hovered:
            return False
        self.hovered = False
        window: Window = self.get_window()
        # Return the cursor to normal
        cursor = window.get_system_mouse_cursor(window.CURSOR_DEFAULT)
        window.set_mouse_cursor(cursor)
        return True

    @property
    def mouse_enter(self):
        if self._mouse_enter:
            return self._mouse_enter
        return self._mouse_enter_base

    @mouse_enter.setter
    def mouse_enter(self, value):
        def new_mouse_enter():
            if self._mouse_enter_base():
                value()
        self._mouse_enter = new_mouse_enter

    @property
    def mouse_leave(self):
        if self._mouse_leave:
            return self._mouse_leave
        return self._mouse_leave_base

    @mouse_leave.setter
    def mouse_leave(self, value):
        def new_mouse_leave():
            if self._mouse_leave_base():
                value()
        self._mouse_leave = new_mouse_leave

    def on_mouse_motion(self, x, y, dx, dy):
        if self.check_if_in_bounds(x, y):
            self.mouse_enter()
        else:
            self.mouse_leave()


Hoverable.register_event_type('on_mouse_motion')
