# Python Module Plugin Example

This example demonstrates a functional set of plugins that zenplate imports through matching python packages whose names start with `zenplate_plugin`.
Any python package that starts with `zenplate_plugin` will be searched for plugins that are subclasses of the 
`zenplate.plugins.DataPlugin`, `zenplate.plugins.JinjaFilterPlugin`, and `zenplate.plugins.JinjaTestPlugin` classes.

You can construct a plugin by decorating the function with the `zenplate.plugins.plugin_wrapper` decorator, 
providing a name and corresponding parent class.


## Overview

The example consists of the following files:

- `vars/vars.yml` - Contains the variables used by the plugins, just a single list of file names. 
  Some are not adherent to the python module naming convention.
- `plugins/jinja_plugins.py` - Contains 2 plugins. 
  - `valid_python_module_name` - A Jinja test plugin that checks if a string is a valid python module name.
  - `make_slug` - A Jinja filter plugin that takes a string and returns a slugified version of it.
- `plugins/data_plugins.py` - Contains a single data plugin.
  - `get_files` - A data plugin that lists the names of files in a directory.
- `templates/file_list.txt` - A template that should format a list of files, using the two plugins to ensure that they have the correct format.

## Usage

1. Ensure the zenplate package is installed, see the main README.md for more information.
2. Install the python package that 2 of the plugins require for functionality `pip install python-slugify`
3. Run the corresponding `run_example.sh` / `run_example.ps1` script to execute the example.
4. Inspect the files in the `output_dir` directory to see the results.