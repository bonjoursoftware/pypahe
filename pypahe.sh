#!/usr/bin/env bash
if ! pipenv &> /dev/null
then
    echo "Installing pipenv ..."
    pip install -qq pipenv
fi

if [[ ! $(pipenv graph 2> /dev/null) ]]; then
    echo "Installing dependencies and creating virtual environment ..."
    pipenv sync &> /dev/null
fi

pipenv run python pypahe.py "$@"
