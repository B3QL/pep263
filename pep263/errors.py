"""Errors occurred while looking for file encoding."""
import enum


class EncodingError(enum.Enum):
    """Encoding error types."""

    OK = enum.auto()
    NOT_FOUND = enum.auto()
    PERMISSION_ERROR = enum.auto()
    INVALID_ENCODING = enum.auto()


ERRORS_COLOUR = {
    EncodingError.OK: 'green',
    EncodingError.NOT_FOUND: 'yellow',
    EncodingError.PERMISSION_ERROR: 'red',
    EncodingError.INVALID_ENCODING: 'red',
}


def error_colour(error):
    """Return error's colour."""
    return ERRORS_COLOUR[error]
