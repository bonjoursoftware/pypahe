# pypahe - Python Package Helper
#
# https://github.com/bonjoursoftware/pypahe
#
# Copyright (C) 2021 Bonjour Software Limited
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
from configparser import ConfigParser
from dataclasses import dataclass
from re import sub
from requests import Response, get
from requests.exceptions import RequestException
from typing import Callable, List

from pypahe.exceptions import PypaheException

PACKAGE_SECTIONS = ["packages", "dev-packages", "tool.poetry.dependencies", "tool.poetry.dev-dependencies"]
PACKAGE_EXCLUSIONS = ["python"]


@dataclass
class Package:
    name: str
    version: str


def list_packages(package_config: str) -> List[Package]:
    parsed_config = ConfigParser()
    parsed_config.read_string(package_config)
    sections = [section[1] for section in parsed_config.items() if section[0] in PACKAGE_SECTIONS]
    packages = [Package(name=package[0], version=package[1]) for section in sections for package in section.items()]
    return list(filter(lambda package: package.name not in PACKAGE_EXCLUSIONS, packages))


def upgrade_packages(package_config: str) -> str:
    for package in list_packages(package_config):
        package_config = sub(
            f"\\S*{package.name}\\s*=\\s*\\S*",
            f'{package.name} = "=={find_latest_version(package.name)}"',
            package_config,
        )
    return package_config


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
