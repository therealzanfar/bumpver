"""Code for scanning files for contained version strings."""

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, List, Optional

from semver import Version

from bumpver.config import Config

# The semver REGEX expects a version to be on it's own line (or a standalone
# string). Modify it so that it looks for a version anywhere in a string.
re_semver = Version._REGEX_TEMPLATE.strip()[1:-1].format(opt_patch="?", opt_minor="")
RE_SEMVER = re.compile(
    r"\b" + re_semver + r"\b",
    flags=re.VERBOSE | re.MULTILINE,
)


@dataclass
class VersionInstance:
    """Details about a specific occurance of a version string."""

    line_no: int
    char_no: int
    version_string: str
    version: Version


@dataclass
class FileVersionInstances:
    """Details about all the occurances of version strings in a file."""

    file_path: Path
    instances: List[VersionInstance] = field(default_factory=list)


def scan_file(file_path: Path) -> Optional[FileVersionInstances]:
    """Scan a file for version strings."""
    logger = logging.getLogger(__name__)

    logger.debug(f"Scanning file {file_path}")

    if not file_path.is_file():
        raise TypeError(f"File path ('{file_path}') is not a file.")

    instances: List[VersionInstance] = []

    with open(file_path, encoding="utf-8") as fh:
        for line_no, line in enumerate(fh):
            if "version" in line.lower():
                for match in RE_SEMVER.finditer(line.strip()):
                    instances.append(
                        VersionInstance(
                            line_no,
                            match.start(0),
                            match.group(0),
                            Version.parse(match.group(0), True),
                        ),
                    )

    if len(instances) > 0:
        return FileVersionInstances(
            file_path,
            instances,
        )

    return None


def scan_filetree(
    root_path: Path,
    config: Config,
) -> Iterator[FileVersionInstances]:
    """Scan a filetree for files containing version strings."""
    logger = logging.getLogger(__name__)

    logger.debug(f"Scanning directory {root_path}")

    if not root_path.is_dir():
        raise TypeError(
            f"Tree root path ('{root_path}') is not a directory.",
        )

    for child_path in root_path.iterdir():
        if config.ignore_path(child_path):
            logger.debug(f"Ignoring {child_path}")
            continue

        if child_path.is_dir():
            yield from scan_filetree(child_path, config=config)

        if child_path.is_file():
            instances = scan_file(child_path)
            if instances is not None:
                yield instances
