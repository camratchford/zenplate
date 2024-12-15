# Zenplate Plugins

## Importing Plugins

There are 3 ways to import plugins into Zenplate:

Add the plugin to the `path_modules` key in the configuration file.

  - This will allow Zenplate to discover any plugins in the modules provided
  - Ex. `path_modules: ['./plugins']`

Add the plugin to the `named_modules` key in the configuration file.

  - Any Python package that contains a `plugin` module can be added to the `named_modules` key.
  - Use the import path of the package as the value in the list.
  - Ex. `named_modules: ['zenplate.plugins.default_plugins.data_plugins']`

Install a Python module whose name begins with `zenplate_plugin`

  - Any Python package that is installed and begins with `zenplate_plugin` will be imported by Zenplate.
  - Ex. `pip install zenplate_plugin_database` (Doesn't exist ... yet)


## Plugin Types

There are three types of plugins that can be used with Zenplate: data plugins, jinja test plugins, and jinja filter plugins.

### Data Plugins

Data plugins are used to supply variables to the template. These plugins are called before the template is rendered and can be used to pull data from databases, APIs, or other sources.
They are initialized before the template is rendered and can be used to supply variables to the template.

Keyword arguments can be passed to the plugin to customize the data that is returned. 

To do this, supply the arguments in the configuration file under the `plugin_config.plugin_kwargs` key.
Each key under `plugin_kwargs` should be the name of the plugin to pass arguments to. 
The value should be a dictionary of keyword arguments to pass to the plugin.

```yaml
plugin_config:
  path_modules:
    - ./plugins
  named_modules:
  - zenplate.plugins.default_plugins.data_plugins
  - zenplate.plugins.default_plugins.jinja_plugins
  plugin_kwargs:
    ls:
      path: .
```

To use a data plugin in a template, use the name of the plugin as a jinja tag.

The example config above (the default configuration) configured the `ls` plugin to list the files in the current directory.
The `ls` plugin can be used in a template like this:

```jinja
{% for file in ls %}
- {{ file }}
{% endfor %}
```


### Jinja Test Plugins

Jinja test plugins are used to add custom tests to the Jinja environment. 
These tests can be used in the template to check conditions and return a boolean value.

Assuming we have a variable `path` that contains a path to a file or directory, we can use the `path_exists` test plugin to check if the path exists.

```yaml
pathlist: 
  - /this/path/exists
  - /this/path/doesnt/exist 
```

Example for using the builtin 'path_exists' test plugin:

> Note: You must use the `is` keyword inside the if block clause for the test work correctly.

```jinja
{%- for path in pathlist %}
{%- if path is path_exists %}
- {{ path }}
{% endif %}
{% endfor %}
```

The resulting output will be:

```text
- /this/path/exists
```

### Jinja Filter Plugins

Jinja filter plugins are used to add custom filters to the Jinja environment.
These filters can be used in the template to modify the output of variables.

Assuming we have a variable called "site_config" containing some application configuration data, 
we can use the `to_yaml` filter plugin to convert the data to YAML format.

```python
# Conceivably originating from a data plugin
site_config = {
    'name': 'My App',
    'version': '1.0.0',
    'description': 'An example application'
}
```

Example for using the builtin 'to_yaml' filter plugin:

```jinja
{{ site_config | to_yaml }}
```

The resulting output will be:

```yaml
name: My App
version: 1.0.0
description: An example application
```

## Creating your own plugin

This topic is covered in two examples.

- [Directory Plugin Example](https://github.com/camratchford/zenplate/tree/main/extras/examples/directory_plugin_example)
- [Python Package Plugin Example](https://github.com/camratchford/zenplate/tree/master/examples/python_package_plugin_example)