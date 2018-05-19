import os
from os import path
from subprocess import Popen, PIPE
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

    def __init__(self, base_dir):
        self._base_dir = base_dir

    def run(self, cmdline, cwd=None):
        _cwd = os.getcwd()
        assert path.isabs(_cwd), _cwd

        os.chdir(self._base_dir)
        if cwd:
            os.chdir(cwd) # absolute or relative to base dir

        try:
            p = Popen(cmdline, stdout=PIPE, stderr=PIPE, shell=True)

            out, err = p.communicate()
            return CommandLineResult(
                out.decode('utf-8'), err.decode('utf-8'), p.returncode)
        finally:
            os.chdir(_cwd)

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
def cli(request):
    base_dir = path.dirname(request.module.__file__)
    return CommandLine(base_dir)

import boto3

@pytest.fixture
def s3_bucket():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(os.environ['S3_BUCKET'])

    _empty_s3_bucket(bucket) # setup
    yield bucket
    _empty_s3_bucket(bucket) # teardown

def _empty_s3_bucket(bucket):
    for key in bucket.objects.all():
        key.delete()

