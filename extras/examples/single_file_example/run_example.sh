#!/bin/bash

THIS_DIR="$(dirname "$(realpath "$0")")"
pushd "$THIS_DIR"

zenplate --config-file 'config.yml' \
    --vars 'title=How do you make a cheeseburger?' \
    --var-file 'vars/vars.yml' \
    --force \
    'templates/readme_template.md.j2' 'README.md'

