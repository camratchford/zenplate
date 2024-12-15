from zenplate.plugins.jinja_plugins import JinjaTestPlugin, JinjaFilterPlugin
from zenplate.plugins.base import plugin_wrapper


@plugin_wrapper("jinja_test", JinjaTestPlugin)
def jinja_test(string: str):
    return isinstance(string, str)


@plugin_wrapper("jinja_filter", JinjaFilterPlugin)
def jinja_filter(a_list: list):
    return [i for i in a_list if len(i) > 1]

