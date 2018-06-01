"""Core functionalities."""
import logging
import re
from collections import namedtuple

from .decorators import seek_file
from .errors import EncodingError

try:
    from os import scandir
except ImportError:
    from scandir import scandir


logger = logging.getLogger(__name__)

# Official regex from https://www.python.org/dev/peps/pep-0263/
ENCODING_PATTERN = re.compile("^[ \t\v]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)")
ENCODING_LINE = '# -*- coding: {encoding_name} -*-\n'
EncodingInfo = namedtuple('EncodingInfo', 'name lineno error')


def find_encoding(filename):
    """Find information about encoding in file."""
    try:
        with open(filename, 'r') as f:
            encoding_info = _find_file_encoding(f)
            return encoding_info
    except PermissionError:
        logger.error('Cannot open file %s', filename)
        return EncodingInfo('permission denied', -1, EncodingError.PERMISSION_ERROR)
    except FileNotFoundError:
        logger.error('File not found %s', filename)
        return EncodingInfo('no encoding', -1, EncodingError.NOT_FOUND)
    except LookupError as exc:
        msg = str(exc).capitalize()
        logger.warning('%s in %s', msg, filename)
        return EncodingInfo('no encoding', -1, EncodingError.NOT_FOUND)
    except ValueError as exc:
        msg = str(exc).capitalize()
        logger.warning('%s in %s', msg, filename)
        return EncodingInfo('invalid encoding', -1, EncodingError.INVALID_ENCODING)


def _find_file_encoding(f, lineno=1):
    if lineno > 2:
        raise LookupError('encoding not found')

    line = f.readline()
    line_match = re.search(ENCODING_PATTERN, line)
    if line_match:
        encoding_name = validate_encoding(line_match.group(1))
        return EncodingInfo(name=encoding_name, lineno=lineno, error=EncodingError.OK)
    return _find_file_encoding(f, lineno + 1)


def validate_encoding(encoding_name):
    """Validate encoding name."""
    try:
        import codecs
        codecs.lookup(encoding_name)
    except LookupError as e:
        raise ValueError(e)
    return encoding_name


def search_files(path):
    """Find recursively python files in path."""
    files = []
    try:
        for entry in scandir(path):
            if _is_py_file(entry):
                files.append(entry.path)
            elif entry.is_dir():
                subdir_files = search_files(entry.path)
                files.extend(subdir_files)
    except PermissionError as exc:
        logger.error('Cannot open %s', exc.filename)
    except FileNotFoundError:
        logger.error('Directory not found %s', path)
    except NotADirectoryError:
        files.append(path)
    return files


def _is_py_file(entry):
    return entry.is_file() and entry.name.endswith('.py')


def append_encoding(filename, encoding_name, force=False):
    """Append encoding to file."""
    try:
        with open(filename, 'r+') as f:
            _append_file_encoding(f, encoding_name, force)
    except PermissionError:
        logger.error('Cannot open a file %s', filename)
    except FileNotFoundError:
        logger.error('File not found %s', filename)
    except IsADirectoryError:
        logger.error('Not a file %s', filename)


def _append_file_encoding(f, encoding_name, replace=False):
    encoding_name = validate_encoding(encoding_name)
    encoding_line = ENCODING_LINE.format(**locals())
    try:
        encoding_info = _find_file_encoding(f)
    except LookupError:
        lineno = _find_lineno(f)
    else:
        if replace:
            lineno = encoding_info.lineno
        else:
            raise RuntimeError('encoding already exists')

    _write_line(f, lineno, encoding_line, replace)


@seek_file
def _find_lineno(f):
    first_line = f.readline()
    shebang = first_line.startswith('#!')
    return 2 if shebang else 1


@seek_file
def _write_line(f, lineno, content, replace):
    file_content = f.readlines()
    line_index = lineno - 1

    if replace:
        file_content[line_index] = content
    else:
        file_content.insert(line_index, content)

    f.seek(0)
    f.writelines(file_content)
