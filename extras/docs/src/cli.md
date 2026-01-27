# Zenplate Command Line Options

## Arguments

Zenplate has 2 positional arguments, they are both required unless the `--export-config` flag is set.


| Argument        | Type            | Description                                                      |
|-----------------|-----------------|------------------------------------------------------------------|
| `template_file` | path (file/dir) | The path to the jinja template / directory that Zenplate will render  |
| `output`        | path (file/dir) | The path to where you'll find the output of Zenplate                  |


## Options

| Option                    | Type        | Description                                                                                |
|---------------------------|-------------|--------------------------------------------------------------------------------------------|
| `--config-file`           | path (file) | The location of the yaml configuration file                                                |
| `--var`                   | text        | A 'varname=value' pair representing a variable, may be used multiple times                 |
| `--var-file`              | path (file) | The path to a yaml file containing key: value pairs, representing variables                |
| `--log-path`              | path (file) | The location of the log file                                                               |
| `--export-config`         | flag        | When true, the current set of configuration parameters will be exported to `--config-file` |
| `--force`                 | flag        | When true, output will overwrite any file in that path                                     |
| `--stdout`                | flag        | Write rendered template to stdout                                                          |
| `--load-environment-vars` | flag        | Will load environment variables in as jinja variables                                      |
| `--install-completion`    | flag        | Install completion for the current shell                                                   |
| `--show-completion`       | flag        | Show completion for the current shell, to copy it or customize the installation            |
| `--help`                  | flag        | Show this message and exit                                                                 |

