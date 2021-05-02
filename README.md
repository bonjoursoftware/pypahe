# [Bonjour Software Limited](https://bonjoursoftware.com/)

[![CI](https://github.com/bonjoursoftware/pypahe/actions/workflows/main.yml/badge.svg)](https://github.com/bonjoursoftware/pypahe/actions/workflows/main.yml)
[![CodeQL](https://github.com/bonjoursoftware/pypahe/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/bonjoursoftware/pypahe/actions/workflows/codeql-analysis.yml)

## pypahe

Bonjour Software's pypahe is a **Py**thon **Pa**ckage **He**lper command-line tool.

### Usage

#### Setup

Ensure [Pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today) is installed first. Then download dependencies
and activate a virtual environment with:

```shell
pipenv sync
pipenv shell
```

#### Commands

The following commands need to be run inside an activated virtual environment:

- find latest package version

```shell
python pypahe.py latest boto3
1.17.62
```

- show available commands

```shell
python pypahe.py --help
```

#### Shell wrapper

A shell script wrapper is available for convenience; it automates the creation and activation of a virtual environment
then calls `pypahe.py` from inside the virtual environment:

```shell
./pypahe.sh latest flake8
3.9.1
```
