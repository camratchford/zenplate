#!/bin/bash

THIS_DIR="$(dirname "$(realpath "$0")")"
pushd "$THIS_DIR"

zenplate --config-file config.yml \
    --force \
    templates output_dir

popd