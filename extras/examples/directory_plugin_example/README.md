# Directory Plugin Example

This example demonstrates a functional set of plugins that zenplate imports through the `plugin_config['path_modules']` key.
It is a less formal, but often more practical was to import and use plugins.

Any directories listen in the `plugin_config['path_modules']` config key will be searched for plugins that
are subclasses of the `zenplate.plugins.DataPlugin`, `zenplate.plugins.JinjaFilterPlugin`, and `zenplate.plugins.JinjaTestPlugin` classes.

You can construct a plugin by decorating the function with the `zenplate.plugins.plugin_wrapper` decorator, 
providing a name and corresponding parent class.

## Overview

The example consists of the following files:

- `vars/vars.yml` - Contains the variables used by the plugins, just a single list of file names. 
  Some are not adherent to the python module naming convention.
- `plugin_package/zenplate_plugin_example` - The python package containing the plugins.
  - `plugin_package/pyproject.toml` - A standard [pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) file. Contains the list of package requirements and registers the package as a python module..
  - `plugin_package/__init__.py` - A standard `__init__.py` file that marks the directory as a python package. Importantly, it also contains a listing of its contents in the `__all__` variable.
  - `plugin_package/zenplate_plugin_example/data_plugins.py` - Contains a single data plugin.
    - `get_files` - A data plugin that lists the names of files in a directory.
  - `plugin_package/zenplate_plugin_example/jinja_plugins.py`
    - `valid_python_module_name` - A Jinja test plugin that checks if a string is a valid python module name.
    - `make_slug` - A Jinja filter plugin that takes a string and returns a slugified version of it.
- `templates/file_list.txt` - A template that should format a list of files, using the two plugins to ensure that they have the correct format.

## Usage

1. Ensure the zenplate package is installed, see the main README.md for more information.
2. Install the module python package `pip install ./plugin_package`
3. Run the corresponding `run_example.sh` / `run_example.ps1` script to execute the example.
4. Inspect the files in the `output_dir` directory to see the results.

