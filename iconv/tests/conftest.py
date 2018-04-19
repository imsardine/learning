import os
from os import path
from subprocess import Popen, PIPE
import pytest

class DataFileHelper(object):

    def __init__(self, base_dir):
        self._base_dir = base_dir

    def abspath(self, fn):
        return path.join(self._base_dir, fn)

    def read(self, fn, encoding=None):
        with open(self.abspath(fn), 'rb') as f:
            data = f.read()
            return data.decode(encoding) if encoding else data

    def json(self, fn, encoding='utf-8'):
        import json
        return json.loads(self.read(fn, encoding))

class Shell(object):

    def __init__(self, base_dir):
        self._base_dir = base_dir

    def __call__(self, cmdline, cwd=None, encoding=None):
        _cwd = os.getcwd()
        assert path.isabs(_cwd), _cwd

        os.chdir(self._base_dir)
        if cwd:
            os.chdir(cwd) # absolute or relative to base dir

        try:
            p = Popen(cmdline, stdout=PIPE, stderr=PIPE, shell=True)

            out, err = p.communicate()
            if encoding:
                out, err = out.decode(encoding), err.decode(encoding)
            return (out, err, p.returncode)
        finally:
            os.chdir(_cwd)

@pytest.fixture
def testdata(request):
    base_dir = path.dirname(request.module.__file__)
    return DataFileHelper(base_dir)

@pytest.fixture
def shell(request):
    base_dir = path.dirname(request.module.__file__)
    return Shell(base_dir)

