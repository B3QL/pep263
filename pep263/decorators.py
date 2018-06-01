"""Decorators."""
import io
from functools import wraps


def seek_file(func):
    """Seek file passed as first argument."""
    @wraps(func)
    def _wrapper(*args, **kwargs):
        f = args[0]
        if isinstance(f, io.IOBase):
            f.seek(0)
        return func(*args, **kwargs)
    return _wrapper
