"""General CLI Settings and Methods."""


import logging
from pathlib import Path
from typing import List

from rich.logging import RichHandler

from bumpver.scan import FileVersionInstances

CLICK_CONTEXT = {"help_option_names": ["-h", "--help"]}


def setup_logging(verbosity: int = 0, force: bool = False) -> None:
    """
    Set up a root logger with console output.

    Args:
        verbosity (int, optional): The logging level; 0=Error, 1=Warning,
            2=Info, 3+=Debug. Defaults to 0.

        force (bool, optiona): Force the logging level to this value, even
            if it's currently set to a more permissive value.",
    """
    logging_level = logging.ERROR
    if verbosity == 1:
        logging_level = logging.WARNING
    elif verbosity == 2:  # noqa: PLR2004
        logging_level = logging.INFO
    elif verbosity >= 3:  # noqa: PLR2004
        logging_level = logging.DEBUG

    if len(logging.root.handlers) == 0:
        logging.basicConfig(
            level=logging_level,
            format="%(message)s",
            datefmt="[%x]",
            handlers=[RichHandler(rich_tracebacks=True)],
        )
        logger = logging.getLogger(__name__)
        logger.info(f"Logging Setup at {logging.getLevelName(logging_level)} level")

    elif logging.root.level > logging_level or force:
        logging.root.setLevel(logging_level)

        logger = logging.getLogger(__name__)
        logger.info(f"Logging updated to {logging.getLevelName(logging_level)} level")

    else:
        logger = logging.getLogger(__name__)
        logger.debug(
            "Ignoring logging setup request: "
            "handler already exists at desired or greater level",
        )


def print_version_report(file_instances: List[FileVersionInstances]) -> None:
    """Print a report of the version instances provided."""
    file_instances.sort(key=lambda i: i.file_path)
    cwd = Path.cwd()

    pathlen = max(len(str(f.file_path.relative_to(cwd))) for f in file_instances)
    linelen = 3
    # charlen = 3

    for file in file_instances:
        file.instances.sort(key=lambda i: (i.line_no, i.char_no))

        for version in file.instances:
            print(
                f"{file.file_path.relative_to(cwd)!s:{pathlen}s} "
                f"line {version.line_no:{linelen}d}: "
                f"found version '{version.version!s}'",
            )
