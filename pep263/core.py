import os
import re
import logging
from collections import namedtuple


logger = logging.getLogger(__name__)

# Official regex from https://www.python.org/dev/peps/pep-0263/
ENCODING_PATTERN = re.compile("^[ \t\v]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)")
EncodingInfo = namedtuple('EncodingInfo', ['name', 'lineno'])


def check_encoding(filename):
    try:
        encoding_info = None
        with open(filename, 'r') as f:
            encoding_info = _check_file_encoding(f)
    except PermissionError:
        logger.error('Cannot open file %s', filename)
    except FileNotFoundError:
        logger.error('File not found %s', filename)
    except LookupError as exc:
        msg = str(exc).capitalize()
        logger.warning('%s in %s', msg, filename)
    except ValueError as exc:
        msg = str(exc).capitalize()
        logger.warning('%s in %s', msg, filename)
    return encoding_info


def _check_file_encoding(f, lineno=1):
    if lineno > 2:
        raise LookupError('encoding not found')

    line = f.readline()
    line_match = re.search(ENCODING_PATTERN, line)
    if line_match:
        encoding_name = _validate_encoding(line_match.group(1))
        return EncodingInfo(name=encoding_name, lineno=lineno)
    else:
        return _check_file_encoding(f, lineno + 1)


def _validate_encoding(encoding_name):
    try:
        import codecs
        codecs.lookup(encoding_name)
    except LookupError as e:
        raise ValueError(e)
    return encoding_name


def search_files(path):
    files = []
    for entry in os.scandir(path):
        if _is_python_file(entry):
            files.append(entry)
        elif _is_directory(entry):
            subdir_files = search_files(entry.path)
            files.extend(subdir_files)
    return files


def _is_python_file(entry):
    return entry.is_file() and entry.name.endswith('.py')


def _is_directory(entry):
    return entry.is_dir()
