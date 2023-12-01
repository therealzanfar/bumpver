#! /usr/bin/env python3

"""Code for Direct Execution of bumpver Module."""

import logging
import sys

import click

from bumpver.cli import CLICK_CONTEXT, print_version_report, setup_logging
from bumpver.config import Config
from bumpver.scan import scan_filetree


@click.command(context_settings=CLICK_CONTEXT)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    flag_value=True,
    default=False,
    type=bool,
    help="Run with minimal output and no input.",
)
@click.option("--verbose", "-v", count=True, help="Increase the logging verbosity.")
def cli_main(
    quiet: bool = False,
    verbose: int = 0,
) -> int:
    """CLI Entry Point."""
    args = locals().items()
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    logger.debug("Running with options: %s", ", ".join(f"{k!s}={v!r}" for k, v in args))

    # Load config
    config = Config()

    # Scan files for current versions
    instances = list(scan_filetree(config.cwd, config=config))
    if not quiet:
        print_version_report(instances)

    # Check that current versions match, bail out if not forced

    # Set the current version to the latest found

    # Calculate the bumped version
    # Prompt for changes, if not quiet
    # Modify files

    # Make Git commit, if requested
    # Make Git tag, if requested

    return 0


if __name__ == "__main__":
    sys.exit(cli_main())
