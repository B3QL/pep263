from pep263 import search_files


def test_no_python_files(tmpdir):
    test_dir = tmpdir.mkdir('test')
    assert len(search_files(test_dir.strpath)) == 0


def test_one_python_file_in_root_dir(tmpdir):
    test_dir = tmpdir.mkdir('test')
    test_file = test_dir.ensure('test.py')
    result = search_files(test_dir.strpath)
    assert len(result) == 1
    assert result[0].name == 'test.py'
    assert result[0].path == test_file.strpath


def test_one_python_file_and_one_text_file_in_root_dir(tmpdir):
    test_dir = tmpdir.mkdir('test')
    test_file = test_dir.ensure('test.py')
    test_dir.ensure('test.txt')
    result = search_files(test_dir.strpath)
    assert len(result) == 1
    assert result[0].name == 'test.py'
    assert result[0].path == test_file.strpath


def test_python_files_different_deep_level(tmpdir):
    test_dir = tmpdir.mkdir('test')
    test_subdir = test_dir.mkdir('subdir')
    test_dir.ensure('test.py')
    test_subdir.ensure('test_subdir.py')
    result = search_files(test_dir.strpath)
    assert len(result) == 2
    assert result[0].name == 'test.py'
    assert result[1].name == 'test_subdir.py'
