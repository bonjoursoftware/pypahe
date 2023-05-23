# pypahe - Python Package Helper
#
# https://github.com/bonjoursoftware/pypahe
#
# Copyright (C) 2021 - 2023 Bonjour Software Limited
#
# https://bonjoursoftware.com/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see
# https://github.com/bonjoursoftware/pypahe/blob/master/LICENSE
#
from argparse import ArgumentParser
from configparser import ConfigParser
from dataclasses import dataclass
from functools import reduce
from re import sub
from requests import Response, get
from requests.exceptions import RequestException
from typing import Callable, Dict, List


from pypahe.exceptions import PypaheException

PACKAGE_SECTIONS = ["packages", "dev-packages", "tool.poetry.dependencies", "tool.poetry.dev-dependencies"]
PACKAGE_EXCLUSIONS = ["python"]


@dataclass
class Package:
    name: str
    section: str
    version: str

    def to_declaration_pattern(self) -> str:
        return f"\\S*{self.name}\\s*=\\s*\\S*"

    def to_latest(self) -> str:
        return f'{self.name} = "{self._version_constraint()}{find_latest_version(self.name)}"'

    def _version_constraint(self) -> str:
        return "" if "poetry" in self.section else "=="


def list_packages(package_config: str) -> List[Package]:
    parsed_config = ConfigParser()
    parsed_config.read_string(package_config)
    sections = [section[1] for section in parsed_config.items() if section[0] in PACKAGE_SECTIONS]
    packages = [Package(name=package[0], version=package[1], section=s.name) for s in sections for package in s.items()]
    return list(filter(lambda package: package.name not in PACKAGE_EXCLUSIONS, packages))


def upgrade_packages(config: str) -> str:
    return reduce(lambda c, p: sub(p.to_declaration_pattern(), p.to_latest(), c), list_packages(config), config)


def find_latest_version(package: str) -> str:
    return _get(
        url=f"https://pypi.org/pypi/{package}/json",
        read_response=_read_version,
        error_msg=f"unable to fetch latest version for '{package}'",
    )


def _get(url: str, read_response: Callable[[Response], str], error_msg: str) -> str:
    try:
        response = get(url=url)
        response.raise_for_status()
        return read_response(response)
    except RequestException as ex:
        raise PypaheException(f"{error_msg}: {ex}") from None


def _read_version(response: Response) -> str:
    return str(response.json()["info"]["version"])


@dataclass
class PypaheArgs:
    command: str
    package: str = ""
    package_config: str = ""


def parse_args() -> PypaheArgs:
    parser = ArgumentParser(
        description="PYthon PAckage HElper (aka pypahe)",
        epilog="https://github.com/bonjoursoftware/pypahe",
        prog="docker run bonjoursoftware/pypahe",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    latest_desc = "Find latest package version"
    latest_parser = subparsers.add_parser("latest", help=latest_desc, description=latest_desc)
    latest_parser.add_argument(dest="package", type=str, help="package name")

    upgrade_desc = "Upgrade package config"
    upgrade_parser = subparsers.add_parser("upgrade", help=upgrade_desc, description=upgrade_desc)
    upgrade_parser.add_argument(dest="package_config", type=str, help="Content of Pipfile or Poetry pyproject.toml")

    args = vars(parser.parse_args())

    return PypaheArgs(
        command=args["command"], package=args.get("package", ""), package_config=args.get("package_config", "")
    )


def main(args: PypaheArgs) -> str:
    command_mappings: Dict[str, Callable[[], str]] = {
        "latest": lambda: find_latest_version(args.package),
        "upgrade": lambda: upgrade_packages(args.package_config),
    }
    return command_mappings[args.command]()
