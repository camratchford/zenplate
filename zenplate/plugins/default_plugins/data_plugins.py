import os
import sys
from pathlib import Path

from zenplate.plugins.base import plugin_wrapper
from zenplate.plugins.data_plugins import DataPlugin


@plugin_wrapper("ls", DataPlugin)
def list_path_contents(path: str, suffix: str = None):
    path_contents = Path(path).iterdir()
    if suffix:
        path_contents = [i for i in path_contents if i.suffix == suffix]
    return [str(i.resolve()) for i in path_contents]


@plugin_wrapper("defaults", DataPlugin)
def data_default_variables(*args, **kwargs):
    variables = {}
    os_vars = {
        "os": {
            "name": os.name,
        }
    }
    variables.update(os_vars)

    sys_vars = {
        "sys": {
            "defaultencoding": sys.getdefaultencoding(),
            "platform": sys.platform,
            "winver": sys.getwindowsversion().major
            if sys.platform == "win32"
            else None,
        }
    }
    variables.update(sys_vars)

    env = {"environ": {}}
    env["environ"].update(os.environ)
    variables.update(env)

    return variables
