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
from requests import Response, get
from requests.exceptions import RequestException
from typing import Callable

from pypahe.exceptions import PypaheException


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
