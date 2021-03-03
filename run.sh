#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "use: ./run.sh {app.py}"
    exit 1
fi

export FLASK_APP=$1
export FLASK_ENV=development
flask run 