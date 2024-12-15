#!/bin/bash
THIS_DIR="$(dirname "$(realpath "$0")")"
PROJECT_ROOT="$(dirname "$(dirname "$THIS_DIR")")"
pushd "$PROJECT_ROOT"


rm -rf sdist
mkdir -p sdist
python -m build --wheel --outdir sdist
python -m build --sdist --outdir sdist
twine upload --verbose --repository pypi sdist/*

popd