import pytest

def test_py2_py3__separate_files(cli):
    cli.src('tox.ini', r"""
    [tox]
    envlist = py27,py36

    [testenv]
    deps = pytest

    [testenv:py27]
    commands = pytest --ignore tests/py3

    [testenv:py36]
    commands = pytest --ignore tests/py2
    """)

    cli.src('setup.py', r"""
    from setuptools import setup

    setup(
        name='hello-world',
    )
    """)

    # common tests
    cli.src('tests/test_hello.py', r"""
    from __future__ import print_function

    def test_hello():
        print('Hello, World!')
    """)

    # Python 2 syntax
    cli.src('tests/py2/test_hello_py2.py', r"""
    def test_hello():
        print 'Hello, World!'
    """)

    # Python 3 syntax
    cli.src('tests/py3/test_hello_py3.py', r"""
    def test_hello():
        print('Hello, World!')
    """)

    r = cli.run('tox')
    assert 'py27: commands succeeded' in r.out
    assert 'py36: commands succeeded' in r.out

def test_py2_py3__mixed(cli):
    cli.src('tox.ini', r"""
    [tox]
    envlist = py27,py36

    [testenv]
    deps = pytest
    commands = pytest
    """)

    cli.src('setup.py', r"""
    from setuptools import setup

    setup(
        name='hello-world',
    )
    """)

    # mixed in a file
    cli.src('tests/test_hello.py', r"""
    import sys, pytest

    py2 = pytest.mark.skipif(sys.version_info[0] != 2, reason="Only for Python 2")
    py3 = pytest.mark.skipif(sys.version_info[0] != 3, reason="Only for Python 3")

    def test_common():
        assert True

    @py2
    def test_py2():
        assert True

    @py3
    def test_py3():
        assert True
    """)

    r = cli.run('tox')
    assert 'py27: commands succeeded' in r.out
    assert 'py36: commands succeeded' in r.out