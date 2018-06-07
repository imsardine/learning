def test_hello_world(cli):
    cli.src('tox.ini', r"""
    [tox]
    envlist = py27,py36

    [testenv]
    deps = pytest
    commands = pytest
    """)

    # setup.py in the same directory
    cli.src('setup.py', r"""
    from setuptools import setup
    setup(
        name='hello-world',
        packages=['hello'],
    )
    """)

    # production code
    cli.src('hello/__init__.py')
    cli.src('hello/hello.py', r"""
    def say_hello(who='World'):
        return 'Hello, %s!' % who
    """)

    # test code; at least one test
    cli.src('tests/test_hello.py', r"""
    from hello import hello
    import pytest

    def test_hello():
        assert hello.say_hello() == 'Hello, World!'
        assert hello.say_hello('Pytest') == 'Hello, Pytest!'
    """)

    r = cli.run('tox')
    assert 'py27: commands succeeded' in r.out
    assert 'py36: commands succeeded' in r.out

    # directories .tox/ and *.egg-info/ got created
    assert cli.exists('.tox/')
    assert cli.exists('hello_world.egg-info/')

def test_interpreter_not_found(cli):
    cli.src('tox.ini', r"""
    [tox]
    envlist = py37

    [testenv]
    deps = pytest
    commands = pytest
    """)

    cli.src('setup.py', r"""
    from setuptools import setup
    setup(
        name='proj',
    )
    """)

    r = cli.run_err('tox')
    assert 'ERROR:   py37: InterpreterNotFound: python3.7' in r.out

