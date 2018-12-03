from typing import List, Dict, Any, Callable

from pyglet.window import Window, key
# from pyglet import clock

from pyglet import clock
from interfaces.interface import Interface


class EventWindow(Window):
    _event_stack: List[Dict[Any, Any]]
    current_interface: Interface = None
    events: dict = {}
    interface_history: List[Interface] = []

    def __init__(self, *args, **kwargs):
        keys = key.KeyStateHandler()
        self.push_handlers(keys)
        super().__init__(*args, **kwargs)

    def set_handler(self, name: str, handler: Callable) -> None:
        """
        Override the set_handler in EventDispatcher to allow multiple event handlers
        :param name:    Name of the event
        :param handler: The event handler
        """
        if name not in self.events:
            # self.events[name] = []
            self.events[name] = {}
        self.events[name][id(handler)] = handler

        # self.events[name].append(handler)

        def callback(*args, **kwargs):
            # for event_handler in self.events[name]:
            for event_handler in self.events[name].values():
                event_handler(*args, **kwargs)

        if type(self._event_stack) is tuple:
            self._event_stack = [{}]

        # self._event_stack[0][name] = callback
        self._event_stack[0][name] = handler

    def refresh_callbacks(self, *names):
        names = names or self.events.keys()
        for name in names:
            def callback(*args, **kwargs):
                # for event_handler in self.events[name]:
                for event_handler in self.events[name].values():
                    event_handler(*args, **kwargs)

            if type(self._event_stack) is tuple:
                self._event_stack = [{}]

            self._event_stack[0][name] = callback

    def remove_handler(self, name: str, handler: Callable) -> None:
        if name not in self.events:
            return
        if id(handler) not in self.events[name]:
            return
        self.events[name].pop(id(handler))
        self.refresh_callbacks(name)

    def load_interface(self, interface: Interface):
        self.clear()
        # clock._schedule_items = []
        # clock._schedule_interval_items = []
        if self.current_interface:
            for func, interval in self.current_interface.scheduled_functions:
                print(f'Unscheduling {func}')
                clock.unschedule(func)
                # clock.unschedule(func.__name__)
            # if hasattr(self.current_interface, '__del__'):
            #     self.current_interface.__del__()
            # del self.current_interface
            # print(clock._schedule_items)
            self.current_interface.clean()
            print('self.current_interface', self.current_interface)
        self.current_interface = None

        #
        # self.interface_history.append(self.current_interface)

        # @self.event
        def on_draw():
            self.clear()
            interface.on_draw()

        self.on_draw = on_draw
        self.current_interface = interface

    def on_resize(self, width, height):
        self.current_interface.resize()
        super().on_resize(width, height)
