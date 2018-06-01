"""Errors occurred while looking for file encoding."""
import enum


class EncodingError(enum.IntEnum):
    """Encoding error types."""

    OK = 0
    NOT_FOUND = 1
    PERMISSION_ERROR = 2
    INVALID_ENCODING = 3


ERRORS_COLOUR = {
    EncodingError.OK: 'green',
    EncodingError.NOT_FOUND: 'yellow',
    EncodingError.PERMISSION_ERROR: 'red',
    EncodingError.INVALID_ENCODING: 'red',
}


def error_colour(error):
    """Return error's colour."""
    return ERRORS_COLOUR[error]
