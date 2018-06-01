"""Command line interface."""
from contextlib import contextmanager

import click

from . import __version__
from .core import append_encoding, find_encoding
from .core import logger as core_logger
from .core import search_files, validate_encoding
from .errors import error_colour


def validate_encoding_name(ctx, param, value):
    """Validate encoding name option."""
    try:
        return validate_encoding(value)
    except ValueError:
        raise click.BadParameter('unknown encoding')
    except TypeError:
        return None


@click.option('--force', '-f', is_flag=True, help='Overwrite all files encoding')
@click.option('--append', '-A', callback=validate_encoding_name, help='Append encoding to files')
@click.argument('path', type=click.Path(exists=True), default='.')
@click.command()
@click.version_option(version=__version__)
def main(path, append, force):
    """Manage source files encodings."""
    with disable_logger(core_logger):
        for filename in search_files(path):
            if append:
                try:
                    append_encoding(filename, encoding_name=append, force=force)
                except RuntimeError:
                    pass
            encoding = find_encoding(filename)
            click.secho('{0}: {1}'.format(filename, encoding.name), fg=error_colour(encoding.error))


@contextmanager
def disable_logger(logger):
    """Disable logger."""
    logger.disabled = True
    yield logger
    logger.disabled = False
