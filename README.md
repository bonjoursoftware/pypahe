# pypahe

[![CI](https://github.com/bonjoursoftware/pypahe/actions/workflows/main.yml/badge.svg)](https://github.com/bonjoursoftware/pypahe/actions/workflows/main.yml)
[![CodeQL](https://github.com/bonjoursoftware/pypahe/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/bonjoursoftware/pypahe/actions/workflows/codeql-analysis.yml)

[Bonjour Software](https://bonjour.software) pypahe is a **Py**thon **Pa**ckage **He**lper command-line tool.

## Requirements

- Python >= 3.9.4

## Usage

- print the latest available version of a given package:

```shell
./pypahe.sh latest boto3
1.17.62
```

- print a given Pipfile or Poetry pyproject where all packages have been upgraded to their latest versions:

```shell
./pypahe.sh upgrade "$(cat /path/to/package_config)"
```

Tip: the Pipfile or Poetry pyproject file can be upgraded in place with:

```shell
./pypahe.sh upgrade "$(cat /path/to/package_config)" > /path/to/package_config
```

- print manual:

```shell
./pypahe.sh  --help
```

Tip: the `--help` argument also works on subcommands:

```shell
./pypahe.sh latest --help
./pypahe.sh upgrade --help
```
