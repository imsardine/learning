from __future__ import print_function
import os, sys
from os import path
from subprocess import Popen, PIPE, CalledProcessError
from textwrap import dedent
import re
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

INDENTED_LITERAL = re.compile(r'^\n?(?P<content>.*)\n?\s*$', re.DOTALL)

class CommandLine(object):

    def __init__(self, workdir):
        print('WORKDIR = %s' % workdir, file=sys.stderr)
        self.workdir = workdir

    def run(self, cmdline, err_expected=False):
        os.chdir(self.workdir)
        p = Popen(cmdline, stdout=PIPE, stderr=PIPE, shell=True)
        return ProcessContext(p, err_expected)

    def run_err(self, cmdline):
        return self.run(cmdline, err_expected=True)

    def src(self, pathname, content='', encoding='utf-8'):
        pathname = self._abspath(pathname)

        dirname = path.dirname(pathname)
        if not path.exists(dirname):
            os.makedirs(dirname)

        with open(pathname, 'wb') as f:
            f.write(self._trim(content).encode(encoding))

    def exists(self, pathname):
        dir_expected = pathname.endswith('/')

        pathname = self._abspath(pathname)
        if not path.exists(pathname):
            return False

        return dir_expected == path.isdir(pathname)

    def _abspath(self, pathname):
        if not path.isabs(pathname):
            pathname = path.join(self.workdir, pathname)
        return pathname

    def _trim(self, content):
        match = INDENTED_LITERAL.match(content)
        assert match, content

        return dedent(match.group('content'))

class ProcessContext(object):

    def __init__(self, popen, err_expected):
        self._popen = popen
        self._err_expected = err_expected

        self._returned = False
        self._out = self._err = ''
        self._rc = 0

    @property
    def rc(self):
        self._wait_to_terminate()
        return self._rc

    @property
    def out(self):
        self._wait_to_terminate()
        return self._out

    @property
    def err(self):
        self._wait_to_terminate()
        return self._err

    def _wait_to_terminate(self):
        if self._returned:
            return

        p = self._popen

        out, err = p.communicate()
        self._out = out.decode('utf-8')
        self._err = err.decode('utf-8')
        self._rc = p.returncode
        self._returned = True

        if p.returncode != 0 and not self._err_expected:
            print(self._out, file=sys.stdout)
            print(self._err, file=sys.stderr)
            raise CalledProcessError(p.returncode, cmdline)
        elif p.returncode == 0 and self._err_expected:
            assert False, 'Error expected!'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._popen.terminate()

@pytest.fixture
def testdata(request):
    base_dir = path.dirname(request.module.__file__)
    return DataFileHelper(base_dir)

@pytest.fixture
def cli(tmpdir):
    return CommandLine(tmpdir.strpath)

