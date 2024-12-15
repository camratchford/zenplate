from typing import Type, Callable


class Plugin:
    func: Callable
    name: str = ""
    kwargs: dict = {}

    def __init__(self):
        if not hasattr(self, "func"):
            raise TypeError("Used without bound function")

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()

    @classmethod
    def __call__(cls, *args, **kwargs):
        return cls.func(*args, **kwargs)


def plugin_wrapper(name: str, cls: Type[object], **kwargs):
    """
    Decorator to turn your function into a Plugin object.
    Copy this function and change the value of Plugin for your own base class.
    """

    def decorator(func):
        if not hasattr(cls, "__call__"):
            raise TypeError("Base class does not have a __call__ method")

        class_properties = {
            "__module__": getattr(func, "__module__"),
            "__doc__": func.__doc__,
            "name": name,
            "func": func,
        }
        class_properties.update(kwargs)

        return type(func.__name__, (cls,), class_properties)

    return decorator
