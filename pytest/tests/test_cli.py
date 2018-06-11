import pytest
from .matchers import *

def test_version(cli):
    r = cli.run('pytest --version')

    assert r.err == like("""
        This is pytest version %s, imported from ...
    """ % pytest.__version__)

