import io
import pytest
from pep263.core import _append_file_encoding, append_encoding


def read_lines(f):
    lines = f.getvalue().split('\n')
    return [line + '\n' for line in lines if line]


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


def test_append_empty_file_utf8_encoding():
    f = io.StringIO()
    _append_file_encoding(f, 'utf-8')
    assert '# -*- coding: utf-8 -*-\n' == f.getvalue()


def test_append_empty_file_utf16_encoding():
    f = io.StringIO()
    _append_file_encoding(f, 'utf-16')
    assert '# -*- coding: utf-16 -*-\n' == f.getvalue()


def test_append_empty_file_invalid_encoding():
    f = io.StringIO()
    with pytest.raises(ValueError) as excinfo:
        _append_file_encoding(f, 'utf-42')
    assert str(excinfo.value) == 'unknown encoding: utf-42'


def test_append_shebanged_file_utf8_encoding():
    initial_content = '#!/usr/bin/env python\n'
    f = io.StringIO(initial_content)
    _append_file_encoding(f, 'utf-8')
    file_content = read_lines(f)
    assert len(file_content) == 2
    assert file_content[0] == initial_content
    assert file_content[1] == '# -*- coding: utf-8 -*-\n'


def test_append_commented_file_utf8_encoding():
    initial_content = '# this is a comment ;-)\n'
    f = io.StringIO(initial_content)
    _append_file_encoding(f, 'utf-8')
    file_content = read_lines(f)
    assert len(file_content) == 2
    assert file_content[0] == '# -*- coding: utf-8 -*-\n'
    assert file_content[1] == initial_content


def test_append_shebanged_and_commented_file_utf8_encoding():
    initial_content = ['#!/usr/bin/env python\n',
                       '# this is a comment ;-)\n']
    f = io.StringIO(''.join(initial_content))
    _append_file_encoding(f, 'utf-8')
    file_content = read_lines(f)
    assert len(file_content) == 3
    assert file_content[0] == initial_content[0]
    assert file_content[1] == '# -*- coding: utf-8 -*-\n'
    assert file_content[2] == initial_content[1]


def test_append_multicommented_file_utf8_encodign():
    initial_content = ['# this is a first comment\n',
                       '# this is a second comment\n']
    f = io.StringIO(''.join(initial_content))
    _append_file_encoding(f, 'utf-8')
    file_content = read_lines(f)
    assert len(file_content) == 3
    assert file_content[0] == '# -*- coding: utf-8 -*-\n'
    assert file_content[1] == initial_content[0]
    assert file_content[2] == initial_content[1]


def test_append_with_encoding_already_set_first_line():
    initial_content = ['# -*- coding: utf-8 -*-\n',
                       '# this is a second comment\n']
    f = io.StringIO(''.join(initial_content))
    with pytest.raises(RuntimeError) as excinfo:
        _append_file_encoding(f, 'utf-16')
    file_content = read_lines(f)
    assert str(excinfo.value) == 'encoding already exists'
    assert len(file_content) == 2
    assert file_content[0] == initial_content[0]
    assert file_content[1] == initial_content[1]


def test_force_append_with_encoding_already_set_first_line():
    initial_content = ['# -*- coding: utf-8 -*-\n',
                       '# this is a second comment\n']
    f = io.StringIO(''.join(initial_content))
    _append_file_encoding(f, 'utf-16', replace=True)
    file_content = read_lines(f)
    assert len(file_content) == 2
    assert file_content[0] == '# -*- coding: utf-16 -*-\n'
    assert file_content[1] == initial_content[1]
