import re
from collections import namedtuple

# Official regex from https://www.python.org/dev/peps/pep-0263/
ENCODING_PATTERN = re.compile("^[ \t\v]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)")
Encoding = namedtuple('Encoding', ['name', 'lineno'])


def check_file(f):
    def _check_file_helper(f, lineno):
        if lineno > 2:
            raise LookupError('encoding not found')

        line = f.readline()
        line_match = re.search(ENCODING_PATTERN, line)
        if line_match:
            encoding_name = _validate_encoding(line_match.group(1))
            return Encoding(name=encoding_name, lineno=lineno)
        else:
            return _check_file_helper(f, lineno + 1)
    return _check_file_helper(f, 1)


def _validate_encoding(encoding_name):
    try:
        import codecs
        codecs.lookup(encoding_name)
    except LookupError as e:
        raise ValueError(e)
    return encoding_name
