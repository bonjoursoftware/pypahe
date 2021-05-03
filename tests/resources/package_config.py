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
PIPFILE = """[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = "*"
records = '>0.5.0'

[dev-packages]
flake8 = "==3.8.2"
pytest = "==6.2.3"

[requires]
python_version = "3.9.4"
"""

PIPFILE_UPGRADE = """[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = "==2.25.1"
records = "==0.5.3"

[dev-packages]
flake8 = "==3.9.1"
pytest = "==6.2.3"

[requires]
python_version = "3.9.4"
"""

POETRY_PYPROJECT = """[tool.poetry]
name = "sample-package-config"
version = "0.8.2"
description = "Some sample package config"
authors = ["Bonjour Software Limited"]

[tool.poetry.dependencies]
python = "*"
pendulum = "^1.4"

[tool.poetry.dev-dependencies]
pytest = "^3.4"
mypy = "*"
"""

POETRY_PYPROJECT_UPGRADE = """[tool.poetry]
name = "sample-package-config"
version = "0.8.2"
description = "Some sample package config"
authors = ["Bonjour Software Limited"]

[tool.poetry.dependencies]
python = "*"
pendulum = "^1.4"

[tool.poetry.dev-dependencies]
pytest = "^3.4"
mypy = "*"
"""
