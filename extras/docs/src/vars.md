# About Zenplate Variables

The jinja templating is supplied with variables to render the template. 
These variables can be supplied in a few different ways.

These variable sources are applied in order, with later sources overwriting earlier sources.

- Configuration file key `jinja_global_vars`
  - All keys under the `jinja_global_vars` key in the configuration file will be used as variables.
  - See [Configuration Reference](config.md) for more information 
- Data plugins
  - Data plugins can be used to supply variables to the template.
  - See [Data Plugins](plugins.md#Data\ Plugins) for more information
- Variable files 
  - YAML files provided with the CLI option `--var-file`
  - Can be used multiple times `--var-file="file1.yaml" --var-file="file2.yaml"`
  - Variables follow standard [YAML syntax](https://yaml.org/spec/1.2.2/)
- Inline variables
  - CLI option `--var="key=value"`
  - Can be used multiple times `--var="key1=value1" --var="key2=value2"`