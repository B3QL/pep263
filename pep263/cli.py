"""Command line interface."""
from contextlib import contextmanager

import click

from . import __version__
from .core import find_encoding
from .core import logger as core_logger
from .core import search_files


@click.option('--force', '-f', is_flag=True)
@click.argument('path', type=click.Path(exists=True), default='.')
@click.command()
@click.version_option(version=__version__)
def main(path, force):
    """Command entry point."""
    with disable_logger(core_logger):
        for filename in search_files(path):
            encoding = find_encoding(filename)
            click.echo('{0}: {1}'.format(filename, encoding.name))


@contextmanager
def disable_logger(logger):
    """Disable logger."""
    logger.disabled = True
    yield logger
    logger.disabled = False
