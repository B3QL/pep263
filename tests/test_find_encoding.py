import io
import pytest
from pep263.core import find_encoding, _find_file_encoding, EncodingInfo


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


def test_file_without_content_2():
    f = io.StringIO()
    with pytest.raises(LookupError) as excinfo:
        _find_file_encoding(f)
    assert str(excinfo.value) == 'encoding not found'


def test_file_with_utf8_coding():
    f = io.StringIO('# -*- coding: utf-8 -*-')
    encoding = _find_file_encoding(f)
    assert isinstance(encoding, EncodingInfo)
    assert encoding.name == 'utf-8'
    assert encoding.lineno == 1


def test_file_with_utf16_coding():
    f = io.StringIO('# -*- coding: utf-16 -*-')
    encoding = _find_file_encoding(f)
    assert isinstance(encoding, EncodingInfo)
    assert encoding.name == 'utf-16'
    assert encoding.lineno == 1


def test_file_with_utf8_coding_in_second_line():
    file_content = ['#!/usr/bin/env python',
                    '# -*- coding: utf-8 -*-']

    f = io.StringIO('\n'.join(file_content))
    encoding = _find_file_encoding(f)
    assert isinstance(encoding, EncodingInfo)
    assert encoding.name == 'utf-8'
    assert encoding.lineno == 2


def test_file_with_utf8_plain_text_coding():
    f = io.StringIO('# This Python file uses the following encoding: utf-8')
    encoding = _find_file_encoding(f)
    assert isinstance(encoding, EncodingInfo)
    assert encoding.name == 'utf-8'
    assert encoding.lineno == 1


def test_file_with_utf8_editor_coding():
    file_content = ['#!/usr/local/bin/python',
                    '# coding: latin-1']

    f = io.StringIO('\n'.join(file_content))
    encoding = _find_file_encoding(f)
    assert isinstance(encoding, EncodingInfo)
    assert encoding.name == 'latin-1'
    assert encoding.lineno == 2


def test_file_with_missing_coding_prefix():
    f = io.StringIO('# utf-8')
    with pytest.raises(LookupError) as excinfo:
        _find_file_encoding(f)
    assert str(excinfo.value) == 'encoding not found'


def test_file_with_utf8_coding_in_third_line():
    file_content = ['#!/usr/local/bin/python',
                    '#',
                    '# -*- coding: latin-1 -*-']

    f = io.StringIO('\n'.join(file_content))
    with pytest.raises(LookupError) as excinfo:
        _find_file_encoding(f)
    assert str(excinfo.value) == 'encoding not found'


def test_file_with_invalid_coding():
    f = io.StringIO('# -*- coding: utf-42 -*-')
    with pytest.raises(ValueError) as excinfo:
        _find_file_encoding(f)
    assert str(excinfo.value) == 'unknown encoding: utf-42'
