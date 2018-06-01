"""Append encoding to files tests."""
import pytest

from pep263.core import _append_file_encoding, append_encoding

from .conftest import assert_lines, create_file


def test_not_a_file(caplog, tmpdir):
    test_dir = tmpdir.mkdir('test')
    append_encoding(test_dir.strpath, 'utf-8')
    assert len(caplog.records) == 1
    assert 'Not a file' in caplog.text


def test_file_without_permission(caplog, tmpdir):
    test_dir = tmpdir.mkdir('test')
    test_file = test_dir.ensure('test.py')
    test_file.chmod(000)
    append_encoding(test_file.strpath, 'utf-8')
    assert len(caplog.records) == 1
    assert 'Cannot open a file' in caplog.text


def test_file_not_exist(caplog):
    append_encoding('no_existing_file.py', 'utf-8')
    assert len(caplog.records) == 1
    assert 'File not found' in caplog.text


def test_file_encoding_already_exist(caplog, tmpdir):
    test_dir = tmpdir.mkdir('test')
    test_file = test_dir.ensure('test.py')
    test_file.write('# -*- coding: utf-8 -*-\n')


def test_append_empty_file_utf8_encoding(empty_file):
    _append_file_encoding(empty_file, 'utf-8')
    assert empty_file.getvalue() == '# -*- coding: utf-8 -*-\n'


def test_append_empty_file_utf16_encoding(empty_file):
    _append_file_encoding(empty_file, 'utf-16')
    assert empty_file.getvalue() == '# -*- coding: utf-16 -*-\n'


def test_append_empty_file_invalid_encoding(empty_file):
    with pytest.raises(ValueError) as excinfo:
        _append_file_encoding(empty_file, 'utf-42')
    assert str(excinfo.value) == 'unknown encoding: utf-42'


@create_file('#!/usr/bin/env python')
def test_append_shebanged_file_utf8_encoding(file):
    _append_file_encoding(file, 'utf-8')
    expected_lines = [
        '#!/usr/bin/env python',
        '# -*- coding: utf-8 -*-'
    ]
    assert_lines(file, expected_lines)


@create_file('# this is a comment ;-)')
def test_append_commented_file_utf8_encoding(file):
    _append_file_encoding(file, 'utf-8')
    expected_lines = [
        '# -*- coding: utf-8 -*-',
        '# this is a comment ;-)'
    ]
    assert_lines(file, expected_lines)


@create_file(
    '#!/usr/bin/env python',
    '# this is a comment ;-)'
)
def test_append_shebanged_and_commented_file_utf8_encoding(file):
    _append_file_encoding(file, 'utf-8')
    expected_lines = [
        '#!/usr/bin/env python',
        '# -*- coding: utf-8 -*-',
        '# this is a comment ;-)'
    ]
    assert_lines(file, expected_lines)


@create_file(
    '# this is a first comment',
    '# this is a second comment'
)
def test_append_multicommented_file_utf8_encoding(file):
    _append_file_encoding(file, 'utf-8')
    expected_lines = [
        '# -*- coding: utf-8 -*-',
        '# this is a first comment',
        '# this is a second comment'
    ]
    assert_lines(file, expected_lines)


@create_file(
    '# -*- coding: utf-8 -*-',
    '# this is a second comment'
)
def test_append_with_encoding_already_set_first_line(file):
    with pytest.raises(RuntimeError) as excinfo:
        _append_file_encoding(file, 'utf-16')
    assert str(excinfo.value) == 'encoding already exists'
    expected_lines = [
        '# -*- coding: utf-8 -*-',
        '# this is a second comment'
    ]
    assert_lines(file, expected_lines)


@create_file(
    '# -*- coding: utf-8 -*-',
    '# this is a second comment'
)
def test_force_append_with_encoding_already_set_first_line(file):
    _append_file_encoding(file, 'utf-16', replace=True)
    expected_lines = [
        '# -*- coding: utf-16 -*-',
        '# this is a second comment'
    ]
    assert_lines(file, expected_lines)
