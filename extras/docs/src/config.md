## Zenplate Configuration Reference

| Option              | Environment Variable       | Type | Description                                                |
|---------------------|----------------------------|------|------------------------------------------------------------|
| `template_path`     | `ZENPLATE_TEMPLATE_FILE`   | path | Path to the template file/directory.                       |
| `output_path`       | `ZENPLATE_OUTPUT_PATH`     | path  | Path to the output file/directory.                         |
| `var_files`         | `ZENPLATE_VAR_FILES`       | list | List of paths to variable files.                           |
| `jinja_config`      | ...                        | dict | Jinja configuration options.                               |
| `jinja_global_vars` | ...                        | dict | Global variables to be passed to the Jinja environment.    |
| `dry_run`           | `ZENPLATE_DRY_RUN`         | bool | If true, the template will not be rendered.                |
| `log_level`         | `ZENPLATE_LOG_LEVEL`       | str  | Log level for the application.                             |
| `log_file`          | `ZENPLATE_LOG_FILE`        | path | Path to the log file.                                      |
| `stdout`            | `ZENPLATE_STDOUT`          | bool | If true, the rendered template will be printed to stdout.  |
| `force_overwrite`   | `ZENPLATE_FORCE_OVERWRITE` | bool | If true, the output file will be overwritten if it exists. |
| `plugin_config`     | ...                        | dict | Plugin configuration options.                              |


## Exporting config

Most of the configuration can be done via the CLI options, with a few exceptions. 
The `config_file` option can be used to export the current configuration to a file. 
This can be useful for saving a configuration that is used frequently.

You can export the current configuration to a file by using the `--export-config` option, 
specifying the location of the dumped config with `--config-file` option.

```shell
zenplate --export-config --config-file /path/to/config.yml
```

With no additional options provided, the exported configuration will look like this:
```yaml
template_path: null
output_path: null
var_files: []
jinja_config:
  trim_blocks: false
  lstrip_blocks: false
  keep_trailing_newline: false
jinja_global_vars: {}
dry_run: false
log_level: ERROR
stdout: false
force_overwrite: false
plugin_config:
  path_modules: []
  named_modules:
  - zenplate.plugins.default_plugins.data_plugins
  - zenplate.plugins.default_plugins.jinja_plugins
  plugin_kwargs:
    ls:
      path: .
```

