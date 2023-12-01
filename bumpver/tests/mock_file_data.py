"""Mock data for scan tests."""


from dataclasses import dataclass
from typing import List

from semver import Version

from bumpver.scan import VersionInstance


@dataclass
class FileDetails:
    """Mock File Details."""

    instances: List[VersionInstance]
    filename: str
    content: str


MOCK_FILES = {
    "pyproject": FileDetails(
        [
            VersionInstance(
                2,
                11,
                "0.1.0",
                Version(0, 1, 0),
            ),
        ],
        "pyproject.toml",
        """[tool.poetry]
name = "some_project"
version = "0.1.0"
description = "Example pyproject.toml File"
authors = ["John Doe <john.doe@not-a-domain.com>"]
license = "GPL-3.0-or-later"
readme = "README.md"

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.8",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities"
]


[tool.poetry.dependencies]
python = "^3.8"

[tool.poetry.dev-dependencies]
black = "^23.11.0"
mypy = "^1.7.0"
pytest = "^7.4.3"
ruff = "^0.1.6"
""",
    ),
    "init": FileDetails(
        [
            VersionInstance(
                5,
                15,
                "1.0.0",
                Version(1, 0, 0),
            ),
        ],
        "__init__.py",
        """__author__ = "John Doe"
__email__ = "john.doe@not-a-domain.com"
__copyright__ = "Copyright 1970, John Doe"
__credits__ = [__author__]
__license__ = "GPL-3.0-or-later"
__version__ = "1.0.0"
__maintainer__ = __author__
__status__ = "Production""",
    ),
}
