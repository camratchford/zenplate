import logging
from typing import Type, Callable

from zenplate.exceptions import ZenplateException


logger = logging.getLogger(__name__)


class ZenplateBasePluginException(ZenplateException):
    pass


class Plugin:
    func: Callable
    name: str = ""
    kwargs: dict = {}

    def __init__(self):
        if not hasattr(self, "func"):
            raise ZenplateBasePluginException("Used without bound function")

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()

    @classmethod
    def __call__(cls, *args, **kwargs):
        try:
            return cls.func(*args, **kwargs)
        except Exception as e:
            ZenplateBasePluginException(f"Error invoking plugin: {e}")


def plugin_wrapper(name: str, cls: Type[object], **kwargs):
    """
    Decorator to turn your function into a Plugin object.
    Copy this function and change the value of Plugin for your own base class.
    """

    def decorator(func):
        if not hasattr(cls, "__call__"):
            raise ZenplateBasePluginException(
                "Base class does not have a __call__ method"
            )

        class_properties = {
            "__module__": getattr(func, "__module__"),
            "__doc__": func.__doc__,
            "name": name,
            "func": func,
        }
        class_properties.update(kwargs)
        try:
            return type(func.__name__, (cls,), class_properties)
        except Exception as e:
            raise ZenplateBasePluginException(
                f"Error creating plugin from spec: {class_properties}\n{e}"
            )

    return decorator
