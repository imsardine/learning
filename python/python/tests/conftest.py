from os import path
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

@pytest.fixture
def datafile(request):
    base_dir = path.dirname(request.module.__file__)
    return DataFileHelper(base_dir)
