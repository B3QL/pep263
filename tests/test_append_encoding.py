import io
from pep263.core import append_encoding


def read_lines(f):
    lines = f.getvalue().split('\n')
    return [line + '\n' for line in lines if line]
            

def test_append_empty_file_utf8_encoding():
    f = io.StringIO()
    append_encoding(f, 'utf-8')
    assert '# -*- coding: utf-8 -*-\n' == f.getvalue()


def test_append_empty_file_utf16_encoding():
    f = io.StringIO()
    append_encoding(f, 'utf-16')
    assert '# -*- coding: utf-16 -*-\n' == f.getvalue()


def test_append_shebanged_file_utf8_encoding():
    initial_content = '#!/usr/bin/env python\n'
    f = io.StringIO(initial_content)
    append_encoding(f, 'utf-8')
    file_content = read_lines(f) 
    assert len(file_content) == 2
    assert file_content[0]  == initial_content
    assert file_content[1] == '# -*- coding: utf-8 -*-\n'


def test_append_commented_file_utf8_encoding():
    initial_content = '# this is a comment ;-)\n'
    f = io.StringIO(initial_content)
    append_encoding(f, 'utf-8')
    file_content = read_lines(f) 
    assert len(file_content) == 2
    assert file_content[0] == '# -*- coding: utf-8 -*-\n'
    assert file_content[1] == initial_content
