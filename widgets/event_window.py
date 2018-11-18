from typing import List, Dict, Any, Callable

from pyglet.window import Window


class EventWindow(Window):
    _event_stack: List[Dict[Any, Any]]
    events: dict = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_handler(self, name: str, handler: Callable) -> None:
        """
        Override the set_handler in EventDispatcher to allow multiple event handlers
        :param name:    Name of the event
        :param handler: The event handler
        """
        if name not in self.events:
            self.events[name] = []
        self.events[name].append(handler)

        def callback(*args, **kwargs):
            for event_handler in self.events[name]:
                event_handler(*args, **kwargs)

        if type(self._event_stack) is tuple:
            self._event_stack = [{}]

        self._event_stack[0][name] = callback

