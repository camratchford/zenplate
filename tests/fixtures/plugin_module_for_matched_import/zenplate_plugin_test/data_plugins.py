from zenplate.plugins.base import plugin_wrapper
from zenplate.plugins.data_plugins import DataPlugin


@plugin_wrapper("data", DataPlugin)
def data():
    return "test"
