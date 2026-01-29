from pathlib import Path

from zenplate.plugins import DataPlugin, plugin_wrapper


@plugin_wrapper("directory_listing", DataPlugin)
def directory_listing(path: str = "."):
    return [i.name for i in Path(path).iterdir() if i.is_file()] if Path(path).is_dir() else []
