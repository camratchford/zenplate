#!/bin/bash

THIS_DIR="$(dirname "$(realpath "$0")")"
pushd "$THIS_DIR"

zenplate \
    -v 'title=How do you make a cheeseburger?' \
    --var-file 'vars/vars.yml' \
    --force \
    'templates/readme_template.md.j2' 'output_files/README.md'

popd