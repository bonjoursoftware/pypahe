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
from httpretty import GET, activate, register_uri
from json import dumps
from pytest import raises
from unittest import TestCase

from pypahe.package_info import find_latest_version
from pypahe.exceptions import PypaheException

from tests.resources.pipy_responses import GET_PACKAGE_INFO


class TestFindLatestVersion(TestCase):
    @activate
    def test_package_exists(self) -> None:
        register_uri(
            method=GET,
            uri="https://pypi.org/pypi/some_package/json",
            body=dumps(GET_PACKAGE_INFO),
            content_type="text/json",
        )
        assert "4.12.3" == find_latest_version("some_package")

    @activate
    def test_package_does_not_exist(self) -> None:
        register_uri(
            method=GET,
            uri="https://pypi.org/pypi/some_package/json",
            status=404,
        )
        with raises(PypaheException):
            find_latest_version("some_package")
