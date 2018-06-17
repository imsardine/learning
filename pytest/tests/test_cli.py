import pytest
from .matchers import *

def test_version(shell):
    r = shell.run('pytest --version')

    assert r.err == like("""
        This is pytest version %s, imported from ...
    """ % pytest.__version__)

