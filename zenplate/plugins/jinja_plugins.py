import logging

from zenplate.exceptions import ZenplateException
from zenplate.plugins.base import Plugin

logger = logging.getLogger(__name__)


class ZenplateJinjaPluginException(ZenplateException):
    pass


class JinjaFilterPlugin(Plugin):
    @classmethod
    def __call__(cls, *args, **kwargs) -> str:
        try:
            return cls.func(*args, **kwargs)
        except Exception as e:
            raise ZenplateJinjaPluginException(f"Error invoking Jinja filter plugin: {e}")


class JinjaTestPlugin(Plugin):
    @classmethod
    def __call__(cls, *args, **kwargs) -> bool:
        try:
            return bool(cls.func(*args, **kwargs))
        except Exception as e:
            raise ZenplateJinjaPluginException(f"Error invoking Jinja test plugin: {e}")
