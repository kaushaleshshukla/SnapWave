#!/bin/bash

python -m venv venv
case $(uname | tr '[:upper:]' '[:lower:]') in
  linux*|darwin*)
    # Script for Linux/macOS
    $PWD/venv/bin/activate.bat
    ;;
  msys*|mingw*)
    # Script for Windows (using Git Bash/Cygwin)
    source $PWD/venv/bin/activate
    ;;
  *)
    echo "Unknown OS, cannot execute script"
    exit 1
    ;;
esac

# pip install -r $PWD/backend/requirements.txt --no-dependencies
pip install -r $PWD/backend/requirements.txt