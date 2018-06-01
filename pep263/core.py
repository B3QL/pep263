"""Core functionalities."""
import logging
import os
import re
from collections import namedtuple

from .decorators import seek_file

logger = logging.getLogger(__name__)

# Official regex from https://www.python.org/dev/peps/pep-0263/
ENCODING_PATTERN = re.compile("^[ \t\v]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)")
ENCODING_LINE = '# -*- coding: {encoding_name} -*-\n'
EncodingInfo = namedtuple('EncodingInfo', 'name lineno')


def find_encoding(filename):
    """Find information about encoding in file."""
    encoding_info = None
    try:
        with open(filename, 'r') as f:
            encoding_info = _find_file_encoding(f)
    except PermissionError:
        logger.error('Cannot open file %s', filename)
    except FileNotFoundError:
        logger.error('File not found %s', filename)
    except (LookupError, ValueError) as exc:
        msg = str(exc).capitalize()
        logger.warning('%s in %s', msg, filename)

    return encoding_info


def _find_file_encoding(f, lineno=1):
    if lineno > 2:
        raise LookupError('encoding not found')

    line = f.readline()
    line_match = re.search(ENCODING_PATTERN, line)
    if line_match:
        encoding_name = _validate_encoding(line_match.group(1))
        return EncodingInfo(name=encoding_name, lineno=lineno)
    return _find_file_encoding(f, lineno + 1)


def _validate_encoding(encoding_name):
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
        for entry in os.scandir(path):
            if _is_py_file(entry):
                files.append(entry)
            elif entry.is_dir():
                subdir_files = search_files(entry.path)
                files.extend(subdir_files)
    except PermissionError as exc:
        logger.error('Cannot open %s', exc.filename)
    except FileNotFoundError:
        logger.error('Directory not found %s', path)
    except NotADirectoryError:
        logger.error('Not a directory %s', path)
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
    encoding_name = _validate_encoding(encoding_name)
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
