from os import path
import pytest

class DataFileHelper(object):

    def __init__(self, base_dir):
        self._base_dir = base_dir

    def read(self, fn):
        with open(path.join(self._base_dir, fn)) as f:
            return f.read()

    def json(self, fn):
        import json
        return json.loads(self.read(fn))

@pytest.fixture
def datafile(request):
    base_dir = path.join(path.dirname(request.module.__file__), 'data')
    return DataFileHelper(base_dir)

