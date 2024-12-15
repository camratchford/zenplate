from datetime import datetime
from pathlib import Path

from yaml import dump

from zenplate.plugins.base import plugin_wrapper
from zenplate.plugins.jinja_plugins import JinjaFilterPlugin, JinjaTestPlugin


@plugin_wrapper("path_exists", JinjaTestPlugin)
def jinja_test_path_exists(path: str):
    return Path(path).exists()


@plugin_wrapper("now", JinjaFilterPlugin)
def jinja_filter_now(fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.now().strftime(fmt)


@plugin_wrapper("datetime_format", JinjaFilterPlugin)
def jinja_filter_datetime_format(value: datetime, fmt: str = "%d-%m-%y %H:%M"):
    return value.strftime(fmt)


@plugin_wrapper("to_yaml", JinjaFilterPlugin)
def jinja_filter_to_yaml(value):
    return dump(value)
