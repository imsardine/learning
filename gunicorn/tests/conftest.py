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

class Shell(object):

    def __init__(self, workdir):
        print('WORKDIR = %s' % workdir, file=sys.stderr)
        self.workdir = workdir

    def run(self, cmdline, err_expected=False):
        _cwd = os.getcwd()
        assert path.isabs(_cwd), _cwd

        os.chdir(self.workdir)
        try:
            p = Popen(cmdline, stdout=PIPE, stderr=PIPE, shell=True)

            out, err = p.communicate()
            if p.returncode != 0 and not err_expected:
                print(out, file=sys.stdout)
                print(err, file=sys.stderr)
                raise CalledProcessError(p.returncode, cmdline)
            elif p.returncode == 0 and err_expected:
                assert False, 'Error expected!'

            return ShellRunResult(
                out.decode('utf-8'), err.decode('utf-8'), p.returncode)
        finally:
            os.chdir(_cwd)

    def run_err(self, cmdline):
        return self.run(cmdline, err_expected=True)

    def spawn(self, cmdline):
        return PexpectSpawnContext(cmdline, self.workdir)

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

class ShellRunResult(object):

    def __init__(self, out, err, rc):
        self.out = out
        self.err = err
        self.rc = rc

class PexpectSpawnContext(object):

    def __init__(self, cmdline, workdir):
        self._cmdline = cmdline
        self._workdir = workdir
        self._child = None

    def __enter__(self):
        import pexpect

        os.chdir(self._workdir)
        self._child = pexpect.spawn( # unicode mode
            'bash', ['-c', self._cmdline], encoding='utf-8')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._child.terminate(force=True)

    def expect(self, pattern, timeout=3):
        pattern = self._to_pexpect_newline(self._to_unicode(pattern))
        return self._child.expect(pattern, timeout=timeout)

    def expect_exact(self, pattern, timeout=3):
        pattern = self._to_pexpect_newline(self._to_unicode(pattern))
        return self._child.expect_exact(pattern, timeout=timeout)

    def expect_eof(self, timeout=3):
        import pexpect
        return self._child.expect(pexpect.EOF, timeout=timeout)

    def expect_no_more_output(self, timeout=3):
        from pexpect import EOF, TIMEOUT

        try:
            self._child.expect(u'\\S', timeout=timeout)
            assert False, self.before + self.after
        except (EOF, TIMEOUT):
            assert True

    def send(self, s):
        s = self._to_unicode(s)
        return self._child.send(s)

    def sendline(self, s=''):
        s = self._to_unicode(s)
        return self._child.sendline(s)

    def _to_unicode(self, s):
        if sys.version_info[0] >= 3:
            if isinstance(s, bytes):
                return s.decode('utf-8')
            elif isinstance(s, str):
                return s
            else:
                assert False, s
        else:
            if isinstance(s, str):
                return s.decode('utf-8')
            elif isinstance(s, unicode):
                return s
            else:
                assert False, s

    @property
    def before(self):
        return self._to_unix_newline(self._child.before)

    @property
    def after(self):
        return self._to_unix_newline(self._child.after)

    def _to_unix_newline(self, input_):
        return input_.replace('\r\n', '\n')

    def _to_pexpect_newline(self, input_):
        return input_.replace('\n', '\r\n').replace(r'\n', r'\r\n')

    @property
    def match(self):
        return self._child.match

@pytest.fixture
def testdata(request):
    base_dir = path.dirname(request.module.__file__)
    return DataFileHelper(base_dir)

@pytest.fixture
def shell(tmpdir):
    return Shell(tmpdir.strpath)
