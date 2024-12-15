from zenplate.plugins.base import Plugin


class DataPlugin(Plugin):
    @classmethod
    def __call__(cls, *args, **kwargs):
        return cls.func(*args, **kwargs)
