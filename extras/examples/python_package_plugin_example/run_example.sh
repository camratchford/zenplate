#!/bin/bash

THIS_DIR="$(dirname "$(realpath "$0")")"
pushd "$THIS_DIR"

zenplate --var-file vars/vars.yml \
    --force \
    templates output_dir

popd