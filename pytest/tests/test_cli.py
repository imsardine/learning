import pytest

def test_version(cli):
    r = cli.run('pytest --version')

    assert r.err.startswith(
        'This is pytest version %s, imported from' % pytest.__version__)

