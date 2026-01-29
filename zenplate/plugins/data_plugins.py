import logging

from zenplate.exceptions import ZenplateException
from zenplate.plugins.base import Plugin

logger = logging.getLogger(__name__)


class ZenplateDataPluginException(ZenplateException):
    pass


class DataPlugin(Plugin):
    @classmethod
    def __call__(cls, *args, **kwargs):
        try:
            return cls.func(*args, **kwargs)
        except Exception as e:
            raise ZenplateDataPluginException(f"Error invoking data plugin: {e}")
