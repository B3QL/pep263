"""Finding encoding in files tests."""
import pytest

from pep263.core import _find_file_encoding, find_encoding

from .conftest import create_file


def test_file_without_permission(caplog, tmpdir):
    test_dir = tmpdir.mkdir('test')
    test_file = test_dir.ensure('test.py')
    test_file.chmod(000)
    find_encoding(test_file.strpath)
    assert len(caplog.records) == 1
    assert 'Cannot open file' in caplog.text
    assert test_file.strpath in caplog.text


def test_file_not_found(caplog):
    filename = 'not_existing_file.py'
    find_encoding(filename)
    assert len(caplog.records) == 1
    assert 'File not found' in caplog.text
    assert filename in caplog.text


def test_file_without_content(caplog, tmpdir):
    test_dir = tmpdir.mkdir('test')
    test_file = test_dir.ensure('test.py')
    find_encoding(test_file.strpath)
    assert len(caplog.records) == 1
    assert 'Encoding not found' in caplog.text
    assert test_file.strpath in caplog.text


def test_file_with_invalid_coding_2(caplog, tmpdir):
    test_dir = tmpdir.mkdir('test')
    test_file = test_dir.join('test.py')
    test_file.write('# -*- coding: utf-42 -*-')
    find_encoding(test_file.strpath)
    assert len(caplog.records) == 1
    assert 'Unknown encoding' in caplog.text
    assert test_file.strpath in caplog.text


def test_file_without_content_2(empty_file):
    with pytest.raises(LookupError) as excinfo:
        _find_file_encoding(empty_file)
    assert str(excinfo.value) == 'encoding not found'


@create_file('# -*- coding: utf-8 -*-')
def test_file_with_utf8_coding(file):
    encoding = _find_file_encoding(file)
    assert encoding.name == 'utf-8'
    assert encoding.lineno == 1


@create_file('# -*- coding: utf-16 -*-')
def test_file_with_utf16_coding(file):
    encoding = _find_file_encoding(file)
    assert encoding.name == 'utf-16'
    assert encoding.lineno == 1


@create_file(
    '#!/usr/bin/env python',
    '# -*- coding: utf-8 -*-'
)
def test_file_with_utf8_coding_in_second_line(file):
    encoding = _find_file_encoding(file)
    assert encoding.name == 'utf-8'
    assert encoding.lineno == 2


@create_file('# This Python file uses the following encoding: utf-8')
def test_file_with_utf8_plain_text_coding(file):
    encoding = _find_file_encoding(file)
    assert encoding.name == 'utf-8'
    assert encoding.lineno == 1


@create_file(
    '#!/usr/local/bin/python',
    '# coding: latin-1'
)
def test_file_with_utf8_editor_coding(file):
    encoding = _find_file_encoding(file)
    assert encoding.name == 'latin-1'
    assert encoding.lineno == 2


@create_file('# utf-8')
def test_file_with_missing_coding_prefix(file):
    with pytest.raises(LookupError) as excinfo:
        _find_file_encoding(file)
    assert str(excinfo.value) == 'encoding not found'


@create_file(
    '#!/usr/local/bin/python',
    '#',
    '# -*- coding: latin-1 -*-'
)
def test_file_with_utf8_coding_in_third_line(file):
    with pytest.raises(LookupError) as excinfo:
        _find_file_encoding(file)
    assert str(excinfo.value) == 'encoding not found'


@create_file('# -*- coding: utf-42 -*-')
def test_file_with_invalid_coding(file):
    with pytest.raises(ValueError) as excinfo:
        _find_file_encoding(file)
    assert str(excinfo.value) == 'unknown encoding: utf-42'
