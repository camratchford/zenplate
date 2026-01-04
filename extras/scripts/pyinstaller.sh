#!/bin/bash
THIS_DIR="$(dirname "$(realpath "$0")")"
PROJECT_ROOT="$(dirname "$(dirname "$THIS_DIR")")"
pushd "$THIS_DIR"

if [ ! -f "$(which pyinstaller)" ]; then
    echo "pyinstaller not found in PATH"
    echo "You probably need to activate the venv and run 'pip install $PROJECT_ROOT[development]'"
    exit 1
fi

pyinstaller -y --clean --console --onefile --uac-admin \
    --name "zenplate" \
    --paths "zenplate" \
    --icon "$THIS_DIR/icon/zenplate.ico" \
    --log-level "FATAL" \
    "$PROJECT_ROOT/zenplate/cli.py"
