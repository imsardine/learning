import os
from zipfile import ZipFile, is_zipfile
import pytest

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

@pytest.fixture
def zipfile():
    return os.path.join(FIXTURE_DIR, 'sample.zip')

@pytest.fixture
def txtfile():
    return os.path.join(FIXTURE_DIR, 'sample.txt.zip')

@pytest.fixture
def zipfile_broken():
    return os.path.join(FIXTURE_DIR, 'sample_broken.zip')

def test_validate_zipfile_valid(zipfile):
    assert is_zipfile(zipfile) # based on its magic number

def test_validate_zipfile_invalid(txtfile):
    assert not is_zipfile(txtfile)

def test_get_filelist_without_extraction(zipfile):
    names = ZipFile(zipfile).namelist()

    assert len(names) == 10
    assert 'dir2/file2-1.txt' in names

def test_read_file_without_extraction(zipfile):
    content = ZipFile(zipfile).read('dir1/file1-1.txt')
    assert content == 'file1-1\n'

def test_extract_all(zipfile, tmpdir):
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
    
def test_check_integrity(zipfile_broken):
    assert is_zipfile(zipfile_broken)

    bad_files = ZipFile(zipfile_broken).testzip() # doesn't work?
    assert bad_files != None

