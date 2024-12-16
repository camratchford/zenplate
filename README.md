
# Zenplate

A pluggable CLI templating tool leveraging the powers of Jinja2 and YAML

___

Documentation can be found at [zenplate.scallawag.ca](https://zenplate.scallawag.ca)

## Features

- Single file templating - render a single file with variables
- Directory templating - render all files in a directory, including file and directory names
- Plugin system - extend the functionality of Zenplate with custom data, filter, and test plugins

## Ideas on how to start using Zenplate

- In place of a heavier templating tool like cookiecutter or Ansible.
- Generate a README.md or pyproject.toml file for a new project
- Generate a directory full of boilerplate code, keeping the structure consistent.
- Write a script to send you an Zenplate templated email based on system information.
- Develop your own data plugins to pull data from databases, APIs, or other sources.

## Installation

(Optionally) 
Clone the repo
```shell
pushd ~
git clone https://github.com/camratchford/zenplate
```

Create a virtual environment and install the package
```shell
cd zenplate
python3 -m venv venv
source venv/bin/activate
# If you cloned the repo
pip install .
# If you didn't clone the repo
pip install zenplate
```


(Optional) Set up the recommended workspace layout
```shell
mkdir -p ~/zenplate/templates ~/zenplate/output ~/zenplate/vars
cd ~/zenplate
zenplate --export-config --config-file zenplate.yml
echo 'source ~/zenplate/venv/bin/activate' >> .zenplaterc
echo 'export ZENPLATE_CONFIG_FILE="'$PWD'/zenplate.yml"' >> .zenplaterc
source .zenplaterc
```

(Alternative to the workspace layout) link the python script to your path
```shell
ln -s ~/zenplate/venv/bin/zenplate /usr/local/bin/zenplate
```

## Contributing

This is a small hobby project, but I'm open to contributions. Please feel free to report any issues or submit a pull request.

See [CONTRIBUTING.md](.github/CONTRIBUTING.md) for more information.


## Built with (Primarily)

- [Jinja2](https://jinja.palletsprojects.com/en/stable/) for templating
- [PyYAML](https://pyyaml.org/) for parsing / dumping YAML files
- [Typer](https://typer.tiangolo.com/) for the CLI


## License

Distributed under the CC0 1.0 Universal License. See [LICENSE](LICENSE) for more information.

