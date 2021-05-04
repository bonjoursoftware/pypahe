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
from httpretty import GET, activate, register_uri
from json import dumps
from pytest import raises
from unittest import TestCase

from pypahe.package_helper import Package, find_latest_version, list_packages, upgrade_packages
from pypahe.exceptions import PypaheException

from tests.resources.package_config import PIPFILE, PIPFILE_UPGRADE, POETRY_PYPROJECT, POETRY_PYPROJECT_UPGRADE


class TestListPackages(TestCase):
    def test_list_pipfile_packages(self) -> None:
        packages = [
            Package(name="requests", version='"*"', section="packages"),
            Package(name="records", version="'>0.5.0'", section="packages"),
            Package(name="flake8", version='"==3.8.2"', section="dev-packages"),
            Package(name="pytest", version='"==6.2.3"', section="dev-packages"),
        ]
        assert packages == list_packages(PIPFILE)

    def test_list_poetry_pyproject_packages(self) -> None:
        packages = [
            Package(name="pendulum", version='"^1.4"', section="tool.poetry.dependencies"),
            Package(name="pytest", version='"^3.4"', section="tool.poetry.dev-dependencies"),
            Package(name="mypy", version='"*"', section="tool.poetry.dev-dependencies"),
        ]
        assert packages == list_packages(POETRY_PYPROJECT)


@activate
class TestUpgradePackages(TestCase):
    def setUp(self) -> None:
        mock_package_version("flake8", "3.9.1")
        mock_package_version("mypy", "0.812")
        mock_package_version("pendulum", "2.1.2")
        mock_package_version("pytest", "6.2.3")
        mock_package_version("records", "0.5.3")
        mock_package_version("requests", "2.25.1")

    def test_upgrade_pipfile_packages(self) -> None:
        assert PIPFILE_UPGRADE == upgrade_packages(PIPFILE)

    def test_upgrade_poetry_pyproject_packages(self) -> None:
        assert POETRY_PYPROJECT_UPGRADE == upgrade_packages(POETRY_PYPROJECT)


class TestFindLatestVersion(TestCase):
    @activate
    def test_package_exists(self) -> None:
        mock_package_version("some_package", "4.12.3")
        assert "4.12.3" == find_latest_version("some_package")

    @activate
    def test_package_does_not_exist(self) -> None:
        register_uri(method=GET, uri="https://pypi.org/pypi/some_package/json", status=404)
        with raises(PypaheException):
            find_latest_version("some_package")


def mock_package_version(package: str, version: str) -> None:
    register_uri(
        method=GET,
        uri=f"https://pypi.org/pypi/{package}/json",
        body=dumps({"info": {"name": package, "version": version}}),
        content_type="text/json",
    )
