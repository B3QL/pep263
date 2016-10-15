import io
import pytest
from pep263 import check_file, Encoding


def test_file_with_no_content():
    f = io.StringIO()
    with pytest.raises(LookupError) as excinfo:
        check_file(f)
    assert str(excinfo.value) == 'encoding not found'


def test_file_with_utf8_coding():
    f = io.StringIO('# -*- coding: utf-8 -*-')
    encoding = check_file(f)
    assert isinstance(encoding, Encoding)
    assert encoding.name == 'utf-8'
    assert encoding.lineno == 1


def test_file_with_utf16_coding():
    f = io.StringIO('# -*- coding: utf-16 -*-')
    encoding = check_file(f)
    assert isinstance(encoding, Encoding)
    assert encoding.name == 'utf-16'
    assert encoding.lineno == 1


def test_file_with_utf8_coding_in_second_line():
    file_content = ['#!/usr/bin/env python',
                    '# -*- coding: utf-8 -*-']

    f = io.StringIO('\n'.join(file_content))
    encoding = check_file(f)
    assert isinstance(encoding, Encoding)
    assert encoding.name == 'utf-8'
    assert encoding.lineno == 2


def test_file_with_utf8_plain_text_coding():
    f = io.StringIO('# This Python file uses the following encoding: utf-8')
    encoding = check_file(f)
    assert isinstance(encoding, Encoding)
    assert encoding.name == 'utf-8'
    assert encoding.lineno == 1


def test_file_with_utf8_editor_coding():
    file_content = ['#!/usr/local/bin/python',
                    '# coding: latin-1']

    f = io.StringIO('\n'.join(file_content))
    encoding = check_file(f)
    assert isinstance(encoding, Encoding)
    assert encoding.name == 'latin-1'
    assert encoding.lineno == 2


def test_file_with_missing_coding_prefix():
    f = io.StringIO('# utf-8')
    with pytest.raises(LookupError) as excinfo:
        check_file(f)
    assert str(excinfo.value) == 'encoding not found'


def test_file_with_utf8_coding_in_third_line():
    file_content = ['#!/usr/local/bin/python',
                    '#',
                    '# -*- coding: latin-1 -*-']

    f = io.StringIO('\n'.join(file_content))
    with pytest.raises(LookupError) as excinfo:
        check_file(f)
    assert str(excinfo.value) == 'encoding not found'


def test_file_with_invalid_coding():
    f = io.StringIO('# -*- coding: utf-42 -*-')
    with pytest.raises(ValueError) as excinfo:
        check_file(f)
    assert str(excinfo.value) == 'unknown encoding: utf-42'
