from typing import Callable


class A:
    name: str = ''
    func: Callable = None

    def __init__(self, name, func):
        self.name = name
        self.func = func

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)


# class AA(A):
#     pass


class B:
    items = []

    def __init__(self):
        @self.add_item('test')
        def test():
            print('HELLO WORLD')

    def add_item(self, name: str):
        def decorator(func):
            a = A(name=name, func=func)
            self.items.append(a)
        return decorator


if __name__ == '__main__':
    b = B()
    print(b.items)
    print(b.items[0]())
