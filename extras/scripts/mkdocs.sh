#!/bin/bash
THIS_DIR="$(dirname "$(realpath "$0")")"
PROJECT_ROOT="$(dirname "$(dirname "$THIS_DIR")")"
pushd "$THIS_DIR/../docs"

if [ ! -f "$(which mkdocs)" ]; then
    echo "mkdocs not found in PATH"
    echo "You probably need to activate the venv and run 'pip install $PROJECT_ROOT[development]'"
    exit 1
fi

mkdocs build

popd 2&>1 /dev/null
if [ "$?" == "2" ]; then
    exit 0
fi
