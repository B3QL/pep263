"""Pytest fixtures and test helpers."""
import io
from functools import partial
from itertools import zip_longest

import pytest


@pytest.fixture
def empty_file():
    """Return file-like object without content."""
    return io.StringIO()


def create_file(*lines):
    """Inject file-like object containing provided lines as first argument."""
    f = io.StringIO('\n'.join(lines) + '\n')

    def _decorator(func):
        return partial(func, f)
    return _decorator


def assert_lines(file, lines):
    """Compare file line by line."""
    file.seek(0)
    for l1, l2 in zip_longest(file, lines):
        assert l1 == l2 + '\n'
