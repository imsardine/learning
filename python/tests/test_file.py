# -*- coding: utf-8 -*-
import os, sys
from os import path
import pytest

def test_getcwd_chdir():
    # https://docs.python.org/2/library/os.html#os.getcwd
    # https://docs.python.org/2/library/os.html#os.chdir
    module_dir = path.dirname(__file__)

    cwd = os.getcwd()
    try:
        os.chdir(module_dir)
        assert os.getcwd() == module_dir
    finally:
        os.chdir(cwd)

def test_type_testing_file(tmpdir):
    # https://docs.python.org/2.7/library/functions.html#file
    with open(path.join(tmpdir.strpath, 'file.ext'), 'w') as f:
        assert isinstance(f, file)

def test_stringio_is_not_file_but_filelike():
    from StringIO import StringIO
    io = StringIO()

    assert not isinstance(io, file)

    # https://docs.python.org/3/glossary.html#term-file-like-object
    assert hasattr(io, 'read')
    assert hasattr(io, 'write')

def test_directory_traversing__topdown(testdata):
    # tree
    # ├── ignore
    # │   └── file-ignore.ext
    # ├── subdir1
    # │   ├── file1-1.ext
    # │   ├── file1-2.ext
    # │   ├── subdir1-1
    # │   │   └── .keep
    # │   └── subdir1-2
    # │       └── .keep
    # └── subdir2
    #     └── file2-1.ext
    top = testdata.abspath('data/tree')
    dirs, files = [], [] # in order
    for dirpath, dirnames, filenames in os.walk(top):
        dirs.append(path.basename(dirpath))
        files.extend(sorted(filenames))

        # in-place modification
        dirnames.sort()
        if 'ignore' in dirnames:
            dirnames.remove('ignore')

    # depth-first traversing
    assert dirs == ['tree', 'subdir1', 'subdir1-1', 'subdir1-2', 'subdir2']
    assert files == ['file1-1.ext', 'file1-2.ext', '.keep', '.keep', 'file2-1.ext']

