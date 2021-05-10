# pypahe

[![CI](https://github.com/bonjoursoftware/pypahe/actions/workflows/main.yml/badge.svg)](https://github.com/bonjoursoftware/pypahe/actions/workflows/main.yml)
[![CodeQL](https://github.com/bonjoursoftware/pypahe/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/bonjoursoftware/pypahe/actions/workflows/codeql-analysis.yml)
[![Docker Build](https://img.shields.io/docker/cloud/build/bonjoursoftware/pypahe.svg)](https://hub.docker.com/r/bonjoursoftware/pypahe/builds)

[Bonjour Software](https://bonjour.software) pypahe is a **Py**thon **Pa**ckage **He**lper command-line tool.

## Requirements

- Docker runtime

## Usage

- print the latest available version of a given package:

```shell
docker run bonjoursoftware/pypahe latest boto3
```

- print a given Pipfile or Poetry pyproject where all packages have been upgraded to their latest versions:

```shell
docker run bonjoursoftware/pypahe upgrade "$(cat /path/to/package_config)"
```

Tip: the Pipfile or Poetry pyproject file can be upgraded in place with:

```shell
docker run bonjoursoftware/pypahe upgrade "$(cat /path/to/package_config)" > /path/to/package_config
```

- print manual:

```shell
docker run bonjoursoftware/pypahe --help
```

Tip: the `--help` argument also works on subcommands:

```shell
docker run bonjoursoftware/pypahe latest --help
docker run bonjoursoftware/pypahe upgrade --help
```
