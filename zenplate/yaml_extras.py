import pathlib
import yaml


class PathObject(pathlib.WindowsPath):
    pass


def pathobj_rep(dumper: yaml.Dumper, data):
    if isinstance(data, pathlib.Path):
        data = str(data.resolve())
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)
