from __future__ import print_function
import os, sys
from os import path
from subprocess import Popen, PIPE, CalledProcessError
from textwrap import dedent
import pytest

class DataFileHelper(object):

    def __init__(self, base_dir):
        self._base_dir = base_dir

    def abspath(self, fn):
        return path.join(self._base_dir, fn)

    def relpath(self, fn):
        return path.relpath(self.abspath(fn)) # relative to CWD

    def read(self, fn, encoding=None):
        with open(self.abspath(fn), 'rb') as f:
            data = f.read()
            return data.decode(encoding) if encoding else data

    def json(self, fn, encoding='utf-8'):
        import json
        return json.loads(self.read(fn, encoding))

class CommandLine(object):

    def __init__(self, workdir):
        self.workdir = workdir

    def run(self, cmdline):
        _cwd = os.getcwd()
        assert path.isabs(_cwd), _cwd

        os.chdir(self.workdir)
        try:
            p = Popen(cmdline, stdout=PIPE, stderr=PIPE, shell=True)

            out, err = p.communicate()
            if p.returncode != 0:
                print(out, file=sys.stdout)
                print(err, file=sys.stderr)
                raise CalledProcessError(p.returncode, cmdline)

            return CommandLineResult(
                out.decode('utf-8'), err.decode('utf-8'), p.returncode)
        finally:
            os.chdir(_cwd)

    def src(self, pathname, content, encoding='utf-8'):
        if not path.isabs(pathname):
            pathname = path.join(self.workdir, pathname)
        with open(pathname, 'wb') as f:
            f.write(dedent(content).encode(encoding))

class CommandLineResult(object):

    def __init__(self, out, err, rc):
        self.out = out
        self.err = err
        self.rc = rc

@pytest.fixture
def testdata(request):
    base_dir = path.dirname(request.module.__file__)
    return DataFileHelper(base_dir)

@pytest.fixture
def cli(tmpdir):
    return CommandLine(tmpdir.strpath)

