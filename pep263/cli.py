"""Command line interface."""
import click

from . import __version__


@click.option('--force', '-f', is_flag=True)
@click.argument('path', type=click.Path(exists=True), default='.')
@click.command()
@click.version_option(version=__version__)
def main(path, force):
    """Command entry point."""
    pass
