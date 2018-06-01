"""Searching for python files tests."""
from pep263 import search_files


def test_no_python_files(tmpdir):
    test_dir = tmpdir.mkdir('test')
    assert search_files(test_dir.strpath) == []


def test_one_python_file_in_root_dir(tmpdir):
    test_dir = tmpdir.mkdir('test')
    test_file = test_dir.ensure('test.py')
    result, = search_files(test_dir.strpath)
    assert result.name == 'test.py'
    assert result.path == test_file.strpath


def test_one_python_file_and_one_text_file_in_root_dir(tmpdir):
    test_dir = tmpdir.mkdir('test')
    test_file = test_dir.ensure('test.py')
    test_dir.ensure('test.txt')
    result, = search_files(test_dir.strpath)
    assert result.name == 'test.py'
    assert result.path == test_file.strpath


def test_python_files_different_deep_level(tmpdir):
    test_dir = tmpdir.mkdir('test')
    test_subdir = test_dir.mkdir('subdir')
    test_file = test_dir.ensure('test.py')
    test_file_subdir = test_subdir.ensure('test_subdir.py')
    result = search_files(test_dir.strpath)

    filenames = [e.name for e in result]
    assert sorted(filenames) == sorted(['test.py', 'test_subdir.py'])

    paths = [e.path for e in result]
    assert sorted(paths) == sorted([test_file.strpath, test_file_subdir.strpath])


def test_subdirectory_without_permission(caplog, tmpdir):
    test_dir = tmpdir.mkdir('test')
    test_subdir = test_dir.mkdir('subdir')
    test_dir.ensure('test.py')
    test_subdir.ensure('test_subdir.py')
    test_subdir.chmod(000)
    result, = search_files(test_dir.strpath)
    assert result.name == 'test.py'
    assert 'Cannot open' in caplog.text


def test_multiple_subdirectory_one_without_permission(caplog, tmpdir):
    test_dir = tmpdir.mkdir('test')
    test_subdir_1 = test_dir.mkdir('subdir_1')
    test_subdir_1.ensure('test_subdir_1.py')
    test_subdir_1.chmod(000)
    test_subdir_2 = test_dir.mkdir('subdir_2')
    test_subdir_2.ensure('test_subdir_2.py')
    test_subdir_3 = test_dir.mkdir('subdir_3')
    test_subdir_3.ensure('test_subdir_3.py')
    result = search_files(test_dir.strpath)

    filenames = [e.name for e in result]
    assert filenames == ['test_subdir_2.py', 'test_subdir_3.py']
    assert 'Cannot open' in caplog.text


def test_not_existing_path(caplog):
    search_files('non_existing/path/at_all')
    assert len(caplog.records) == 1
    assert 'Directory not found' in caplog.text


def test_not_a_directory(caplog, tmpdir):
    test_dir = tmpdir.mkdir('test')
    test_file = test_dir.ensure('test.py')
    search_files(test_file.strpath)
    assert len(caplog.records) == 1
    assert 'Not a directory ' in caplog.text
