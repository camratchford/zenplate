#!/bin/bash

THIS_DIR="$(dirname "$(realpath "$0")")"
pushd "$THIS_DIR"

zenplate --var-file vars/specific_vars.yml \
    --var-file vars/general_vars.yml \
    --force \
    templates output_dir