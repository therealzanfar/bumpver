#! /usr/bin/env python3

"""Code for Direct Execution of bumpver Module."""

import logging
import sys

import click

from bumpver.cli import CLICK_CONTEXT, setup_logging


@click.command(context_settings=CLICK_CONTEXT)
@click.option("-v", "--verbose", count=True)
def cli_main(verbose: int = 0) -> int:
    """CLI Entry Point."""
    args = locals().items()
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    logger.debug("Running with options: %s", ", ".join(f"{k!s}={v!r}" for k, v in args))

    return 0


if __name__ == "__main__":
    sys.exit(cli_main())
