import os
from os import path
from zipfile import ZipFile, is_zipfile, ZIP_DEFLATED
import pytest

def test_validate_zipfile__valid(datafile):
    assert is_zipfile(datafile.abspath('data/zip/sample.zip')) # based on its magic number

def test_validate_zipfile__invalid(datafile):
    assert not is_zipfile(datafile.abspath('data/zip/sample.txt.zip'))

def test_get_filelist_without_extraction(datafile):
    zipfile = datafile.abspath('data/zip/sample.zip')
    names = ZipFile(zipfile).namelist()

    assert len(names) == 10
    assert 'dir2/file2-1.txt' in names

def test_read_file_without_extraction(datafile):
    zipfile = datafile.abspath('data/zip/sample.zip')
    content = ZipFile(zipfile).read('dir1/file1-1.txt')
    assert content == 'file1-1\ncontent\ncontent\ncontent\n'

def test_extract_all(datafile, tmpdir):
    zipfile = datafile.abspath('data/zip/sample.zip')
    ZipFile(zipfile).extractall(tmpdir.strpath)

    assert [f.relto(tmpdir) for f in tmpdir.listdir(sort=True)] == \
            ['dir1', 'dir2', 'file1.txt', 'file2.txt']

    dir1 = tmpdir.join('dir1')
    assert [f.relto(dir1) for f in dir1.listdir(sort=True)] == \
            ['dir1-1', 'dir1-2', 'file1-1.txt', 'file1-2.txt']

    assert [f.relto(dir1) for f in dir1.join('dir1-1').listdir(sort=True)] == []
    assert [f.relto(dir1) for f in dir1.join('dir1-2').listdir(sort=True)] == []

    dir2 = tmpdir.join('dir2')
    assert [f.relto(dir2) for f in dir2.listdir(sort=True)] == \
            ['file2-1.txt', 'file2-2.txt']

@pytest.mark.xfail
def test_check_integrity(datafile):
    zipfile_broken = datafile.abspath('data/zip/sample_broken.zip')
    assert is_zipfile(zipfile_broken)

    bad_files = ZipFile(zipfile_broken).testzip() # doesn't work?
    assert bad_files != None

def test_archive__deflate_compression(datafile, tmpdir):
    content_dir = datafile.relpath('data/zip/content')

    # Not to change current working directory
    zfn = tmpdir.join('archive.zip').strpath
    with ZipFile(zfn, 'w', compression=ZIP_DEFLATED) as zf:
        for dirpath, dirnames, filenames in os.walk(content_dir):
            for fn in filenames:
                fn_full = path.join(dirpath, fn)
                arcname = path.relpath(fn_full, content_dir)
                zf.write(fn_full, arcname)

    with ZipFile(zfn) as zf:
        assert sorted(zf.namelist()) == [ # no dirs?
            'dir1/file1-1.txt',
            'dir1/file1-2.txt',
            'dir2/file2-1.txt',
            'dir2/file2-2.txt',
            'file1.txt',
            'file2.txt',
        ]

        info = zf.getinfo('dir1/file1-1.txt')
        assert info.compress_type == ZIP_DEFLATED
        assert info.file_size > info.compress_size

        assert zf.read(info.filename) == 'file1-1\ncontent\ncontent\ncontent\n'

