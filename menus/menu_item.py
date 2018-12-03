from typing import Callable


class MenuItem:
    name: str = ''
    func: Callable = None

    def __init__(self, name, func):
        self.name = name
        self.func = func

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)

    def __repr__(self):
        return f'MenuItem named {self.name}'

