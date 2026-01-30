import logging

from zenplate.plugins.base import Plugin

logger = logging.getLogger(__name__)


class DataPlugin(Plugin):
    @classmethod
    def __call__(cls, *args, **kwargs):
        try:
            return cls.func(*args, **kwargs)
        except Exception as e:
            raise RuntimeError(f"Error invoking data plugin: {e}")
