#! /usr/bin/env python3

"""Code for Direct Execution of bumpver Module."""

import logging
import sys

import click

from bumpver.cli import CLICK_CONTEXT, print_version_report, setup_logging
from bumpver.config import Config
from bumpver.scan import scan_filetree, versions_match


@click.command(context_settings=CLICK_CONTEXT)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    flag_value=True,
    default=False,
    type=bool,
    help="Force the update even if versions do not match, or the new version is older.",
)
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
    force: bool = False,
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
    versioned_files = list(scan_filetree(config.cwd, config=config))
    if len(versioned_files) <= 0:
        if not quiet:
            print("No versioned files found.")
        return 0

    if not quiet:
        print_version_report(versioned_files)

    # Check that current versions match, bail out if not forced
    if not versions_match(versioned_files) and not force:
        if not quiet:
            print("Versions do not match; aborting.")
        return 1

    # Calculate the bumped version
    # Prompt for changes, if not quiet
    # Modify files

    # Make Git commit, if requested
    # Make Git tag, if requested

    return 0


if __name__ == "__main__":
    sys.exit(cli_main())
