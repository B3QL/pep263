import io
from functools import wraps


def seek_file(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        f = args[0]
        if isinstance(f, io.IOBase):
            f.seek(0)
        return func(*args, **kwargs)
    return wrapper
