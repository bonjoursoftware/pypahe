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
from argparse import ArgumentParser, Namespace

from pypahe import package_info
from pypahe.exceptions import PypaheException


def parse_args() -> None:
    parser = ArgumentParser(description="Python Package Helper", epilog="https://github.com/bonjoursoftware/pypahe")
    parser.set_defaults(func=lambda _: print(parser.format_help()))

    subparsers = parser.add_subparsers()

    latest_desc = "Find latest package version"
    latest_parser = subparsers.add_parser("latest", help=latest_desc, description=latest_desc)
    latest_parser.add_argument(dest="package", type=str, help="package name")
    latest_parser.set_defaults(func=find_latest_version)

    args = parser.parse_args()
    args.func(args)


def find_latest_version(args: Namespace):
    try:
        print(package_info.find_latest_version(args.package))
    except PypaheException as ex:
        print(ex)


def main() -> None:
    parse_args()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
