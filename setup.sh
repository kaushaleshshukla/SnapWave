#!/bin/bash

python -m venv venv
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    # Windows (Git Bash, MSYS, Cygwin)
    source venv/Scripts/activate
else
    # Linux or macOS
    source venv/bin/activate
fi

# pip install -r $PWD/backend/requirements.txt --no-dependencies
pip install -r backend/requirements.txt