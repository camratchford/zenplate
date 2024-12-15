from zenplate.plugins.base import Plugin


class JinjaFilterPlugin(Plugin):
    @classmethod
    def __call__(cls, *args, **kwargs) -> str:
        return str(cls.func(*args, **kwargs))


class JinjaTestPlugin(Plugin):
    @classmethod
    def __call__(cls, *args, **kwargs) -> bool:
        return bool(cls.func(*args, **kwargs))
