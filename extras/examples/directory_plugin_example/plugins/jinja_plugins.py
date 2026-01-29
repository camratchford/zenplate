from re import compile

from slugify import slugify

from zenplate.plugins import JinjaFilterPlugin, JinjaTestPlugin, plugin_wrapper

python_path_regex = r"[^-a-z0-9_]+.py"


@plugin_wrapper("valid_python_module_name", JinjaTestPlugin)
def valid_python_module_name(string: str):
    # Admittedly, this regex is not correct
    return compile(python_path_regex).match(string) is not None


@plugin_wrapper("make_slug", JinjaFilterPlugin)
def make_slug(string: str):
    slug = slugify(string, separator="_", regex_pattern=python_path_regex)
    if not slug.endswith(".py"):
        slug += ".py"
    return slug
